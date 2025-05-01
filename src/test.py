import os
import re
import datetime
from dotenv import load_dotenv
from core import secretaryCalendarCore as scc

rem = scc.Reminder()
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
    dt = datetime.datetime(*l)
    return dt

events = [
    ['name_01', '2025/1/1/0/0'],
    ['name_02', '2025/1/2/0/0'],
    ['name_03', '2025/1/3/0/0'],
    ['name_04', '2025/1/4/0/0'],
    ['name_05', '2025/1/5/0/0'],
    ['name_06', '2025/1/6/0/0'],
    ['name_07', '2025/1/7/0/0'],
    ['name_08', '2025/1/8/0/0'],
    ['name_09', '2025/1/9/0/0'],
    ['name_10', '2025/1/1/0/0'],
    ['name_11', '2025/1/1/0/0'],
    ['name_12', '2025/1/1/0/0'],
    ['name_13', '2025/1/1/0/0'],
    ['name_14', '2025/1/1/0/0'],
    ['name_15', '2025/1/1/0/0'],
    ['name_16', '2025/1/1/0/0'],
    ['name_17', '2025/1/1/0/0'],
    ['name_18', '2025/1/1/0/0']
    ]
for e in events:
    rem.add_event(name=e[0],date_time=str2dt(e[1]))

m = list((re.match(r"(\d+)\s*([a-zA-Z]+)","10 sed")).groups())
timeUnit = {
        "s": "seconds",
        "m": "minutes",
        "h": "hours",
        "d": "days",
        "w": "weeks"
}
print(timeUnit[m[1][0]])
#if __name__ == "__main__":
#    r = scc.Reminder()
#    r.start_reminder_loop()
#
#    # 10秒後の予定
#    dt = datetime.datetime.now() + datetime.timedelta(seconds=10)
#    r.add_event("会議", dt, location="会議室A", items="資料", repeat="daily")
#
#    # 15秒後にカスタムメッセージ付きでリマインド
#    r.remind_after("水分補給", 15, "seconds", message="水を飲んでリフレッシュしましょう")
#
#    # 予定一覧表示
#    r.display_events()
#
#    print("リマインダーを起動中...")
#    while True:
#        time.sleep(60)