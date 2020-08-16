import discord
from discord.ext import commands
from discord.utils import get
import youtube_dl
import os
import shutil
import asyncio

class Music(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	queues = {}

	@commands.command(pass_context=True, aliases=['j', 'joi'])
	async def join(self, ctx):
	    global voice
	    channel = ctx.message.author.voice.channel
	    voice = get(self.bot.voice_clients, guild=ctx.guild)

	    if voice and voice.is_connected():
	        await voice.move_to(channel)
	    else:
	        voice = await channel.connect()

	    await voice.disconnect()

	    if voice and voice.is_connected():
	        await voice.move_to(channel)
	    else:
	        voice = await channel.connect()

	    await ctx.send(f"Подключение к каналу ***{channel}***")


	@commands.command(pass_context=True, aliases=['l', 'lea'])
	async def leave(self, ctx):
	    channel = ctx.message.author.voice.channel
	    voice = get(self.bot.voice_clients, guild=ctx.guild)

	    if voice and voice.is_connected():
	        await voice.disconnect()
	        await ctx.send(f"Отключение от канала ***{channel}***")
	    else:
	        await ctx.send("Я не подключён ни к одному каналу")


	@commands.command(pass_context=True, aliases=['p', 'pla'])
	async def play(ctx, url):
        server = ctx.message.server
        voice_client = client.voice_client_in(server)
        player = await voice_client.create_ytdl_player(url)
        players[server.id] = player
        player.start()
        await ctx.send("Песня загружается...")


	

def setup(bot):
	bot.add_cog(Music(bot))