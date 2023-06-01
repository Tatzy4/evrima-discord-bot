__author__ = "Tatzy"

import discord
from discord.ext import tasks
import socket

ip = "99.99.99.99" #ur server ip here
port = 88888 #ur rcon port here
password = b"RCONpassword" #ur rcon password here
timeout = 5
packetMainLength = 2

intents = discord.Intents.default()
intents.presences = True
intents.guilds = True

client = discord.Client(intents=intents)

@tasks.loop(seconds=60)  # Update every 60 seconds
async def update_status():
    player_count = getPlayerCount()
    await client.change_presence(activity=discord.Game(name=f"Players: {player_count}")) # u can modify that by adding "Players: {player_count}/ur server max" and the players u can also change

def getPlayerCount():
    LIST = bytes('\x02', 'utf-8') + bytes('\x40', 'utf-8') + bytes('\x00', 'utf-8')

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(timeout)
        s.connect((ip, port))
        s.send(LIST)
        message = s.recv(1024)
        player_data = message.decode().split('\n')
        player_count = len(player_data) - 1
        return player_count

@client.event
async def on_ready():
    print(f"Logged in as {client.user.name}")
    update_status.start()

client.run("bot token here")

print("Tatzy")
