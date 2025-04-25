# カレンダーを使う機能用、カレンダーの基本部分
import calendar

class genCalendar():
    calendarList = []
    def __init__(self):
        self.events = [
            {
                "name": "Str, name of Events like 'Birth day'",
                "date": "YYYY-MM-DD/Mon~Sun/nth-M~S",
                "time": "0~24:0~60",
                "detail": "Str, detail of events",
                "repeat": "no/week/month/year"
                }
                ]
    def addEvent(self, data:dict):
        self.events.append(data)
    def removeEvent(self, name:str):
        for e in self.events:
            self.events.remove(e) if ("name",name) in e else None

