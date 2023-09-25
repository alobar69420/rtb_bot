import os
import discord
from dotenv import load_dotenv
from discord.ext import commands
from RealTimeBillionaires import ForbesRTB
from RTBDataFormatter import RTBDataFormatter

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

TEST_SERVER_CHAN = 1155219310848004197
SKYPE_SERVER_EDS_CHAN = 1115510691739217920

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

rtb_source = ForbesRTB()
rtb_formatter = RTBDataFormatter(rtb_source)

def is_allowed_channel():
	allowed_channels = [TEST_SERVER_CHAN, SKYPE_SERVER_EDS_CHAN]
	async def predicate(ctx):
		return ctx.channel.id in allowed_channels
	return commands.check(predicate)

@bot.event
async def on_ready():
	print(f'{bot.user.name} has connected to Discord!')


@bot.command(name='richlist', help='Responds with the top X people on Forbes Real Time Billionaires list')
@is_allowed_channel()
async def rich_list(ctx, num: int = 3):
	if num < 21:
		response = rtb_formatter.format_richlist(num)
	else:
		response = ':pinching_hand:'
	await ctx.send(response)

@bot.command(name='furious', help='Responds with how far Elon is up or down on #1, and who is furious about it')
@is_allowed_channel()
async def furios(ctx):
	response = rtb_formatter.format_furious()
	await ctx.send(response)

@bot.command(name='swong', help="Responds with daily swong of requested person")
@is_allowed_channel()
async def swong(ctx, *, name: str):
	response = rtb_formatter.format_swong(name)
	await ctx.send(response)

@bot.command(name='position', help="Responds with weath and position of requested person")
@is_allowed_channel()
async def position(ctx, *, name: str):
	response = rtb_formatter.format_position(name)
	await ctx.send(response)

# @bot.event
# async def on_command_error(ctx, error):
#     if isinstance(error, commands.errors.CheckFailure):
#         await ctx.send('I shit the bed, tell someone to clean it!')

bot.run(TOKEN)