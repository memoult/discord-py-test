import discord
from discord.ext import commands


class Logs(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        print('Модуль {} загружен'.format(self.__class__.__name__))

    @commands.Cog.listener()
    async def on_member_join(self, member):
        msg = f'{member.name} зашел на сервер!'
        await self.bot.get_channel(980541965223485450).send(msg)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        msg = f'{member.name} вышел с сервера!'
        await self.bot.get_channel(980541965223485450).send(msg)

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        msg = f'Сообщение до изменений {before.content}\n' \
                f'Сообщение после {after.content}'
        await self.bot.get_channel(980544131891875880).send(msg)

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        msg = f'Удаленное сообщение: {message.content}'
        await self.bot.get_channel(980544131891875880).send(msg)

    @commands.Cog.listener()
    async def on_voice_state_update(self, member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
        if before.channel is None:
            msg = f'{member.display_name} зашел в канал {after.channel.mention}'
            await self.bot.get_channel(980546189969727550).send(msg)
        elif after.channel is None:
            msg = f'{member.display_name} покинул канал {before.channel.mention}'
            await self.bot.get_channel(980546189969727550).send(msg)
        elif before.channel != after.channel:
            msg = f'{member.display_name} перешел из канал {before.channel.mention} в канал {after.channel.mention}'
            await self.bot.get_channel(980546189969727550).send(msg)
def setup(bot):
    bot.add_cog(Logs(bot))