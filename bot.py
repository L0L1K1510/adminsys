import discord
from discord.ext import commands

import urllib.parse, urllib.request, re

import logging
import random
import datetime
import asyncio
import os

#Log
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

bot = commands.Bot(command_prefix='!')
bot.remove_command('help')
TOKEN = open('TOKEN.txt', 'r').read()

@bot.event
async def on_ready():
	print('Bot online...')
	print(bot.user.name)
	print('--------------')

#AutoRole
@bot.event
async def on_member_join(member):
	role = discord.utils.get(member.guild.roles, name='Куда сдавать бутылки?')
	await member.add_roles(role)


@bot.command(aliases=['say'])
async def echo(ctx, *, words: commands.clean_content):
	await ctx.send(words)


		
#Testembed
@bot.command()
async def testembed(ctx):
	embed = discord.Embed(title='Title', description='Description', colour=discord.Color.red(), url='https://www.google.com')

	embed.set_author(name=bot.user.name, icon_url=bot.user.avatar_url)
	embed.set_footer(text=ctx.author.name, icon_url=ctx.author.avatar_url)
	embed.set_image(url='https://discordpy.readthedocs.io/en/latest/_images/snake.png')
	embed.set_thumbnail(url='https://www.python.org/static/img/python-logo.png')

	embed.add_field(name='Field 1', value='value 1')
	embed.add_field(name='Field 2', value='value 2')

	embed.add_field(name='Field 3', value='value 3', inline=False)
	embed.add_field(name='Field 4', value='value 4')

	await ctx.send(embed=embed)



#Status
async def chng_pr():
	await bot.wait_until_ready()

	statuses = ['!help', 'http://b92103ya.beget.tech/']

	while not bot.is_closed():
		status = random.choice(statuses)

		await bot.change_presence(activity=discord.Game(status))

		await asyncio.sleep(20)


#Cogs
for cog in os.listdir(".//cogs"):
	if cog.endswith(".py"):
		try:
			cog = f"cogs.{cog.replace('.py', '')}"
			bot.load_extension(cog)
		except Exception as e:
			print(f"{cog} не может быть запущен:")
			raise e


bot.loop.create_task(chng_pr())
bot.run('TOKEN')
