import discord
from discord.ext import commands
import random


kiss = ['https://c.tenor.com/F02Ep3b2jJgAAAAM/cute-kawai.gif',
        'https://c.tenor.com/16MBIsjDDYcAAAAM/love-cheek.gif',
        'https://c.tenor.com/wPzIJLI3IeQAAAAC/kiss-hot.gif',
        'https://c.tenor.com/HKK43jaPV2QAAAAd/milk-and-mocha-love-you-lots.gif'
        ]

hug = ['https://acegif.com/wp-content/gif/anime-hug-41.gif',
        'https://pa1.narvii.com/7673/03a994f187deb264a6f60ce9cbbf8357e44b90c9r1-500-281_hq.gif',
        'https://c.tenor.com/OXCV_qL-V60AAAAC/mochi-peachcat-mochi.gif',
        'https://c.tenor.com/XyMvYx1xcJAAAAAC/super-excited.gif'
        ]


slap = ['https://c.tenor.com/pYXfwOc2JCQAAAAC/despierta-ya.gif',
        'https://c.tenor.com/2L_eT6hPUhcAAAAC/spongebob-squarepants-patrick-star.gif',
        'https://c.tenor.com/DWI_Vtq_9_cAAAAC/slap-face.gif',
        'https://c.tenor.com/gro7rD1KWr8AAAAC/simpsons-slap.gif'
        ]

class Action(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        print('Модуль {} загружен'.format(self.__class__.__name__))

    @commands.command()
    async def kiss(self, ctx, member: discord.Member):
        embed = discord.Embed()
        embed.set_image(url=random.choice(kiss))
        embed.set_footer(text='Разработчик - Xodor')
        await ctx.send(f'{ctx.author.mention} поцеловал {member.mention}', embed=embed)

    @commands.command()
    async def hug(self, ctx, member: discord.Member):
        embed = discord.Embed()
        embed.set_image(url=random.choice(hug))
        embed.set_footer(text='Разработчик - Xodor')
        await ctx.send(f'{ctx.author.mention} крепко обнял {member.mention}', embed=embed)

    @commands.command()
    async def slap(self, ctx, member: discord.Member):
        embed = discord.Embed()
        embed.set_image(url=random.choice(slap))
        embed.set_footer(text='Разработчик - Xodor')
        await ctx.send(f'{ctx.author.mention} сильно ударил {member.mention}!', embed=embed)

def setup(bot):
    bot.add_cog(Action(bot))