# Botとして動かすためのいろいろ。
# 起動とかコマンドとか。
import os
import re
import discord
from discord import app_commands
from discord.ui import Select, ChannelSelect, View
import datetime
from dotenv import load_dotenv
from core import secretaryCalendarCore as scc
from core import secretaryReactCore as src

load_dotenv()
TOKEN=os.getenv("DISCORD_TOKEN")

rem = scc.Reminder()
client = rem.client
tree = app_commands.CommandTree(client)

def str2dt(text:str):
    """
    YYYY/MM/DD/HH/MMなどのstrをdatetimeに変換する。
    出力はdatetime。
    年月日等の区切りは数字でなければなんでもOK。
    2025/12/25 12:00
    2025 12 25 12 00
    2025年12月25日12時00分
    """
    l = []
    while re.match(r'\D',text[-1]):
        text = text[:-2]
    for e in re.split(r"\D", text):
        if e != "":
            l.append(int(e))
    dt = datetime.datetime(*l, microsecond=0)
    return dt

class selectRemindView(View):
    @discord.ui.select(
        cls=Select,
        placeholder="",
        options=[
            discord.SelectOption(label="このチャンネル",value='ch',description="このチャンネルでリマインド"),
            discord.SelectOption(label="DM",value='dm',description="DMでリマインド")
            ]
    )
    async def selectMenu(self, ctx: discord.Interaction, select: Select):
        await ctx.response.send_message("送信先を決定しました。", ephemeral=True)
        if select.values[0] == 'ch':
            await rem.configAddres(typeInput="ch",addres=ctx.channel_id)
        else:
            await rem.configAddres(typeInput="dm", addres=ctx.user)
class selectTalkView(View):
    @discord.ui.select(
        cls=ChannelSelect
    )
    async def selectMenu(self, ctx: discord.Interaction, select: Select):
        src.React.reactCh = (select.values[0]).id
        await ctx.response.send_message("送信先を決定しました。", ephemeral=True)
@tree.command(name="test",description="テストコマンドです。")
@app_commands.describe(
    text="Text to say hello." # 引数名=説明
)
async def test_command(ctx: discord.Interaction, text:str):
    channel = client.get_channel(src.React.reactCh)
    await channel.send(f"てすと！\nprovided word: {text}")#ephemeral=True→「これらはあなただけに表示されています」
    return
@tree.command(name="t", description="圧縮して設定を更新")
async def t(ctx: discord.Interaction):
    await rem.configAddres(typeInput="ch",addres=ctx.channel_id)
    rem.add_event(name="test", date_time=str2dt("2026/01/01"))
    await ctx.response.send_message("このチャンネルにてテストします。\nテスト用イベントの詳細: test,2026/01/01", ephemeral=True)
    return
@tree.command(name="displayconfig",description="設定を見せる")
async def command_displayconfig(ctx: discord.Interaction):
    await ctx.response.send_message(f"{rem.schedule}\n\n{rem.addres}",ephemeral=True)
    return
#ここからbotのメイン機能たち
@tree.command(name="configremind", description="リマインドの送信先を設定をします。")
async def command_configremind(ctx: discord.Interaction):
    view = selectRemindView()
    await ctx.response.send_message("リマインドの送信場所を設定", view=view, ephemeral=True)
    return
@tree.command(name="configtalk", description="会話の場所を設定をします。")
async def command_configtalk(ctx: discord.Interaction):
    view = selectTalkView()
    await ctx.response.send_message("リマインドの送信場所を設定", view=view, ephemeral=True)
    return
@tree.command(name="add_event",description="用事を登録します。")
@app_commands.describe(name="用事の名前(必須)")
@app_commands.describe(date= "予定の日時")
@app_commands.describe(location="用事がある場所")
@app_commands.describe(items="持ち物")
@app_commands.describe(repeat="繰り返しの頻度")
@app_commands.describe(message="リマインドの際に表示する文言")
@app_commands.choices(
    repeat=[
        app_commands.Choice(name="繰り返さない",value="None"),
        app_commands.Choice(name="毎日",value="daily"),
        app_commands.Choice(name="毎週",value="weekly"),
        app_commands.Choice(name="毎月",value="monthly"),
        app_commands.Choice(name="毎年",value="yearly")
        ]
)
async def command_addEvent(ctx: discord.Interaction, name:str, date:str, location:str=None, items:str=None, repeat:str=None, message:str=None):
    user = ctx.user.id
    dt = str2dt(date)
    rem.add_event(name=name, date_time=dt, location=location, items=items, repeat=repeat, message=message, user=user)
    embed = discord.Embed(title="予定を追加しました！", color=discord.Colour.green())
    embed.add_field(name="予定名", value=f"{name}", inline=False)
    embed.add_field(name="日時", value=f"{dt.strftime('%Y年%m月%d日 %H時%M分')}", inline=False)
    if location is not None:
        embed.add_field(name="場所", value=f"{location}", inline=False)
    if items is not None:
        embed.add_field(name="持ち物", value=f"{items}", inline=False)
    if repeat is not None:
        repeatList = {
        "daily":"毎日",
        "weekly":"毎週",
        "monthly":"毎月",
        "yearly":"毎年"
        }
        embed.add_field(name="繰り返し", value=f"{repeatList[repeat]}お知らせします。", inline=False)
    await ctx.response.send_message(content=f"<@{user}>\n",embed=embed,ephemeral=True)
    return
@tree.command(name="delete_event",description="用事を消します。")
@app_commands.describe(name="削除したい用事の名前")
@app_commands.describe(date="予定を開けたい日時")
async def command_deleteEvent(ctx: discord.Interaction, name:str=None, date:str=None):
    user = ctx.user.id
    name = dt = None
    if date is not None: dt = str2dt(date)
    deleted = rem.delete_event(name, dt)
    embed = discord.Embed(title=f"{len(deleted)}件の予定を削除しました！", color=discord.Colour.red())
    detail = ""
    for e in deleted:
        detail += f"* {e['name']}({e['date_time'].strftime('%Y年%m月%d日 %H時%M分')})\n"
    embed.add_field(name="削除した予定の詳細", value=f"{detail}", inline=False)
    await ctx.response.send_message(content=f"<@{user}>\n",embed=embed,ephemeral=True)
    return

@tree.command(name="update_event",description="用事の詳細を変更します。")
@app_commands.describe(old_name="変更したい予定の名前")
@app_commands.describe(old_date="変更したい予定の日付")
@app_commands.describe(new_name="変更後の用事の名前(必須)")
@app_commands.describe(new_location="変更後の用事がある場所")
@app_commands.describe(new_items="変更後の持ち物")
@app_commands.describe(new_repeat="変更後の繰り返しの頻度")
@app_commands.describe(new_message="変更後のリマインドの際に表示する文言")
@app_commands.describe(new_date= "変更後の予定の日時")
@app_commands.choices(
    new_repeat=[
        app_commands.Choice(name="繰り返さない",value="None"),
        app_commands.Choice(name="毎日",value="daily"),
        app_commands.Choice(name="毎週",value="weekly"),
        app_commands.Choice(name="毎月",value="monthly"),
        app_commands.Choice(name="毎年",value="yearly")
        ]
)
async def command_updateEvent(ctx: discord.Interaction, old_name:str, old_date:str,new_name:str, new_date:str, new_location:str=None, new_items:int=None, new_repeat:str=None, new_message:str=None):
    user = ctx.user.id
    old_date = str2dt(old_date)
    new_data = {
            "name": new_name,
            "date_time": str2dt(new_date),
            "location": new_location,
            "items": new_items,
            "repeat": new_repeat,
            "message": new_message,
            "user": user
        }
    a = rem.update_event(old_name=old_name, old_date=old_date, new_event_data=new_data)
    if a is not None:
        embed = discord.Embed(title=f"{old_name}({old_date.strftime('%Y年%m月%d日 %H時%M分')})を変更しました！")
        content = f"**予定名:** {new_name}\n"
        content += f"**日時:** {str2dt(new_date).strftime('%Y年%m月%d日 %H時%M分')}\n"
        if new_location is not None:
            content += f"**場所:** {new_location}\n"
        if new_items is not None:
            content += f"**持ち物:** {new_items}\n"
        if new_repeat is not None:
            repeatList = {
            "daily":"毎日",
            "weekly":"毎週",
            "monthly":"毎月",
            "yearly":"毎年"
            }
            content += f"**繰り返し:** {repeatList[new_repeat]}お知らせします。"

        embed.add_field(name="変更内容", value=f"{content}", inline=False)
        await ctx.response.send_message(content=f"<@{user}>", embed=embed,ephemeral=True)
    else:
        await ctx.response.send_message(content="予定の変更に失敗しました！\n入力内容をお確かめください。", ephemeral=True)
    return


@tree.command(name="list_events",description="予定一覧をリストとして取得します。")
@app_commands.describe(date="日付(任意)")
async def command_listEvents(ctx: discord.Interaction,date:str=None):
    user = ctx.user.id
    events = ""
    if date is not None:
        eventList = rem.list_events(date=str2dt(date))
        desc = f"# {str2dt(date).strftime('%Y年%m月%d日(%H時%M分)の予定一覧')}\n"

        for e in eventList:
            events += f"{e['name']}\n"
    else:
        desc = "# 予定一覧\n"
        eventList = rem.list_events()
        for e in eventList:
            events += f"{e['name']} ({e['date_time'].strftime('%Y年%m月%d日(%H時%M分)')})\n"
    await ctx.response.send_message(content=f"<@{user}>\n{desc}{events}",ephemeral=True)
    return

@tree.command(name="remind_after",description="指定した期間の後でリマインドします。")
@app_commands.describe(name="用事の名前(必須)")
@app_commands.describe(delay= "リマインドまでの長さ。\n単位は秒、分、時、日、週。")
@app_commands.describe(location= "予定の場所")
@app_commands.describe(items= "持ち物")
@app_commands.describe(message= "表示するメッセージ")
async def command_remindAfter(ctx: discord.Interaction, name:str, delay:str, location:str=None, items:str=None, message:str=None):
    user = ctx.user.id
    m = list((re.match(r"(\d+)\s*([a-zA-Z]+)",delay)).groups())
    timeUnit = {
        "s": "seconds",
        "m": "minutes",
        "h": "hours",
        "d": "days",
        "w": "weeks"
    }
    timeUnit2 = {
        "s": "秒",
        "m": "分",
        "h": "時間",
        "d": "日",
        "w": "週"
    }
    await ctx.response.send_message(f"{m[0]}{timeUnit2[m[1][0]]}後にリマインドします！", ephemeral=True)
    rem.remind_after(name=name,delay_amount=int(m[0]),delay_unit=timeUnit[m[1][0]],location=location,items=items,message=message,user=user)

#@tree.command(name="reportjob",description="進捗を報告します。")
#async def command_reportJob(ctx: discord.Interaction, jobSumary:str, selfEvaluation:str):
#    await src.React()
#コマンドここまで
@client.event
async def on_ready():
    print("起動完了")
    await tree.sync()#スラッシュコマンドを同期
    rem.start_reminder_loop()

client.run(TOKEN)
