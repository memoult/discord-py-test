from aiogram import bot
import discord
from discord.ext import commands

class HelpCommand(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        print('Модуль {} загружен'.format(self.__class__.__name__))

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def help_command(self, ctx):
        embed = discord.Embed(title='Help Command')
        embed.set_author(name=ctx.message.guild.name, icon_url=ctx.message.guild.icon_url)
        embed.add_field(name='!kiss', value='Поцеловать пользователя', inline=False)
        embed.add_field(name='!hug', value='Обнять пользователя', inline=False)
        embed.add_field(name='!slap', value='Ударить пользователя', inline=False)
        embed.add_field(name='!help_comand', value='Помощь по командам', inline=False)
        embed.add_field(name='!help', value='Помощь по серверу', inline=False)
        embed.add_field(name='!userinfo', value='Узнать информацию о пользователе', inline=False)
        embed.set_footer(text='Разработчик - Ходор')
def setup(bot):
    bot.add_cog(HelpCommand(bot))
