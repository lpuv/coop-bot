import discord
from discord.ext import commands
import datetime

from urllib import parse, request
import re, os

bot = commands.Bot(command_prefix='!', description="This is a Helper Bot")

@bot.command()
async def ping(ctx):
    await ctx.send('pong')

@bot.command()
async def setupChamberList(ctx, pastebin):
    await ctx.send(f'setting the chamber list to {pastebin}...')
    bot_data = shelve.open("bot_data")
    #import requests

    response = requests.get(f'https://pastebin.com/raw/{pastebin}')

    bot_data['chamber-list'] = response.content.decode('ascii').replace('\r', '').split('\n')
    bot_data.close()

# Events
@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name="Watching Cooperation Conundrum"))
    print('My Ready is Body')


@bot.listen()
async def on_message(message):
    #if "tutorial" in message.content.lower():
        # in this case don't respond with the word "Tutorial" or you will call the on_message event recursively
    await bot.process_commands(message)

bot.run(os.environ['TOKEN'])
