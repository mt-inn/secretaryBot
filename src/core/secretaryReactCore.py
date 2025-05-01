import random

class React():
    def __init__(self):
        self.praise = []
        self.cheer = []
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