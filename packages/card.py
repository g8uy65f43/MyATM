class Card:
    def __init__(self,cardid,pw,islock=False,money=100):
        self.password = pw
        self.money = money
        self.islock = islock
        self.cardid = cardid