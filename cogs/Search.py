import discord
import asyncio
from discord.ext import commands

import urllib
import pprint
import json
import httplib2

class Search(commands.Cog):
	
	def __init__(self, bot):
		self.bot = bot


	@commands.command()
	async def ggsearch(self, ctx, *, text):
		url = "http://ajax.googleapis.com/ajax/services/search/web?v=1.0&" + \
		urllib.urlencode({'q':query});
		referer = "http://wikipedia.org"
		h = httplib2.Http({})
		resp, content = h.request(url, "GET", headers={'Referer': referer})
		if resp.status == 200: pprint.pprint( json.loads(content) )
		else: print('Error')

def setup(bot):
	bot.add_cog(Search(bot))
