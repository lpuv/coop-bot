import discord
from discord.ext import commands
import datetime

from urllib import parse, request
import re, os

bot = commands.Bot(command_prefix='$', description="Cooperation Conundrum Bot")

@bot.command()
async def ping(ctx):
    await ctx.send('pong')

@bot.command()
async def setupChamberList(ctx, pastebin):
    await ctx.send(f'setting the chamber list to {pastebin}...')
#    bot_data = shelve.open("bot_data")
    #import requests

    response = requests.get(f'https://pastebin.com/raw/{pastebin}')

    os.unlink('chamber-list.txt')
    os.unlink('current-chamber.txt')
    chamber_list = open('chamber-list.txt', 'w')


    chamber-list-array = response.content.decode('ascii').replace('\r', '').split('\n')
    current_chamber = chamber-list-array[0]
    current_chamber_file = open('current-chamber.txt', 'w')
    current_chamber_file.write(current_chamber)
    for chamber in chamber-list-array:
        chamber_list.write(chamber)
    chamber_list.close()
#bot_data.close()

@bot.command()
async def nextChamber(ctx):
   await ctx.send("Advancing to next chamber...")
   file = open('current-chamber.txt', 'r')
   current_chamber = file.readline()
   file.close()
#os.unlink('currrent-chamber.txt')

   chambers = []
   file = open('chamber-list.txt', 'r')
   for chamber in file:
       chambers.append(file.readline())

   current_chamber = chambers[chambers.index(current_chamber) + 1]
   os.unlink('current-chamber.txt')
   file = open('current-chamber.txt', 'w')
   file.write(current_chamber)

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
