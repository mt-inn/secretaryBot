import asyncio
import datetime
from dateutil.relativedelta import relativedelta
from core import config

class Reminder:
    client = config.client

    def __init__(self):
        """
        登録された予定を辞書形式で管理
        {
        "key":{"name":"hoge"...}
        }
        """
        self.schedule = {}
        self.addres = 0
        self.addresType = "dm"
    
    def _generate_key(self, name, date_time):
        # 各予定を一意に識別するためのキーを生成
        return f"{name}_{int(date_time.timestamp())}"
    async def configAddres(self, addres, typeInput:str):
        if typeInput == "ch":
            self.addres = self.client.get_channel(addres)
        else:
            self.addres = addres
        self.addresType = typeInput
        return
    
    async def sendMessage(self, content):
        await self.addres.send(content)
        return
    def add_event(self, name:str, date_time:datetime, location:str=None, items:str=None, repeat:str=None, message:str=None, user:int=None):
        """
        新しい予定を追加します。

        Args:
            name (str): 予定名
            date_time (datetime): 実行時刻
            location (str): 場所
            items (str): 持ち物など
            repeat (str): 繰り返し（'daily', 'weekly', 'monthly', 'yearly')
            message (str): カスタムリマインドメッセージ
            user (int): メンションする相手のID

        例:
            dt = datetime.datetime(2025, 5, 1, 9, 0)
            add_event("出張", dt, location="大阪", items="資料", repeat="monthly")
        """
        key = self._generate_key(name, date_time)
        self.schedule[key] = {
            "name": name,
            "date_time": date_time,
            "location": location,
            "items": items,
            "repeat": repeat,
            "message": message,
            "user": user
        }
        return

    def delete_event(self, name:str=None, date:datetime=None):
        """
        名前または日付に基づいて予定を削除します。

        Args:
            name (str): 削除対象の予定名
            date (datetime.date): 削除対象の予定日

        Returns:
            int: 削除した予定の数

        例:
            delete_event(name="会議")
            delete_event(date=datetime.date(2025, 5, 1))
        """
        to_delete = []
        deleted = []
        for key, event in self.schedule.items():
            if (name is None or event["name"] == name) and (date is None or event["date_time"].date() == date):
                to_delete.append(key)
        for k in to_delete:
            deleted.append(self.schedule.pop(k))
        return deleted

    def update_event(self, old_name:str, old_date:datetime, new_event_data:dict):
        """
        既存の予定を更新します。

        Args:
            old_name (str): 更新対象の旧予定名
            old_date (datetime.date): 更新対象の旧日付
            new_event_data (dict): 新しい予定情報 (add_eventと同じ構造)

        Returns:
            bool: 更新成功時は True

        例:
            update_event("出張", datetime.date(2025, 5, 1), {
                "name": "出張",
                "date_time": datetime.datetime(2025, 5, 2, 10, 0),
                "location": "名古屋",
                "items": "名刺",
                "repeat": "monthly",
                "message": "新幹線を予約する"
            })
        """
        for key, event in list(self.schedule.items()):
            if event["name"] == old_name and event["date_time"].date() == old_date:
                self.schedule[key] = new_event_data
                return True
        return False

    def list_events(self, inputDate:datetime=None):
        """
        予定一覧をリストとして取得します。

        Args:
            date (datetime.date): 指定日の予定のみ抽出（省略可）

        Returns:
            list[dict]: 条件に一致した予定のリスト
        """
        result = []
        for event in sorted(self.schedule.values(), key=lambda e: e["date_time"]):
            print(f"{event["date_time"]}, {inputDate.date}")
            if inputDate is None or event["date_time"].date() == inputDate.date.date():
                result.append(event)
        return result

    def display_events(self, date:datetime=None):
        """
        ターミナルに予定一覧を表示します。

        Args:
            date (datetime.date): 指定日のみを表示（省略可）

        例:
            display_events()
            display_events(datetime.date.today())
        """
        events = self.list_events(date)
        if not events:
            print("予定はありません。")
            return
        for e in events:
            print(f"\n📅 {e['name']} - {e['date_time'].strftime('%Y-%m-%d %H:%M')}")
            if e['location']:
                print(f"  - 場所: {e['location']}")
            if e['items']:
                print(f"  - 持ち物: {e['items']}")
            if e['repeat']:
                print(f"  - 繰り返し: {e['repeat']}")
            if e['message']:
                print(f"  - メッセージ: {e['message']}")
        return

    async def _remind(self, event):
        # リマインドの実行内容（カスタムメッセージ優先）
        text = f"<@{event['user']}>\n**リマインド:** {event['name']}"
        if event['message']:
            text += f"\n{event['message']}"
        else:
            text += f"\n**時間:** {event['date_time']}"
            if event['location']:
                text += f"\n**場所:** {event['location']}"
            if event['items']:
                text += f"**持ち物:** {event['items']}"
        await self.sendMessage(content=text)
        return

    def _reschedule(self, key, event):
        # 繰り返し設定がある予定を次回にスケジュール
        dt = event["date_time"]
        repeat = event["repeat"]

        if repeat == "daily":
            new_dt = dt + datetime.timedelta(days=1)
        elif repeat == "weekly":
            new_dt = dt + datetime.timedelta(weeks=1)
        elif repeat == "monthly":
            new_dt = dt + relativedelta(months=1)
        elif repeat == "yearly":
            new_dt = dt + relativedelta(years=1)
        else:
            return

        new_key = self._generate_key(event["name"], new_dt)
        event["date_time"] = new_dt
        self.schedule[new_key] = event
        del self.schedule[key]
        return

    def start_reminder_loop(self):
        """
        リマインダーのバックグラウンドループを開始します。
        毎秒予定をチェックして、該当があればリマインドします。
        """
        async def checkLoop():
            while True:
                now = datetime.datetime.now()
                for key, event in list(self.schedule.items()):
                    if abs((event["date_time"] - now).total_seconds()) < 1:
                        if event["repeat"]:
                            self._reschedule(key, event)
                        else:
                            del self.schedule[key]
                        await self._remind(event)
                await asyncio.sleep(1)
    
        asyncio.create_task(checkLoop())  # ← タスクとして起動

    def remind_after(self, name:str, delay_amount:int, delay_unit:str="seconds", location:str=None, items:str=None, message:str=None,user:int=None):
        """
        指定した時間後にリマインドする予定を作成します。

        Args:
            name (str): イベント名
            delay_amount (int): 遅延時間の量
            delay_unit (str): 'seconds', 'minutes', 'hours', 'days', 'weeks'

        例:
            remind_after("立ち上がる", 30, "minutes", message="少し歩きましょう")
        """
        unit_map = {
            "seconds": "seconds",
            "minutes": "minutes",
            "hours": "hours",
            "days": "days",
            "weeks": "weeks"
        }
        if delay_unit not in unit_map:
            raise ValueError("無効な時間単位です")
        delta = datetime.timedelta(**{unit_map[delay_unit]: delay_amount})
        remind_time = datetime.datetime.now() + delta
        self.add_event(name=name, date_time=remind_time, location=location, items=items, message=message,user=user)
