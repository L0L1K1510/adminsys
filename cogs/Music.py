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
			print(f"Присоединяется к каналу {channel}\n")

		await ctx.send(f"Присоединяется к каналу {channel}")


	@commands.command(pass_context=True, aliases=['l', 'lea'])
	async def leave(self, ctx):
		channel = ctx.message.author.voice.channel
		voice = get(self.bot.voice_clients, guild=ctx.guild)

		if voice and voice.is_connected():
			await voice.disconnect()
			print(f"Покидает канал {channel}")
			await ctx.send(f"Покидает канал {channel}")
		else:
			print("Боту было сказано покинуть канал, но он не был в нём")
			await ctx.send("Невозможно покинуть канал, в котором бот не находится")


	@commands.command(pass_context=True, aliases=['p', 'pla'])
	async def play(self, ctx, url: str):

		def check_queue():
			Queue_infile = os.path.isdir("./Queue")
			if Queue_infile is True:
				DIR = os.path.abspath(os.path.realpath("Queue"))
				length = len(os.listdir(DIR))
				still_q = length - 1
				try:
					first_file = os.listdir(DIR)[0]
				except:
					print("Очередь пуста\n")
					self.queues.clear()
					return
				main_location = os.path.dirname(os.path.realpath(__file__))
				song_path = os.path.abspath(os.path.realpath("Queue") + "//" + first_file)
				if length != 0:
					print("Песня закончена, проигрывается следующая в очереди\n")
					print(f"Песен в очереди: {still_q}")
					song_there = os.path.isfile("song.mp3")
					if song_there:
						os.remove("song.mp3")
					filename = os.path.basename(song_path)
					dest = os.path.join(main_location,filename)
					shutil.move(song_path, dest)
					main_dir_list = os.listdir("./")
					print(main_dir_list)
					for file in os.listdir("./"):
						if file.endswith(".mp3"):
							os.rename(file, 'song.mp3')

					voice.play(discord.FFmpegPCMAudio("song.mp3"), after=lambda e: check_queue())
					voice.source = discord.PCMVolumeTransformer(voice.source)
					voice.source.volume = 0.07

				else:
					self.queues.clear()
					return

			else:
				self.queues.clear()
				print("Ни одной песни не было в очереди к концу предыдущей\n")



		song_there = os.path.isfile("song.mp3")
		try:
			if song_there:
				os.remove("song.mp3")
				self.queues.clear()
				print("Удаляем старый файл")
		except PermissionError:
			print("Попытка удалить файл песни, которая проигрывается в данный момент")
			await ctx.send("Ошибка: песня проигрывается в данный момент")
			return


		Queue_infile = os.path.isdir("./Queue")
		try:
			Queue_folder = "./Queue"
			if Queue_infile is True:
				print("Старая очередь удалена")
				shutil.rmtree(Queue_folder)
		except:
			print("Нет старых очередей")

		await ctx.send("Идёт подготовка")

		voice = get(self.bot.voice_clients, guild=ctx.guild)

		ydl_opts = {
			'format': 'bestaudio/best',
			'quiet': True,
			'postprocessors': [{
				'key': 'FFmpegExtractAudio',
				'preferredcodec': 'mp3',
				'preferredquality': '192',
			}],
		}
		try:
			with youtube_dl.YoutubeDL(ydl_opts) as ydl:
				print("Музыка загружается...\n")
				ydl.download([url])
		except:
			print("Этой URL нет на Ютубе, ищем на Spotify...")
			c_path = os.path.dirname(os.path.realpath(__file__))
			system("spotdl -f " + '"' + c_path + '"' + " -s " + url)

		for file in os.listdir("./"):
			if file.endswith(".mp3"):
				name = file
				print(f"Переименован файл: {file}\n")
				os.rename(file, "song.mp3")

		voice.play(discord.FFmpegPCMAudio("song.mp3"), after=lambda e: check_queue())
		voice.source = discord.PCMVolumeTransformer(voice.source)
		voice.source.volume = 0.07

		nname = name.rsplit("-", 2)
		await ctx.send(f"Сейчас проигрывается: {nname[0]}")
		print("Проигрывается\n")


	@commands.command(pass_context=True, aliases=['pa', 'pau'])
	async def pause(self, ctx):

		voice = get(self.bot.voice_clients, guild=ctx.guild)

		if voice and voice.is_playing():
			print("Проигрывание приостановлено")
			voice.pause()
			await ctx.send("Пауза")
		else:
			print("Пауза невозможна, т.к. музыка не проигрывается")
			await ctx.send("Пауза невозможна, т.к. в данный момент музыка не проигрывается")


	@commands.command(pass_context=True, aliases=['r', 'res'])
	async def resume(self, ctx):

		voice = get(self.bot.voice_clients, guild=ctx.guild)

		if voice and voice.is_paused():
			print("Возобновление")
			voice.resume()
			await ctx.send("Возобновление")
		else:
			print("Нечего возобновлять")
			await ctx.send("Нечего возобновлять")


	@commands.command(pass_context=True, aliases=['s', 'sto'])
	async def stop(self, ctx):
		voice = get(self.bot.voice_clients, guild=ctx.guild)

		self.queues.clear()

		queue_infile = os.path.isdir("./Queue")
		if queue_infile is True:
			shutil.rmtree("./Queue")

		if voice and voice.is_playing():
			print("Проигрывание остановлено")
			voice.stop()
			await ctx.send("Проигрывание остановлено")
		else:
			print("Остановка невозможна, т.к. музыка не проигрывается")
			await ctx.send("Остановка невозможна, т.к. музыка не проигрывается")

	queues = {}

	@commands.command(pass_context=True, aliases=['q', 'que'])
	async def queue(self, ctx, url: str):
		Queue_infile = os.path.isdir("./Queue")
		if Queue_infile is False:
			os.mkdir("Queue")
		DIR = os.path.abspath(os.path.realpath("Queue"))
		q_num = len(os.listdir(DIR))
		q_num += 1
		add_queue = True
		while add_queue:
			if q_num in self.queues:
				q_num += 1
			else:
				add_queue = False
				self.queues[q_num] = q_num

		queue_path = os.path.abspath(os.path.realpath("Queue") + f"/song{q_num}.%(ext)s")

		ydl_opts = {
			'format': 'bestaudio/best',
			'quiet': True,
			'outtmpl': queue_path,
			'postprocessors': [{
				'key': 'FFmpegExtractAudio',
				'preferredcodec': 'mp3',
				'preferredquality': '192',
			}],
		}
		try:
			with youtube_dl.YoutubeDL(ydl_opts) as ydl:
				print("Загружается аудио...\n")
				ydl.download([url])
		except:
			print("Этот URL не был найден на Youtube, ищем на Spotify...")
			q_path = os.path.abspath(os.path.realpath("Queue"))
			system(f"spotdl -ff song{q_num} -f " + '"' + q_path + '"' + " -s " + url)


		await ctx.send("Добавление " + str(q_num) + " в очередь")

		print("Песня добавлена в очередь\n")


	@commands.command(pass_context=True, aliases=['n', 'nex'])
	async def next(self, ctx):
		voice = get(self.bot.voice_clients, guild=ctx.guild)

		if voice and voice.is_playing():
			print("Следующая песня")
			voice.stop()
			await ctx.send("Следующая песня")
		else:
			print("Музыка не проигрывается в данный момент")
			await ctx.send("Ничего не проигрывается в данный момент")


	

def setup(bot):
	bot.add_cog(Music(bot))
