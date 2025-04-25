# Botとして動かすためのいろいろ。
# 起動とかコマンドの読み込みとか。
import discord
from discord.ext import commands, tasks
from discord import app_commands
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN=os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

@tree.command(name="test",description="テストコマンドです。")
async def test_command(interaction: discord.Interaction):
    await interaction.response.send_message("てすと！",ephemeral=True)#ephemeral=True→「これらはあなただけに表示されています」

@client.event
async def on_ready():
    print("起動完了")
    await tree.sync()#スラッシュコマンドを同期

client.run(TOKEN)