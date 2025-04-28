# Botとして動かすためのいろいろ。
# 起動とかコマンドとか。
import discord
from discord.ext import commands, tasks
from discord import app_commands
import os
from dotenv import load_dotenv
from core import secretaryCalendarCore as scc

load_dotenv()
TOKEN=os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

rem = scc.Reminder()
rem.start_reminder_loop()


@tree.command(name="test",description="テストコマンドです。")
@app_commands.describe(
    text="Text to say hello." # 引数名=説明
)
async def test_command(interaction: discord.Interaction, text:str):
    await interaction.response.send_message(f"てすと！\nprovided word: {text}",ephemeral=True)#ephemeral=True→「これらはあなただけに表示されています」
@tree.command(name="add_event",description="用事を登録します。")
async def command_addEvent(interaction: discord.Interaction):
    user = interaction.user
    await rem.add_event()
@tree.command(name="delete_event",description="用事を消します。")
async def command_deleteEvent(interaction: discord.Interaction):
    return 0

@tree.command(name="update_event",description="用事の詳細を変更します。")
async def command_updateEvent(interaction: discord.Interaction):
    return 0
@tree.command(name="list_events",description="予定一覧をリストとして取得します。")
async def command_listEvents(interaction: discord.Interaction):
    return 0

@tree.command(name="display_events",description="予定一覧を表示します。")
async def command_displayEvents(interaction: discord.Interaction):
    return 0

@tree.command(name="start_reminder_loop",description="用事が見つかったらリマインドします。")
async def command_startReminderLoop(interaction: discord.Interaction):
    return 0

@tree.command(name="remind_after",description="指定した期間の後でリマインドします。")
async def command_remindAfter(interaction: discord.Interaction):
    return 0

@client.event
async def on_ready():
    print("起動完了")
    await tree.sync()#スラッシュコマンドを同期

client.run(TOKEN)