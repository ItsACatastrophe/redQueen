import discord
import asyncio
# import syllables

from discord.ext import commands
from utilities import formatting, settings
from random import randint
from cogs.battle import fighter as fighter_util
from cogs.battle import battle as battle_util


settings = settings.config("settings.json")

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        #rps vars
        self.rps1 = None #challenger member
        self.rps2 = None #challengee member
        self.input1 = None
        self.input2 = None
        self.rps_channel = None
        self.rps_state = 0
        self.set = 0


    #use subcommands with this later on to make it crisp
    @commands.command(help='(start/choose) (verified user)')
    #@commands.has_role(VERIFIED_ROLE_ID) #this breaks the dm-aspect of the game
    async def rps(self, ctx, state, *, selection=None):
        if state.lower() == 'start' and self.rps_state == 0:
            self.rps2 = formatting.get_from_in(self.bot, ctx, "mem", selection)

            self.rps1 = ctx.message.author
            self.rps_state = 1
            self.rps_channel = ctx.message.channel

            await ctx.send(content='Please send your choice to my dm using: \n> **,rps choose rock**   **,rps choose paper**  **,rps choose scissors**')

            for i in range(60):
                if self.rps_state == 0:
                    return
                await asyncio.sleep(1)

            await self.rps_channel.send(content='No response, game has timed out')

            self.rps_state = 0
            self.rps1 = None 
            self.rps2 = None 
            self.input1 = None
            self.input2 = None
            self.rps_channel = None
        
        if state.lower() == 'start' and self.rps_state == 1:
            await self.rps_channel.send(content='There\'s an ongoing game, please wait for them to finish!')

        if state.lower() == 'choose' and ctx.guild is None :
            if ctx.author == self.rps1:
                self.input1 = selection.lower()
                await ctx.send(content='Choice received')
                await self.rps_channel.send(f'Received from **{self.rps1.name}#{self.rps1.discriminator}**')

            if ctx.author == self.rps2:
                self.input2 = selection.lower()
                await ctx.send(content='Choice recieved')
                await self.rps_channel.send(f'Received from **{self.rps2.name}#{self.rps2.discriminator}**')
        
        if self.input1 != None and self.input2 != None:
            #I'm not positive how to do this other than comparing the if statements. Maybe assigning them to numbers... but the hierachy makes a circle so there's no value comparison that works
            winner = None
            if self.input1 == self.input2: 
                winner = None
            elif self.input1 == 'rock' and self.input2 == 'paper':
                winner = self.rps2
            elif self.input1 == 'rock' and self.input2 == 'scissors':
                winner = self.rps1
            elif self.input1 == 'paper' and self.input2 == 'rock':
                winner = self.rps1
            elif self.input1 == 'paper' and self.input2 == 'scissors':
                winner = self.rps2
            elif self.input1 == 'scissors' and self.input2 == 'rock':
                winner = self.rps2
            elif self.input1 == 'scissors' and self.input2 == 'paper':
                winner = self.rps1
            else:
                await self.rps_channel.send(content='Someone gave an incorrect input. Please start a new game.')

                self.rps_state = 0
                self.rps1 = None 
                self.rps2 = None 
                self.input1 = None
                self.input2 = None
                self.rps_channel = None
            
                return

            try:
                embed = discord.Embed(title='Rock! Paper! Scissors!', description=f'**{winner.mention} is the winner!**', color=0x64b4ff)
            except AttributeError:
                embed = discord.Embed(title='Rock! Paper! Scissors!', description=f'', color=0x64b4ff)

            if randint(1, 100) == 1 and winner is not None:
                loser = None
                if winner is self.rps1:
                    loser = self.rps2
                else:
                    loser = self.rps1
                embed.description = f'**{winner.mention} would have won but they cheated so __{loser.mention} wins!__**'

            if winner is None:
                embed.set_thumbnail(url='https://i.imgur.com/TIGi71f.png') #thumbnail for no winner
                embed.description = '**It\'s a tie!**'
            else: 
                embed.set_thumbnail(url='https://i.imgur.com/GWKFyR9.png') #thumbnail for anyone winning

            embed.add_field(name=f'{self.rps1.name}#{self.rps1.discriminator}', value=f'{self.input1}', inline=False)
            embed.add_field(name=f'{self.rps2.name}#{self.rps2.discriminator}', value=f'{self.input2}', inline=False)
            embed.timestamp = ctx.message.created_at

            await self.rps_channel.send(embed=embed)
            
            self.rps_state = 0
            self.rps1 = None 
            self.rps2 = None 
            self.input1 = None
            self.input2 = None
            self.rps_channel = None


    @commands.command(help='(user)')
    @commands.has_role(settings.VERIFIED_ROLE_ID)
    async def ship(self, ctx, target1, target2=None):
        member2 = formatting.get_from_in(self.bot, ctx, "mem", target1)

        #checking to see if author is implied as a target
        if target2:
            member1 = formatting.get_from_in(self.bot, ctx, "mem", target2)

        else:
            member1 = ctx.author

        num1 = member1.id%1000 #command user
        num2 = member2.id%1000 #target
        comp_num = (num1 + num2 - 40)%101
        bars_ref = comp_num//10
        bars_on = bars_ref*'<a:baron:725816473704202242>'
        bars_off = (10-bars_ref)*'<a:baroff:725816609176027635>'
        status = None

        #this seems sloppy, I think there's a better way to do this. Fixed by using if elif.
        while True:
            if comp_num == 100:
                status = 'You\'re made for eachother <a:true_love:725827494585827481>'
            if comp_num >= 90:
                status = 'True love :heart_eyes:'
                break
            if comp_num >= 80:
                status = 'Wew is it hot in here? :fire:'
                break
            if comp_num >= 70:
                status = 'Just 2 gals being pals :wink:'
                break
            if comp_num == 69:
                status = 'Nice <a:okhandspin:644684375287660564>'
                break
            if comp_num >= 60:
                status = 'Budding potential :heart:'
                break
            if comp_num >= 50:
                status = 'Besties :smile:'
                break
            if comp_num >= 40:
                status = 'Lets just be friends :eyes:'
                break
            if comp_num >= 30:
                status = 'It\'s not you it\'s me... :eyes:'
                break
            if comp_num >= 20:
                status = 'Prepare to get ghosted :ghost:'
                break
            if comp_num >= 10:
                status = 'Bitter rivals :angry:'
                break
            if comp_num >= 1:
                status = 'Sworn enemies :right_facing_fist::left_facing_fist: '
                break
            else:
                status = 'She\'s practically your sister! :nauseated_face:'
                break

        embed = discord.Embed(description=f'**{comp_num}%** {bars_on}{bars_off} {status}', color=0xe484dc)

        await ctx.message.delete()
        await ctx.send(content=f'{member1.mention} and {member2.mention} sitting in a tree...', embed=embed)


    @commands.command(help='(num of dice)d(faces on die) + (modifiers)')
    @commands.has_role(settings.VERIFIED_ROLE_ID)
    async def roll(self, ctx, *, roll):
        roll = roll.lower()
        split = roll.index('d')
        modifier = False
        dice_num = int(roll[:split])

        if dice_num > 100:
            await ctx.send(content='Thats way too many dice. Please roll a smaller amount')
            return

        try:
            dice_faces = int(roll[split+1:roll.index('+')-1])
            modifier = int(roll[roll.index('+')+1:])
        except ValueError:
            dice_faces = int(roll[split+1:])

        if dice_faces > 10000:
            await ctx.send(content='I don\'t think they make die with that many sides. Please use a smaller amount.')
            return
            
        roll_results = []
        message = ''

        while dice_num > 0:
            roll = randint(1, dice_faces)
            roll_results.append(roll)
            message = message + f'[ **{roll}** ]  + '
            dice_num -= 1
        message = message [:-3]

        if modifier:
            roll_results.append(modifier)
            message = message + f'+ {modifier}'

        results = 0
        for roll in roll_results:
            results += roll
        
        message = message + f'\n\n__Total__ = {results}'
        await ctx.send(content=message)


    #UNFINISHED
    @commands.command(help='(user)', aliases=['deathbattle', 'fight'])
    @commands.has_role(settings.VERIFIED_ROLE_ID)
    async def battle(self, ctx, target1, target0=None):
        fighter1 = fighter_util.Fighter(formatting.get_from_in(self.bot, ctx, "mem", target1), 1)
        if target0:
            fighter0 = fighter_util.Fighter(formatting.get_from_in(self.bot, ctx, "mem", target0), 0)
        else:
            fighter0 = fighter_util.Fighter(ctx.author, 0)

        fighters = [fighter0, fighter1]
        users_set = {fighter0.user, fighter1.user}

        for fighter in fighters:
            if fighter.user.bot:
                choices = list(battle_util.weapon_choice.keys())
                seed = randint(0, len(choices) - 1)
                fighter.set_weapon(choices[seed])

        embed = discord.Embed(description=f'{fighters[0].user.name} 🆚 {fighters[1].user.name}', color=0x64b4ff)
        embed.add_field(name=fighters[0].name, value='?', inline=True)
        embed.add_field(name=fighters[1].name, value='?', inline=True)
        embed.add_field(name='Choose your weapon', value='If your weapon is not selected on reaction, please re-react', inline=False)
        message = await ctx.send(embed=embed)

        for emote in battle_util.weapon_choice.keys():
            await message.add_reaction(emote)

        reaction_list = set()
        waiting = True
        def check(reaction, user):
            if reaction.message == message:
                reaction_list.add(user)

                for fighter in fighters:
                    if user == fighter.user and not fighter.user.bot:
                        fighter.set_weapon(reaction.emoji)
                        #Something has to be returned or else it just hangs
                        return True

        while not fighters[0].weapon or not fighters[1].weapon:
            await self.bot.wait_for('reaction_add', check=check, timeout=20.0)
            done = await self.bot.wait_for('reaction_add', check=check, timeout=20.0)
            if done is None:
                await ctx.send('__**Error:**__\nThe pending game has timed out!')
            for fighter in fighters:
                try:
                    embed.set_field_at(index=fighter.position, name=embed.fields[fighter.position].name, value=fighter.weapon.icon)
                except:
                    embed.set_field_at(index=fighter.position, name=embed.fields[fighter.position].name, value='?')
            await message.edit(embed=embed)

        embed.clear_fields()
        embed.add_field(name=f'{fighters[0].name} - {fighters[0].weapon.icon}', value=f'{fighters[0].hp}/{fighters[0].hp_max} {fighters[0].heart}', inline=True)
        embed.add_field(name=f'{fighters[1].name} - {fighters[1].weapon.icon}', value=f'{fighters[1].hp}/{fighters[1].hp_max} {fighters[1].heart}', inline=True)
        await message.edit(embed=embed)

        attacker = randint(0, 1)
        description = ''
        turns = 2
        while fighters[0].hp > 0 and fighters[1].hp > 0:
            attacked = attacker
            attacker = (attacked + 1) % 2
            seed = randint(0, 1000)
            data = {
                'seed': seed,
                'turn': turns // 2,
                'attacker': fighters[attacker],
                'attacked': fighters[attacked],
                'embed': embed,
            }

            results = fighters[attacker].attack(data)
            text = results.get('text').format(attacker=fighters[attacker].name, attacked=fighters[attacked].name)
            text = '{heart} '.format(heart=fighters[attacker].circle) + text
            description = battle_util.text_handler(self, text, description)

            embed.description = description
            field_name = embed.fields[fighters[attacked].position].name
            field_value = f'{max(0, fighters[attacked].hp)}/100 {fighters[attacked].heart}'
            embed.set_field_at(index=attacked, name=field_name, value=field_value)
            embed.color = fighters[attacker].color
            await message.edit(embed=embed)

            await asyncio.sleep(2)
            turns += 1
            
        if fighters[0].hp < fighters[1].hp:
            winner = 1
        else:
            winner = 0
        
        text = f'👑 __**{fighters[winner].name}**__ has deafeated __{fighters[(winner + 1) % 2].name}__'
        embed.description = battle_util.text_handler(self, text, description)
        embed.add_field(name='Winner', value=fighters[winner].user.mention, inline=False)
        await message.edit(embed=embed)


    @commands.command(aliases=['whatsthis', 'owo'], help='no arg: requested by Naaz')
    @commands.has_role(settings.VERIFIED_ROLE_ID)
    async def naazify(self, ctx):
        async for message in ctx.channel.history(limit=2):
            if message.id != ctx.message.id:
                break   #of the two messages, one being the function call and the other being the message above it, we choose whichever is not our function call.  
        emoteList = ['┌[ ◔ ͜ ʖ ◔ ]┐', 'ヽ༼ ் ▽ ் ༽╯', '୧[ * ಡ ▽ ಡ * ]୨', 'ヽ༼ ͠ ͠° ͜ʖ ͠ ͠° ༽ﾉ', '(✿ ◕‿◕)', 'ᕕ( ՞ ᗜ ՞ )ᕗ', 's( ^ ‿ ^)-b', 'ლ ( ◕  ᗜ  ◕ ) ლ', '╰(◕ᗜ◕)╯', '░ ∗ ◕ ں ◕ ∗ ░', '(⊹つ•۝•⊹)つ', '(∩╹□╹∩)', '(✿ ◕ᗜ◕)━♫.*･｡ﾟ', 'ʕ ⊃･ ◡ ･ ʔ⊃', '╭(◕◕ ◉෴◉ ◕◕)╮', '♪ヽ( ⌒o⌒)人(⌒-⌒ )v ♪', '╰(✿˙ᗜ˙)੭━☆ﾟ.*･｡ﾟ', '(ง ͡ʘ ͜ʖ ͡ʘ)ง', '乁༼☯‿☯✿༽ㄏ', 'c(ˊᗜˋ*c)']
        seed1 = randint(0, len(emoteList) - 1) #string multiplier to determine whether or not start multiplying
        seed2 = randint(0, len(emoteList) - 1)
        m = list(message.content)

        #building the string
        leadFace = f'{emoteList[seed1]} '

        i = 0
        while i < len(m): #replacing necessary characters with l's and w's
            if m[i] == 'l' or m[i] == 'r':
                m[i] = 'w'
            elif m[i] == 'L' or m[i] == 'R':
                m[i] = 'W'
            try:
                if m[i-1] == ' ' and randint(0,9) == 0:
                    m.insert(i, m[i] + '-')
            except IndexError:
                pass
            i = i + 1
        
        stut = (m[0] + '-')*(seed1 % 2)
        trailFace = f' {emoteList[seed2]}'
        
        body = ''
        i = 0
        while i < len(m):
            body = body + m[i]
            i = i + 1

        sO = f'**{message.author}**: {leadFace}{stut}{body}{trailFace}' 
        
        await ctx.message.delete()
        await ctx.send(content=sO)


    @commands.command(aliases=['8-ball', '8ball', 'magic8ball'], help='(question) requested by Annalina')
    @commands.has_role(settings.VERIFIED_ROLE_ID)
    async def magic8(self, ctx, *, string):
        if 'server owner' in string.lower() or 'serverowner' in string.lower():
            out = 'Do __**NOT**__ ask who owns the server.'

        elif 'love' in string.lower():
            out = 'I am incapable of understanding love.'
        
        elif 'blue queen' in string.lower() or 'bluequeen' in string.lower():
            out = 'Leave *her* out of this.'

        elif ' ban' in string.lower() or ' banned' in string.lower():
            out = '**Yes!**'

        else:
            responses = ['**ABSOLUTELY NOT**',
            'As I see it, yes.', 
            'Ask again later.',
            'Better not tell you now.',
            'Can you word your question better?',
            'Cannot predict now.',
            'Concentrate and ask again.',
            'Do not count on it.',
            'If I say yes will you stop asking?',
            'It is certain.',
            'It is decidedly so.',
            'Most likely.',
            'My reply is no.',
            'My sources say no.',
            'Outlook not so good.',
            'Outlook good.',
            'Reply hazy, try again.',
            'Signs point to yes.',
            'Sure, why not...',
            'Try asking in the waiting room',
            'Very doubtful.',
            'Without a doubt.',
            'Yeeaaa... No.',
            'Yes.',
            'Yes – definitely.',
            'You cannot handle the truth',
            'You may rely on it.']
            seed = randint(0, len(responses)-1)
            out = '🎱 ' + responses[seed]
        await ctx.send(out)

    @commands.command(aliases=['keyed'], help='(question) requested by Annalina')
    @commands.has_role(settings.VERIFIED_ROLE_ID)
    async def based(self, ctx):
        async for message in ctx.channel.history(limit=2):
            if message.id != ctx.message.id:
                break
        await ctx.message.delete()
        emotes = [
            '\N{Regional Indicator Symbol Letter B}',
            '\N{Regional Indicator Symbol Letter A}',
            '\N{Regional Indicator Symbol Letter S}',
            '\N{Regional Indicator Symbol Letter E}',
            '\N{Regional Indicator Symbol Letter D}',
            '\U00002753',
            '\N{Regional Indicator Symbol Letter O}',
            '\N{Regional Indicator Symbol Letter N}',
            '\U00002754',
            '\N{Regional Indicator Symbol Letter W}',
            '\N{Regional Indicator Symbol Letter H}',
            '\U0001F170',
            '\N{Regional Indicator Symbol Letter T}'
        ]
        while emotes:
            await message.add_reaction(emotes.pop(0))

    def haiku_helper(self, words, sylla_goal):
        count = 0
        for word in words:
            count += syllables.estimate(word)
            if count > sylla_goal:
                return

    # @commands.command()
    # @commands.has_role(settings.VERIFIED_ROLE_ID)
    # async def haiku(self, ctx, *, message):
    #     words = message.lower().split()
    #     count = 0
    #     for word in words:
    #         count += syllables.estimate(word)
    #         if count > 17:
    #             return
    #     if count < 17:
    #         return

    #     count = 0
    #     for word in words:
    #         count += syllables.estimate(word)
    #         if count


def setup(bot):
    bot.add_cog(Fun(bot))