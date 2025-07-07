import discord
from dotenv import load_dotenv
import os
import json

file = "configLog.json"

load_dotenv()
TOKEN=os.getenv("DISCORD_TOKEN")
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
intents.dm_messages = True
client = discord.Client(intents=intents)
configdata = {
    "calender": {
        "schedule": {},
        "addres": 0,
        "addresType": "dm"
    },
    "react": {
        "reactCh": None
    }
}
def backupConfig(data:any, category=None, name=None):
    if category is None: return "error"
    if name is None:
        configdata[category] = data
    else:
        configdata[category][name] = data
    with open(file, "w", encoding="utf-8") as f:
        json.dump(configdata, f, indent=2, ensure_ascii=False)

def loadBackup():
    with open(file, "r", encoding="utf-8") as f:
        data = json.load()
    return data