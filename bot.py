import discord
from discord.ext import commands

import random
import datetime
import asyncio
import os

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
	role = discord.utils.get(member.guild.roles, name='Start role')
	await member.add_roles(role)

#Chat
@bot.command()
async def ping(ctx):
	await ctx.send('Pong!')

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


@bot.command()
@commands.has_permissions(kick_members=True)
@commands.is_owner()
async def reload(ctx, cog):
	try:
		bot.unload_extension(f"cogs.{cog}")
		bot.load_extension(f"cogs.{cog}")
		await ctx.send(f"{cog} перезагружен.")
	except Exception as e:
		print(f"{cog} не может быть запущен:")
		raise e


#Userinfo
@bot.command()
async def userinfo(ctx, member: discord.Member = None):
	member = ctx.author if not member else member
	roles = [role for role in member.roles]

	embed = discord.Embed(colour=member.color, timestamp=ctx.message.created_at)

	embed.set_author(name=f'Информация о пользователе - {member}')
	embed.set_thumbnail(url=member.avatar_url)
	embed.set_footer(text=f'Запросил информацию - {ctx.author}', icon_url=ctx.author.avatar_url)

	embed.add_field(name='ID:', value=member.id)
	embed.add_field(name='Ник:', value=member.display_name)

	embed.add_field(name='Создал аккаунт:', value=member.created_at.strftime('%d.%m.%Y'))
	embed.add_field(name='Присоединился:', value=member.joined_at.strftime('%d.%m.%Y'))

	embed.add_field(name=f'Роли ({len(roles)})', value=' '.join([role.mention for role in roles]))
	embed.add_field(name='Наилучшая роль:', value=member.top_role.mention)

	embed.add_field(name='Bot?', value=member.bot)

	await ctx.send(embed=embed)

#Status
async def chng_pr():
	await bot.wait_until_ready()

	statuses = ['!help', 'site']

	while not bot.is_closed():
		status = random.choice(statuses)

		await bot.change_presence(activity=discord.Game(status))

		await asyncio.sleep(20)


#Cogs
for cog in os.listdir(".\\cogs"):
	if cog.endswith(".py"):
		try:
			cog = f"cogs.{cog.replace('.py', '')}"
			bot.load_extension(cog)
		except Exception as e:
			print(f"{cog} не может быть запущен:")
			raise e


bot.loop.create_task(chng_pr())
bot.run(TOKEN)