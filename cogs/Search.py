import discord
import asyncio
from discord.ext import commands

class Search(commands.Cog):
	
	def __init__(self, bot):
		self.bot = bot


	@commands.command()
	async def ytsearch(self, ctx, *, text):
		command = text.replace(" ", "+")
		await ctx.send('Youtube: https://www.youtube.com/results?search_query=' + command)

def setup(bot):
	bot.add_cog(Search(bot))
