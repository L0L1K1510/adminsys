import discord
from discord.ext import commands

class Events(commands.Cog):
	def __init__(self, bot):
		self.bot = bot


	@commands.Cog.listener()
	async def on_message(self, message):
		if message.author == self.bot.user:
			return

		user = message.author.name
		msg = message.content
		print(f"{user} said {msg}")


	@commands.Cog.listener()
	async def on_message_delete(self, message):
		await message.channel.send('***Сообщение удалено***')


	@commands.Cog.listener()
	async def on_command_error(self, ctx, error):
		if isinstance(error, commands.CheckFailure):
			await ctx.send('***Вы не имеете прав для использования этой команды!***')
		if isinstance(error, commands.CommandNotFound):
			await ctx.send('***Такой команды нет!***')

		raise error











def setup(bot):
	bot.add_cog(Events(bot))
