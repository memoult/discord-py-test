from aiogram import Bot
import discord
from discord.ext import commands

class ErrorOfCommand(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

@commands.Cog.listener()
async def on_command_error(ctx, error):
    print(error)

    if isinstance(error, commands.MissingPermissions):
        await ctx.send(f'{ctx.mention}, У вас не достаточно прав для выполнение этой команды!')
    elif isinstance(error, commands.UserInputError):
        await ctx.send(embed=discord.Embed(
            description=f"Правильное использование команды: '{ctx.prefix}{ctx.command.name}' ({ctx.command.brief})\nПример: {ctx.prefix}{ctx.command.usage}"
        ))

    @commands.Cog.listener()
    async def on_ready(self):
        print("ErrorOfCommand загружен")
        
def setup(bot):
    bot.add_cog(ErrorOfCommand(bot))