import discord
from discord.ext import commands
import datetime, requests

from urllib import parse, request
import re, os

bot = commands.Bot(command_prefix='$', description="Cooperation Conundrum Bot")

import psycopg2
import urllib.parse as urlparse
import os

url = urlparse.urlparse(os.environ['DATABASE_URL'])
dbname = url.path[1:]
user = url.username
password = url.password
host = url.hostname
port = url.port

con = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host,
            port=port
            )

#con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

@bot.command()
async def ping(ctx):
    await ctx.send('pong')

@bot.command()
async def setupChamberList(ctx, pastebin):
    await ctx.send(f'setting the chamber list to {pastebin}...')
#    bot_data = shelve.open("bot_data")
    #import requests

    response = requests.get(f'https://pastebin.com/raw/{pastebin}')

#    os.unlink('chamber-list.txt')
#    os.unlink('current-chamber.txt')
    #chamber_list = open('chamber-list.txt', 'w')


    chamber_list_array = response.content.decode('ascii').replace('\r', '').split('\n')
    current_chamber = chamber_list_array[0]
    #current_chamber_file = open('current-chamber.txt', 'w')
    #current_chamber_file.write(current_chamber)
    cur = con.cursor()
    cur.execute('DELETE FROM CHAMBERS;')
    cur.execute('DELETE FROM CURRENTCHAMBER;')
    for i in range(chamber_list_array):
        cur.execute(f'INSERT INTO CHAMBERS (index, chamber) VALUES ({i}, {chamber_list_array[i]});')
    cur.execute(f'INSERT INTO CURRENTCHAMBER (index) VALUES (0);')
    con.commit()
    await ctx.send("Done!")
#bot_data.close()

@bot.command()
async def nextChamber(ctx):
   await ctx.send("Advancing to next chamber...")
   #file = open('current-chamber.txt', 'r')
   #current_chamber = file.readline()
   #file.close()
#os.unlink('currrent-chamber.txt')
   cur = con.cursor()
   cur.execute('SELECT NAME FROM CHAMBERS;')
   chambers = cur.fetchall()
   #file = open('chamber-list.txt', 'r')
   #for chamber in file:
   #    chambers.append(file.readline())

   cur.execute('SELECT INDEX FROM CURRENTCHAMBER;')
   currentchamber = cur.fetchall() + 1
   cur.execute('DELETE FROM CURRENTCHAMBER;')
   cur.commit()
   cur.execute(f'INSERT INTO CURRENTCHAMBER (index) VALUES ({currentchamber});')
   cur.commit()
#   os.unlink('current-chamber.txt')
   #file = open('current-chamber.txt', 'w')
   #file.write(current_chamber)

# Events
@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name="Watching Cooperation Conundrum"))
    print('My Ready is Body')
    cursor = con.cursor()
    cursor.execute('CREATE TABLE IF NOT EXIST CHAMBERS (INDEX INT PRIMARY KEY NOT NULL, NAME VARCHAR(255) NOT NULL);')
    cursor.execute('CREATE TABLE IF NOT EXIST CURRENTCHAMBER (INDEX INT NOT NULL);')
    con.commit()


bot.run(os.environ['TOKEN'])
