import random
from core import config

class React():
    def __init__(self):
        self.reactCh = None
        self.praise = []
        self.cheer = []
    def reactionText(self, text):
        """
        求められる答えに応じて返信するテキストをランダム選出
        """
        reactionLists = [
            ["終わった", "done"],
            ["終わり", "done"],
            ["どね", "done"],
            ["done", "done"],
            ["疲れた", "tired"],
            ["褒めて", "homete"]
            ]
        reaction = {
            "done": ["お疲れ様です！"],
            "tired": ["よく頑張りましたね！"],
            "homete": ["死ぬほどえらいです！"]
        }
        for e in reactionLists:
            if e[0] in text:
                return random.choice(reaction[e[1]])
