import discord
from discord.ext import commands

class Help(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command()
	async def help(self, ctx):
		embed = discord.Embed(title='Помощь', description='Список команд', colour=discord.Color.red(), url='https://discordapp.com/api/oauth2/authorize?client_id=599168929222361088&permissions=8&scope=bot')

		embed.set_author(name='Список команд', icon_url=ctx.author.avatar_url)

		embed.add_field(name='Пользовательские', value='help, userinfo, roleinfo, diceinfo, giverole, diceup, dicedown, level, echo(say)')
		embed.add_field(name='Модераторские', value='kick, clear, reload')
		embed.add_field(name='Администраторские', value='ban, addmoney, addexp, addlvl')

		await ctx.send(embed=embed)

	@commands.command()
	async def roleinfo(self, ctx):
		embed = discord.Embed(color=discord.Color.red())

		embed.set_author(name='Список ролей', icon_url=ctx.author.avatar_url)

		embed.add_field(name='Role lvl 2', value='может быть получена на 10 уровне, лишает роли Start role.', inline=False)
		embed.add_field(name='Role lvl 3', value='может быть получена на 20 уровне, позволяет создавать и удалять каналы.', inline=False)
		embed.add_field(name='Role lvl 4', value='может быть получена на 30 уровне, роль делает участника полноценным модератором.', inline=False)
		embed.add_field(name='Внимание', value='запрещается флудить, с целью повышения уровня.', inline=False)

		await ctx.send(embed=embed)

	@commands.command()
	async def diceinfo(self, ctx):
		embed = discord.Embed(color=discord.Color.red())

		embed.set_author(name='Правила Dice', icon_url=ctx.author.avatar_url)

		embed.add_field(name='!diceup N', value='Используя данную команду, вы ставите N своих крышек на то, что случайно выбраное ботом число будет ***больше*** 50. Если вы угадываете, то получаете на свой счёт в 2 раза больше, чем поставили. В противном случае, вы теряете N крышек.', inline=False)
		embed.add_field(name='!dicedown N', value='Используя данную команду, вы ставите N своих крышек на то, что случайно выбраное ботом число будет ***меньше*** 50. Если вы угадываете, то получаете на свой счёт в 2 раза больше, чем поставили. В противном случае, вы теряете N крышек.', inline=False)
		embed.add_field(name='Штраф', value='Если выпадает число 50, вы получаете штраф N в пятикратном размере.', inline=False)
		embed.add_field(name='Особый выигрыш', value='Если выпадает число 0 или 100, вы получаете N в десятикратном размере.', inline=False)

		await ctx.send(embed=embed)

	@commands.command()
	async def shop(self, ctx):
		embed = discord.Embed(color=discord.Color.green())

		embed.set_author(name='Магазин ролей', icon_url=ctx.author.avatar_url)

		embed.add_field(name='Майнкрафт моя жызнь', value='250 крышек. Роль поможет подчеркнуть вашу индивидуальность. (1)')
		embed.add_field(name='20 см', value='500 крышек. Благодаря этой роли, все поймут, что вы пиздабол. (2)')
		embed.add_field(name='Ярость Любы', value='1000 крышек. Ибо нехуй. (3)')
		embed.add_field(name='Mod', value='2000 крышек. Данная роль наделяет владельца правами модератора (4)')
		embed.add_field(name='Внимание', value='Цифра в скобках, индивидуальный номер для покупки роли.')

		await ctx.send(embed=embed)

	@commands.command()
	async def donate(self, ctx):
		embed = discord.Embed(color=discord.Color.green())

		embed.set_author(name='Магазин ролей', icon_url=ctx.author.avatar_url)

		embed.add_field(name='100 крышек', value='10 рублей')
		embed.add_field(name='10 опыта', value='5 рублей')
		embed.add_field(name='1 уровень', value='20 рублей')
		embed.add_field(name='Роль модератора', value='Отсосать у админа')
		embed.add_field(name='Обращаться', value='L0L1K#9280.')

		await ctx.send(embed=embed)




def setup(bot):
	bot.add_cog(Help(bot))
