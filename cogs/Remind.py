import discord
import datetime
import asyncio
from discord.ext import commands, timers
TIMEZONE = 3 # set timezone "UTC +value"

class Remind(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.bot.timer_manager = timers.TimerManager(self.bot)

	@commands.command()
	async def remind(self, ctx, time, *, text):
		msg_date = ctx.message.created_at
		date = msg_date + datetime.timedelta(hours = float(time))
		mf = msg_date + datetime.timedelta(TIMEZONE = 3)
		md = date + datetime.timedelta(TIMEZONE = 3)
		await ctx.channel.send("Принято: сообщение \"{}\" будет отправлено {}.".format(text, md.strftime("%d.%m.%Y в %H:%M")))
		self.bot.timer_manager.create_timer("reminder", date, args=(ctx.channel.id, mf.strftime("%d.%m.%Y %H:%M"), ctx.author, text))


	@commands.Cog.listener()
	async def on_reminder(self, channel_id, date, author, text):
		channel = self.bot.get_channel(channel_id)
		await channel.send("{}, твоё напоминание от {} : {}".format(author.mention, date, text))
		
	@commands.Cog.listener()
	@remind.error
	async def remind_error(self, ctx, error):
		if isinstance(error, commands.MissingRequiredArgument):
			await ctx.send('***Формат записи - !remind [число часов (поддерживаются дроби)] [напоминание]***')
		if isinstance(error,commands.BadFrgument):
			await ctx.send('***Формат записи - !remind [число часов (поддерживаются дроби)] [напоминание]***')


def setup(bot):
	bot.add_cog(Remind(bot))
