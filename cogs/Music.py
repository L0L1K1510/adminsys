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

	players = {}

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
	async def play(ctx, url : str):
		song_there = os.path.isfile('song.mp3')
		
		try:
			if song_there:
				os.remove('song.mp3')
				print('[Music] Старый файл удалён')
		except PermissionError:
			print('[Music] Файл не найдён')
			
		await ctx.send('Песня загружается...')
		
		voice = get(self.bot.voice_clients, guild = ctx.guild)
		
		ydl_opts = {
			'format' : 'bestaudio/best',
			'postprocessors' : [{
				'key' : 'FFmpegExtractAudio',
				'preferredcodec' : 'mp3',
				'preferredquality' : '192'
			}],
		}
		
		with youtube_dl.YoutubeDL(ydl_opts) as ydl:
			print('[Music] Загрузка...')
			ydl.download([url])
			
		for file in os.listdir('./'):
			if file.endswith('.mp3'):
				name = file
				print(f'[Music] Переименование файла: {file}')
				os.rename(file, 'song.mp3')
				
		voice.play(discord.FFmpegPCMAudio('song.mp3'), after = lambda e: print(f'[Music] {name}, музыка закончила проигрывание'))
		voice.source = discord.PCMVolumeTransformer(voice.source)
		voice.source.volume = 0.05
		
		song_name = name.rsplit('-', 2)
		await ctx.send(f'Сейчас играет: {song_name[0]}')
		
		


	

def setup(bot):
	bot.add_cog(Music(bot))
