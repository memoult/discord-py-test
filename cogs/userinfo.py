from discord.ext import commands
import discord
import datetime


class UserInfo(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        print('Модуль {} запущен'.format(self.__class__.__name__))


    @commands.command()
    async def userinfo(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.author
        roles = [role for role in member.roles]
        embed = discord.Embed(title=f"Информация о пользователе {member.name}")
        embed.set_thumbnail(url=member.avatar_url)
        embed.add_field(name="ID: ", value=member.id, inline=True)
        embed.add_field(name="НикНейм: ", value=member.display_name, inline=True)
        embed.add_field(name="Аккаунт был создан: ", value=member.created_at.strftime("%d.%m.%Y %H:%M:%S"), inline=True)
        embed.add_field(name="Зашел на сервер: ", value=member.joined_at.strftime("%d.%m.%Y %H:%M:%S"), inline=True)
        embed.add_field(name="Роли: ", value="".join(role.mention for role in roles), inline=True)
        embed.add_field(name="Самая высокая роль: ", value=member.top_role.mention, inline=True)
        embed.add_field(name="Этот пользователь бот? ", value=member.bot, inline=True)
        embed.set_footer(text='Разработчик - Xodor')
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(UserInfo(bot))
