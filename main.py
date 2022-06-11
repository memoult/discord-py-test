
import discord
from discord.ext import commands
import asyncio
from discord.utils import get
from discord.utils import find
from discord.ext import commands
from discord.ext.commands import Bot
import os
from func import *

bot = commands.Bot(command_prefix="!", help_command=None, intents=discord.Intents.all())

bot.devs = '46284760702307533'

@bot.event
async def on_ready():
    print ('Бот включен')

    await bot.change_presence(status=discord.Status.online, activity=discord.Game('Для ознакомления пропишите !help'))

@bot.event
async def on_member_join(member):
    mutes =  load_json('jsons/mutes.json')
    if str(member.id) in mutes:
        role = discord.utils.get(member.guild.roles, name='muted')
        await member.add_roles(role)

@bot.command()
async def load(ctx, extension):
    extension = extension.lower()
    bot.load_extension(f'cogs.{extension}')
    await ctx.send(f'{extension} loaded')

@bot.command(pass_context=True)
async def reload(ctx, cog=None):
    if not int(ctx.author.id) in bot.devs:
        print("Перезапустить Cog не получилось!")
        embed=discord.Embed(title="Error", description=f"Вы не разработчик\nПо этому вы не можете перезапустить Cog", color=bot.red)
        msg = await ctx.send(embed=embed)
        await asyncio.sleep(5)
        await msg.delete()
    else:
        if not cog:
            return
        else:
            try:
                print('Перезапуск Cog')
                bot.reload_extension(cog)
                await ctx.message.add_reaction('✅')
                msg = await ctx.send(f'Перезапуск **{cog}**')
                await asyncio.sleep(20)
                await msg.delete()
            except Exception as e:
                await ctx.message.add_reaction('❌')
                msg = await ctx.send(f'Error **{cog}**!\n```{e}```')
                dev_logs = bot.get_channel(872925132786655342)
                mod_logs = bot.get_channel(872925132786655342)
                await asyncio.sleep(20)
                await msg.delete()
                await dev_logs.send(f'Error **{cog}**!\n```{e}```')
                await mod_logs.send(f'Error **{cog}**!\n```{e}```')

@bot.command()
async def unload(ctx, extension):
    extension = extension.lower()
    bot.unload_extension(f'cogs.{extension}')
    await ctx.send(f'{extension} unloaded')


for filename in os.listdir("./cogs"):
    if filename.endswith(".py") and not filename.startswith("_"):
        bot.load_extension(f"cogs.{filename[:-3]}")



bot.run('ODcyOTI1MjQzNjM3OTE1Njg5.Gl8MOx.RXhcmMnTzt-_B4vt31iAhGzyMoKBfCLp7i1BK0')