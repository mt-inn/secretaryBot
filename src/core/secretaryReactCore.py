import random

class React():
    def __init__(self):
        self.reactCh = ""
        self.praise = []
        self.cheer = []
    def testWord(self):
        return "Hello"
    def evaluateJob(self,score):
        if score < 20:
            return "DO MORE, HARDER"
        elif score<40:
            return "You can do more"
        elif score<60:
            return "not Bad"
        elif score<80:
            return "Very Good"
        else:
            return "You did your best👍"
    def randomList(self,list):
        n = random.randint(0, len(list))
        return list[n]
    
    def reactionText(self, word):
        """
        求められる答えに応じて返信するテキストをランダム選出
        """
        reaction = {
            "done": ["お疲れ様です！"],
            "tired": ["よく頑張りましたね！"],
            "homete": ["死ぬほどえらいです！"]
        }
        return random.choice(reaction[word])
    def cheerUp(self):
        """
        なんか応援するような内容
        """
        answer = "もっとやれ"
        return answer
    def doMore(self):
        """
        尻叩き
        """
        answer = "もっとやれ"
        return answer
    def goodJob(self):
        """
        褒められたい
        """
        answer = "お疲れ様です！"
        return answer
    def mentalCare(self):
        """
        よしよしされたい！！！！！！！！！！！！！！！！
        """
        answer = "よく頑張りましたね！"
        return answer
