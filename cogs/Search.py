import discord
import asyncio
import json
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
		print(content.read().decode())
		f = open('result.txt', 'w')
		f.write(str(content.read().decode()))
		f.close()
		
		f = open("result.txt", "r", encoding="utf-8").read()
		js = f.split("\n")[0].split("=", 1)[1][:-1]
		j_res = json.loads(js)
		f.close()
		result = re.findall(r'videoId\":\"...........', j_res)
		for res in result:
			res = res[9: ]
		print(result)
		await ctx.send('https://www.youtube.com/watch?v=' + result[0])

def setup(bot):
	bot.add_cog(Search(bot))
