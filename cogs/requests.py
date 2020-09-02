import os
import discord
from tinydb import TinyDB, Query


from datetime import datetime, timezone, date
from dotenv import load_dotenv
from discord.ext import commands
from utilities import datedifference, formatting, settings, dbinteract
from random import randint

settings = settings.config("settings.json")


class Requests(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command()
    @commands.has_permissions(administrator=True)
    async def test(self, ctx):
        pass


    @commands.command()
    @commands.has_permissions(administrator=True)
    async def bunnysetup(self, ctx, *, id_post):
        db = TinyDB(settings.DB_PATH)
        member = Query()
        
        id_post = id_post + '-'
        id_build = ''
        user_ids = []
        dates = []
        i = 0

        for char in id_post:
            if char == '\n' or char == ',':
                if i % 2 == 0:
                    user_ids.append(int(id_build))
                else:
                    dates.append(id_build)
                id_build = ''
                i = i + 1
            else:
                id_build = id_build + char
        
        i = 0
        while i < len(user_ids) and i < len(dates): #Doesn't update the DB, only adds to it
            table = db.table(user_ids[i])
            table.upsert({'last_seen' : dates[i]}, member.id == user_ids[i])
            i = i + 1
        formatting.fancify(settings.DB_PATH)
    
    
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def dbsetup(self, ctx):
        member_list = []
        for member in ctx.guild.members:
            member_list.append(member.id)

        dbinteract.activity_push(member_list, 'before 2020-08-31')


    @commands.command()
    @commands.has_permissions(administrator=True)
    async def test2(self, ctx, target, *, reason):
        user = self.bot.get_user(int(target))

        embed = discord.Embed(title='Kick', color=0xff6464)
        embed.set_author(name=f'{user.name}#{user.discriminator}', icon_url=f'{user.avatar_url}')
        embed.add_field(name='Target', value=f'{user.mention}', inline=True)
        embed.add_field(name='Moderator', value=f'{ctx.author.mention}', inline=True)
        embed.add_field(name='Reason', value=f'{reason}', inline=False)
        embed.timestamp = ctx.message.created_at

        await ctx.send(embed=embed)
 

    @commands.command(help='noarg: a simple way to tell if the bot is online')
    @commands.has_role(settings.VERIFIED_ROLE_ID)
    async def ping(self, ctx):
        await ctx.send('pong')
    

    @commands.command(help='noarg: laney\'s request')
    @commands.has_role(settings.VERIFIED_ROLE_ID)
    async def bing(self, ctx):
        await ctx.send('bong')


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
        embed = discord.Embed(description='**(mention user) was (banned/kicked/action taken)', color=0xfefefe)
        embed.set_author(name='Target of the action', icon_url='https://i.imgur.com/oKHBjZt.png')
        embed.set_thumbnail(url='https://i.imgur.com/oKHBjZt.png')
        embed.timestamp = ctx.message.created_at
        embed.set_footer(text='Timestamp of action')

        await ctx.send(content='Logging Template (logged bans, logged kicks, logged...) \n__Color will change dependent on what action is taken__\nAuthor pic and thumbnail will both be the target\'s pfp', embed=embed)


def setup(bot):
    bot.add_cog(Requests(bot))