import discord
from dotenv import load_dotenv
import os

load_dotenv()
TOKEN=os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
intents.dm_messages = True
client = discord.Client(intents=intents)