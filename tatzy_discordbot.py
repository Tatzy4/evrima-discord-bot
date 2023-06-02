import discord
from discord.ext import commands
import socket
import sys
import os
import asyncio

__author__ = "Tatzy"


ip = "ip here" # like 127.10.100.137
port = RCONPORT # like 8888
password = b"RCONpasswordHERE" 
timeout = 5
packetMainLength = 2

# Discord bot token
TOKEN = 'bot token here'

# Discord intents
intents = discord.Intents.default()
intents.typing = False
intents.presences = False

# Discord client
client = commands.Bot(command_prefix='!', intents=intents)

def cls():
    os.system('cls' if os.name == 'nt' else 'clear')

async def playerList():
    while True:
        cls()
        LIST = b'\x02@\x00'
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            # Connect to the TCP Socket
            s.settimeout(timeout)
            s.connect((ip, port))
            s.send(LIST)
            message = s.recv(1024)
            message_str = message.decode()
            print("Server returned: " + message_str)

            # Extract player names from the message
            player_names = [name.strip() for name in message_str.split(",") if name.strip()]
            print("Player names: " + ", ".join(player_names))

            # Count the number of players
            player_count = len(player_names)
            print("Number of players: " + str(player_count))

            # Update Discord bot status
            update_status(player_count)

        await asyncio.sleep(60)  # Wait for 1 minute

def connect():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # Connect to the TCP Socket
        s.settimeout(timeout)
        s.connect((ip, port))
        print("TCP connection established with server")
        # Form our login Packet
        payload = b'\x01' + password + b'\x00'
        print("Sending: " + str(payload) + "\n")
        s.send(payload)
        message = s.recv(1024)
        if "Accepted" in message.decode():
            print(message)
        else:
            print(message)
            sys.exit()
        playerListTask = asyncio.create_task(playerList())
        asyncio.get_event_loop().run_until_complete(playerListTask)

def update_status(player_count):
    game = discord.Game(name=f"Gracze: {player_count}")
    client.loop.create_task(client.change_presence(activity=game))

@client.event
async def on_ready():
    print(f'Logged in as {client.user.name} ({client.user.id})')
    print('------')
    print('see errors? hit tatzy#2190')
    await playerList()

client.run(TOKEN)
