import discord
import datetime
import asyncio
from discord.ext import commands, timers

class Remind(commands.Cog):
   def __init__(self, bot):
      self.bot = bot
      self.bot.timer_manager = timers.TimerManager(self.bot)
        
  @bot.command()
  async def remind(ctx, time, *, text):
      msg_date = ctx.message.created_at
      date = msg_date + datetime.timedelta(hours = float(time))
      mf = msg_date + datetime.timedelta(hours = 3)  #костыли из-за часовых поясов
      md = date + datetime.timedelta(hours = 3)      #костыли из-за часовых поясов
      await ctx.channel.send("Принято: сообщение \"{}\" будет отправлено {}.".format(text, md.strftime("%d.%m.%Y в %H:%M")))
      self.bot.timer_manager.create_timer("reminder", date, args=(ctx.channel.id, mf.strftime("%d.%m.%Y %H:%M"), ctx.author, text))

    
  @bot.event
  async def on_reminder(channel_id, date, author, text):
      channel = self.bot.get_channel(channel_id)
      await channel.send("{}, твоё напоминание от {} : {}".format(author.mention, date, text))


def setup(bot):
	bot.add_cog(Remind(bot))
