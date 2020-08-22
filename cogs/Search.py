import discord
import asyncio
from discord.ext import commands

import urllib, re

class Search(commands.Cog):
	
	def __init__(self, bot):
		self.bot = bot


	@commands.command()
	async def ytsearch(self, ctx, *, text):
		url = "https://www.youtube.com/results?" + \
		urllib.parse.urlencode({'search_query':text.replace(' ', '+')});
		content = urllib.request.urlopen(url)
		print(content.read().decode()))
		print(content)
		print(url)
		result = re.findall(r'v', str(content.read().decode()))
		#for res in result:
			#res = res[9: ]
		print(result)
		await ctx.send('https://www.youtube.com/watch?v=' + result[0])

def setup(bot):
	bot.add_cog(Search(bot))
