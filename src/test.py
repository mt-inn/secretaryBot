from core import secretaryCalendarCore as scc
import datetime


cal = scc.Reminder()
#Name: Any, date_time: Any, location: Any | None = None, items: Any | None = None, repeat: Any | None = None, message: Any
name = "name"#input("イベント名: ")
date = datetime.datetime(input("日時: "))
loc = "here"#input("場所: ")
item = "no"#input("持ち物: ")
rep = "daily"#input("繰り返し('daily', 'weekly', 'monthly', 'yearly'): ")
mes = "testMassege"#input("メッセージ: ")
cal.add_event(name, date, loc, item, rep, mes)


if __name__ == "__main__":
    r = scc.Reminder()
    r.start_reminder_loop()

    # 10秒後の予定
    dt = datetime.datetime.now() + datetime.timedelta(seconds=10)
    r.add_event("会議", dt, location="会議室A", items="資料", repeat="daily")

    # 15秒後にカスタムメッセージ付きでリマインド
    r.remind_after("水分補給", 15, "seconds", message="水を飲んでリフレッシュしましょう")

    # 予定一覧表示
    r.display_events()

    print("リマインダーを起動中...")
    while True:
        time.sleep(60)