from ast import Delete
from unicodedata import name
from discord.ext import commands
import discord
from func import *
import datetime
from discord.ext import tasks
from discord.ext.commands.core import command


class Moderation(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        print('Модуль {} загружен'.format(self.__class__.__name__))

    @tasks.loop()
    async def check_mutes(self):
        current = datetime.datetime.now()
        mutes = load_json("jsons/mutes.json")
        users, times = list(mutes.keys()), list(mutes.values())
        for i in range(len(times)):
            time = times[i]
            unmute = datetime.datetime.strptime(str(time), "%c")
            if unmute < current:
                user_id = users[times.index(time)]
                try:
                    member = await self.guild.fetch_member(int(user_id))
                    await member.remove_roles(self.mutedrole)
                    mutes.pop(str(member.id))
                except discord.NotFound:
                    pass
                write_json("jsons/mutes.json", mutes)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def mute(self, ctx, member: discord.Member = None, time: str = None, *, reason="не указана"):
        if member is None:
            return await ctx.send(embed=discord.Embed(description='Укажите пользователя'))
        if member.bot is True:
            return await ctx.send(embed=discord.Embed(description='Вы не можете замутить бота!'))
        if member == ctx.author:
            return await ctx.send(embed=discord.Embed('Вы не можете замутить самого себя!'))
        if len(reason) > 150:
            return await ctx.send(embed=discord.Embed('Причина слишком длинная'))
        if member and member.top_role.position >= ctx.author.top_role.position:
            return await ctx.send(embed=discord.Embed('Вы не можете замутить пользователя с ролью выше вашей'))
        if time is None:
            return await ctx.send(embed=discord.Embed('Вы не указали длительность'))
        else:
            try:
                seconds = int(time[:-1])
                duration = time[-1]
                if duration == "s":
                    pass
                if duration == "m":
                    seconds *= 60
                if duration == "h":
                    seconds *= 3600
                if duration == "d":
                    seconds *= 86400
            except:
                return await ctx.send(embed=discord.Embed('Указана неправильная длительность'))
            mute_expiration = (datetime.datetime.now() + datetime.timedelta(seconds=int(seconds))).strftime("%c")
            role = self.mutedrole
            if not role:
                return await ctx.send(embed=discord.Embed('Я не могу найти роль мута!'))
            mutes = load_json("jsons/mutes.json")
            try:
                member_mute = mutes[str(member.id)]
                return await ctx.send(embed=discord.Embed('Этот пользователь уже замучен'))
            except:
                mutes[str(member.id)] = str(mute_expiration)
                write_json("jsons/mutes.json", mutes)
                await member.add_roles(role)
                await member.move_to(channel=None)
                embed = discord.Embed(title=f'Мут {member}', inline=False)
                embed.set_thumbnail(url=member.avatar_url)
                embed.add_field(name='НикНейм', value=member.mention, inline=False)
                embed.add_field(name='Модератор: ', value=ctx.author.mention, inline=False)
                embed.add_field(name='Время мута: ', value=mute_expiration, inline=False)
                embed.add_field(name='Причина: ', value=reason, inline=False)
                embed.set_footer(text='Разработчик - Xodor')
                await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def unmute(self, ctx, member: discord.Member):
        await member.remove_roles(self.mutedrole)
        await ctx.send(embed=discord.Embed(description=f"{ctx.author.name} размучен {member.display_name}"))
        mutes = load_json("jsons/mutes.json")
        mutes.pop(str(member.id))
        write_json("jsons/mutes.json", mutes)

    @commands.Cog.listener()
    async def on_ready(self):
        self.guild = await self.bot.fetch_guild('872925132786655339' or '979117594223198238')
        self.mutedrole = discord.utils.get(self.guild.roles, name='muted')
        self.check_mutes.start()

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def clear(self, ctx, amount: int):
        await ctx.channel.purge(limit=amount + 1)
        await ctx.send(embed=discord.Embed(description=f'Было удалено {amount} сообщений!'), delete_after=5)

    @commands.command()
    @commands.has_permissions(ban_members=True)
    @commands.guild_only()
    async def ban(self, ctx, member: discord.Member, *, reason='не указана'):
        if member != ctx.author:
            await member.ban(reason=reason)
            embed = discord.Embed(title='Бан пользователя')
            embed.set_thumbnail(url=member.avatar_url)
            embed.add_field(name='Забанен: ', value=member.display_name, inline=False)
            embed.add_field(name='Модератором: ', value=ctx.author.mention, inline=False)
            embed.add_field(name='Причина', value=reason, inline=False)
            embed.set_footer(text='Разработчик - Xodor')
            await ctx.send(embed=embed)
        else:
            await ctx.send('Вы не можете забанить самого себя!', delete_after=10)


    @ban.error
    async def ban_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.message.delete()
            await ctx.send(embed=discord.Embed(description='У вас не достаточно прав для того чтобы использовать данную команду!'), delete_after=5)
            return
        if isinstance(error, commands.MemberNotFound):
            await ctx.message.delete()
            await ctx.send(embed=discord.Embed(description='Пользователь не был найден!'), delete_after=5)
            return

    
    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, userid: int, reason='не указана'):
        user = await self.bot.fetch_user(userid)
        try:
            await ctx.guild.unban(user)
            embed = discord.Embed(title='Информация о разбане')
            embed.add_field(name='Ник', value=userid, inline=False)
            embed.add_field(name='Модератор', value=ctx.author, inline=False)
            embed.add_field(name='Причина', value=reason, inline=False)
            embed.set_footer(text='Разработчик - Xodor')
            await ctx.send(embed=embed)
            return
        except:
            return await ctx.send(embed=discord.Embed(description='Пользователь не находится в бане!', delete_after=3))

    @unban.error
    async def unban_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.message.delete()
            await ctx.send(embed=discord.Embed(description='У вас не достаточно прав для использование данной команды'), delete_after=5)


    @commands.command()
    @commands.has_permissions(administrator=True)
    async def moderation_help(self, ctx):
        embed = discord.Embed(title='Moderation Help')
        embed.set_author(name=ctx.message.guild.name, icon_url=ctx.message.guild.icon_url)
        embed.add_field(name='!help', value='Помощь по серверу', inline=False)
        embed.add_field(name='!ban', value='Забанить пользователя', inline=False)
        embed.add_field(name='!unban', value='Разбанить пользователя', inline=False)
        embed.add_field(name='!mute', value='Замутить пользователя', inline=False)
        embed.add_field(name='!unmute', value='Размутить пользователя', inline=False)
        embed.set_footer(text='Разработчик - Ходор')
        await ctx.send(embed=embed)


    
def setup(bot):
    bot.add_cog(Moderation(bot))