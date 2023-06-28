import discord
from discord.ext import commands
import socket
import sys
import os
import asyncio
import configparser

__author__ = "tatzy"

# Discord intents
intents = discord.Intents.default()
intents.typing = False
intents.presences = False

# Discord client
client = commands.Bot(command_prefix='!', intents=intents)

config = configparser.ConfigParser()
config.read('config.ini')

ip = config.get('Server', 'ip')
port = int(config.get('Server', 'port'))
password = config.get('Server', 'password').encode()
timeout = int(config.get('Server', 'timeout'))
packetMainLength = int(config.get('Server', 'packetMainLength'))
prefixText = config.get('Discord', 'prefixText')
serverSlots = config.get('Discord', 'serverSlots')
TOKEN = config.get('Discord', 'token')

def cls():
    os.system('cls' if os.name == 'nt' else 'clear')

def playerList():
    cls()
    LIST = b'\x02@\x00'
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # Connect to the TCP Socket
        s.settimeout(timeout)
        s.connect((ip, port))
        s.send(LIST)
        message = s.recv(10192)
        message_str = message.decode()
        print("Server returned: " + message_str)

        # Extract player names from the message
        player_names = []
        count_next = False
        for name in message_str.split(","):
            name = name.strip()
            if name and count_next:
                player_names.append(name)
            count_next = not count_next

        print("Player names: " + ", ".join(player_names))

        # Count the number of players
        player_count = len(player_names)
        print("Number of players: " + str(player_count))

        # Update Discord bot status
        update_status(player_count)

async def connect_and_run():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # Connect to the TCP Socket
        s.settimeout(timeout)
        s.connect((ip, port))
        print("TCP connection established with server")
        # Form our login Packet
        payload = b'\x01' + password + b'\x00'
        print("Sending: " + str(payload) + "\n")
        s.send(payload)
        message = s.recv(10192)
        if "Accepted" in message.decode():
            print(message)
        else:
            print(message)
            sys.exit()

    while True:
        playerList()
        await asyncio.sleep(60)  # Wait for 1 minute

def update_status(player_count):
    game = discord.Game(name=f"{prefixText} {player_count}/{serverSlots}")
    client.loop.create_task(client.change_presence(activity=game))

@client.event
async def on_ready():
    print(f'if errors hit tatzy#2190')
    client.loop.create_task(connect_and_run())

client.run(TOKEN)
