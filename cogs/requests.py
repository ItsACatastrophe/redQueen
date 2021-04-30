import discord
import os

from ast import literal_eval
from discord.ext import commands
from utilities import formatting, settings, dbinteract
from tinydb import TinyDB, Query
from random import randint

from cogs.battle import fighter as fighter_util
from cogs.battle import battle as battle_util

settings = settings.config("settings.json")


class Requests(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.guild = self.bot.get_guild(settings.GUILD_ID)
        self.role = None


    @commands.command()
    @commands.has_permissions(administrator=True)
    async def test(self, ctx, *, inp):
        await ctx.send('')        

    #@commands.command()
    #@commands.has_permissions(administrator=True)
    #async def dbrecover(self, ctx, * , members):
        

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def test2(self, ctx):
        await ctx.send(formatting.get_from_in(self.bot, ctx, "use", ctx.author.id).name)
        #should send "Cat"


    @commands.command()
    @commands.has_permissions(administrator=True)
    async def test3(self, ctx):
        db = TinyDB(settings.DB_PATH + 'temp' + '.json')
        table = db.table('test')
        member = Query()
        test = table.get(member.test_key1 != None)['test_key1'] #Grabs document_id X containing member.y and then finds value corresponding to ['key_str']
        print(test)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def fix_the_server(self, ctx, *, string):
        await ctx.send("I've started fixing the server")
        try:
            channels = literal_eval(string)
        except Exception as e:
            await ctx.send(f"something went wrong: {e}")
            return
        for channel_id in channels:
            channel = self.bot.get_channel(channel_id)
            if channel.name != channels[channel_id]:
                await channel.edit(name=channels[channel_id])
        await ctx.send("Everything **should** be fixed")


    @commands.command()
    @commands.has_permissions(administrator=True)
    async def log_the_server(self, ctx):
        string = "```{"
        for channel in ctx.guild.channels:
            if len(string) > 1500:
                string = string + "}```"
                await ctx.send(string)
                string = "```{"
            string = f'{string}{channel.id}:"{channel.name}",'
        string = string + "}```"
        await ctx.send(string)


    @commands.command()
    @commands.has_permissions(administrator=True)
    async def bunnysetup(self, ctx, *, id_post):
        id_post = id_post + '-'
        id_build = ''
        user_ids = []
        dates = []
        i = 0

        for char in id_post:
            if char == '\n' or char == ',':
                if i % 2 == 0:
                    user_ids.append(id_build)
                else:
                    dates.append(id_build)
                id_build = ''
                i = i + 1
            else:
                id_build = id_build + char
        
        i = 0
        while i < len(user_ids) and i < len(dates): #Doesn't update the DB, only adds to it
            path = settings.DB_PATH + user_ids[i] + '.json'
            db = TinyDB(path)
            member = Query()
            table = db.table('information')
            table.upsert({'last_seen' : dates[i]}, member.last_seen != None)
            i = i + 1
            formatting.fancify(path)
    
    
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def dbsetup(self, ctx):
        member_list = []
        for member in ctx.guild.members:
            member_list.append(member.id)

        dbinteract.activity_push(member_list, 'before 2020-08-31')


    @commands.command()
    @commands.has_permissions(administrator=True)
    async def dbcleanup(self, ctx):
        member_list = []
        for member in ctx.guild.members:
            member_list.append(member.id)

        file_list = []
        for file in os.listdir(settings.DB_PATH):
            file_list.append(int(file[0:-5]))
            
        print(file_list)
        for fname in file_list:
            if fname not in member_list:
                os.remove(str(fname) + ".json")


    @commands.command()
    @commands.is_owner()
    async def test_weapon(self, ctx, num_tests, num_round, weapon_emote):
        fighter = fighter_util.Fighter(ctx.author, 0)
        fighter.set_weapon(weapon_emote)
        weapon_name = str(fighter.weapon)
        kills = 0

        with open(f'{weapon_name}.csv', 'w+') as weapon_file:
            weapon_file.write(f'{fighter.weapon}\n')

            index_test = 0
            total_damage = 0
            while index_test < int(num_tests):

                index_round = 0
                damage = 0
                turns = 1
                temp_fighter = fighter_util.Fighter(ctx.author, 0)
                temp_fighter.set_weapon(weapon_emote)
                while index_round < int(num_round):
                    seed = randint(0, 1000)
                    data = {
                        'seed': seed,
                        'turn': turns,
                        'attacker': temp_fighter,
                        'attacked': temp_fighter,
                    }
                    results = temp_fighter.attack(data)
                    damage += results.get('damage')
                    index_round += 1
                    turns += 1
                if damage >= 100:
                    damage = 100
                    kills += 1

                weapon_file.write(f'{min(100, damage)}\n')
                total_damage += min(100, damage)
                index_test += 1

        await ctx.send(
            content=f'Your test of {weapon_emote} is complete.\nThe mean (where damage is (0, 100]) is {total_damage/int(num_tests)}\nKill proportion {kills/int(num_tests)}', 
            file=discord.File(
                fp=f'{weapon_name}.csv', 
                filename=f'{weapon_name}.csv'
            )
        )


    @commands.command()
    @commands.is_owner()
    async def test_weapons(self, ctx, num_tests, num_round):
        fighters = [] # Each entry represents a different weapon
        weapon_names = []
        weapon_emotes = []
        total_damage = []
        kills = []
        for weapon in battle_util.weapon_choice:
            fighter = fighter_util.Fighter(ctx.author, 0)
            fighter.set_weapon(weapon)
            fighters.append(fighter)
            weapon_names.append(str(fighter.weapon))
            weapon_emotes.append(weapon)
            total_damage.append(0)
            kills.append(0)

        with open(f'Weapons.csv', 'w+') as weapon_file:
            for weapon in weapon_names:
                weapon_file.write(f'{weapon},')
            weapon_file.write('\n')

            index_test = 0
            while index_test < int(num_tests):
                
                index_fighter = 0
                for fighter in fighters:

                    index_round = 0
                    damage = 0
                    turns = 1
                    temp_fighter = fighter_util.Fighter(ctx.author, 0)
                    temp_fighter.set_weapon(weapon_emotes[index_fighter])
                    while index_round < int(num_round):
                        seed = randint(0, 1000)
                        data = {
                            'seed': seed,
                            'turn': turns,
                            'attacker': temp_fighter,
                            'attacked': temp_fighter,
                        }
                        results = temp_fighter.attack(data)
                        damage += results.get('damage')
                        
                        index_round += 1
                        turns += 1
                    if damage >= 100:
                        damage = 100
                        kills[index_fighter] += 1
                    weapon_file.write(f'{min(100, damage)},')
                    total_damage[index_fighter] += min(100, damage)
                    index_fighter += 1
                index_test += 1
                weapon_file.write(f'\n')
        
        string = '\n__Averages where damage is (0, 100]__\n'
        i = 0
        for fighter in fighters:
            string = f'{string}{weapon_names[i]}: {total_damage[i]/int(num_tests)}\n'
            i += 1
        string = string + '__Kill proportions__\n'
        i = 0
        for kill_total in kills:
            string = f'{string}{weapon_names[i]}: {kill_total/int(num_tests)}\n'
            i += 1

        await ctx.send(content=f'Your test of all weapons is complete{string}', file=discord.File(fp=f'Weapons.csv', filename=f'Weapons.csv'))


    @commands.command(help='noarg: a simple way to tell if the bot is online')
    @commands.has_role(settings.VERIFIED_ROLE_ID)
    async def ping(self, ctx):
        await ctx.send('pong')
    

    @commands.command(help='noarg: laney\'s request')
    @commands.has_role(settings.VERIFIED_ROLE_ID)
    async def bing(self, ctx):
        await ctx.send('bong')


    @commands.command(help='noarg')
    @commands.has_role(settings.VERIFIED_ROLE_ID)
    async def latency(self, ctx):
        await ctx.send(content=f'Delay of discord client: **{round(self.bot.latency, 3)} seconds**')


    @commands.command(help='noarg: myka\'s request')
    @commands.has_role(settings.VERIFIED_ROLE_ID)
    async def alice(self, ctx):
        await ctx.send('You\'re all going to die down here.')


    @commands.command(help='noarg: cat\'s request')
    @commands.has_role(settings.VERIFIED_ROLE_ID)
    async def howlong(self, ctx):
        await ctx.send('too long')


    @commands.command(help='noarg: annalina\'s request')
    @commands.has_role(settings.VERIFIED_ROLE_ID)
    async def serverowner(self, ctx):
        await ctx.message.delete(delay=1)


    #negative mod action
    @commands.command(help='no arg')
    @commands.has_permissions(administrator=True)
    async def format1(self, ctx):
        embed = discord.Embed(title='Name of the action', color=0xff6464)
        embed.set_author(name='Target of the action', icon_url='https://i.imgur.com/oKHBjZt.png')
        embed.add_field(name='Category1', value='Body1', inline=True)
        embed.add_field(name='Category2', value='Body2', inline=True)
        embed.add_field(name='Category3', value='Body3', inline=False)
        embed.timestamp = ctx.message.created_at
        embed.set_footer(text='Timestamp of action')

        await ctx.send(content='Negative Moderation Action Template (banning, kicking, timing-out)', embed=embed) 


    #positive mod action
    @commands.command(help='no arg')
    @commands.has_permissions(administrator=True)
    async def format2(self, ctx):
        embed = discord.Embed(title='Name of the action', color=0x64ff64)
        embed.set_author(name='Target of the action', icon_url='https://i.imgur.com/oKHBjZt.png')
        embed.add_field(name='Category1', value='Body1', inline=True)
        embed.add_field(name='Category2', value='Body2', inline=True)
        embed.add_field(name='Category3', value='Body3', inline=False)
        embed.timestamp = ctx.message.created_at
        embed.set_footer(text='Timestamp of action')

        await ctx.send(content='Positive Moderation Action Template (unbanning, ?unkicking?, un-timing-out)', embed=embed)
    

    #neutral info/short response
    @commands.command(help='no arg')
    @commands.has_permissions(administrator=True)
    async def format3(self, ctx):
        embed = discord.Embed(title='Name of the command', color=0x64b4ff)
        embed.set_author(name='Target of the command (if none then user who called the command or potentially empty section)', icon_url='https://i.imgur.com/oKHBjZt.png')
        embed.add_field(name='Category1', value='Body1', inline=True)
        embed.add_field(name='Category2', value='Body2', inline=True)
        embed.add_field(name='Category3', value='Body3', inline=False)
        embed.timestamp = ctx.message.created_at
        embed.set_footer(text='Timestamp of action')

        await ctx.send(content='Information Response Template (userinfo, whoin, howmany), also used for short responses to commands', embed=embed)


    #log
    @commands.command(help='no arg')
    @commands.has_permissions(administrator=True)
    async def format4(self, ctx):
        embed = discord.Embed(description='**(mention user) was (banned/kicked/action taken)**', color=0xfefefe)
        embed.set_author(name='Target of the action', icon_url='https://i.imgur.com/oKHBjZt.png')
        embed.set_thumbnail(url='https://i.imgur.com/oKHBjZt.png')
        embed.timestamp = ctx.message.created_at
        embed.set_footer(text='Timestamp of action')

        await ctx.send(content='Logging Template (logged bans, logged kicks, logged...) \n__Color will change dependent on what action is taken__\nAuthor pic and thumbnail will both be the target\'s pfp', embed=embed)


def setup(bot):
    bot.add_cog(Requests(bot))