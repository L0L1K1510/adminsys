import discord
from discord.ext import commands

from random import randint

import json
import asyncio

class Mod(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command()
	@commands.has_permissions(kick_members=True)
	async def kick(self, ctx, member: discord.Member, *, reason="Без причины"):
		await member.kick(reason=reason)
		await ctx.send(f'{member.mention} был кикнут модератором {ctx.author.mention}. Причина: {reason}.')

	@commands.command()
	@commands.has_permissions(ban_members=True)
	async def ban(self, ctx, member: discord.Member, *, reason="Без причины"):
		await member.ban(reason=reason)
		await ctx.send(f'{member.mention} был забанен администратором {ctx.author.mention}. Причина: {reason}.')

	@commands.command()
	@commands.has_permissions(manage_messages=True)
	async def clear(self, ctx, amount: int):
		await ctx.channel.purge(limit=amount + 1)
		await ctx.send(f'{amount} сообщений было удалено.')

	@commands.command()
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


	@commands.Cog.listener()
	@clear.error
	async def clear_error(self, ctx, error):
		if isinstance(error, commands.CheckFailure):
			await ctx.send('***Вы не имеете права это использовать!***')
		if isinstance(error, commands.MissingRequiredArgument):
			await ctx.send('***Введите количество сообщений.***')
		if isinstance(error,commands.BadFrgument):
			await ctx.send('***Количеством сообщений может быть только целое число!***')

	@commands.Cog.listener()
	@kick.error
	async def kick_error(self, ctx, error):
		if isinstance(error, commands.CheckFailure):
			await ctx.send('***Вы не имеете права это использовать!***')
		if isinstance(error, commands.MissingRequiredArgument):
			await ctx.send('***Неверно введена команда (!kick @nick#0000 reason)!***')
		if isinstance(error,commands.BadFrgument):
			await ctx.send('***Неверно введена команда (!kick @nick#0000 reason)!***')

	@commands.Cog.listener()
	@ban.error
	async def ban_error(self, ctx, error):
		if isinstance(error, commands.CheckFailure):
			await ctx.send('***Вы не имеете права это использовать!***')
		if isinstance(error, commands.MissingRequiredArgument):
			await ctx.send('***Неверно введена команда (!ban @nick#0000 reason)!***')
		if isinstance(error,commands.BadFrgument):
			await ctx.send('***Неверно введена команда (!ban @nick#0000 reason)!***')


		raise error



		
def setup(bot):
	bot.add_cog(Mod(bot))