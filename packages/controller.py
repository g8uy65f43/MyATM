from packages.user import User
from packages.card import Card
import os
import pickle
import time


class Controller:
    def __init__(self):
        self.userList = []
        self.cardList = []
        self.cardIdList = []
        self.nameList = []
        self.uidList = []
        # 入力データチェック用
        self.data_List = ('1', '2', '3', '4', '5', '6', '7', '8', '9', '0')
        if os.path.getsize('./simulateDataBases/userid.txt') > 0:
            with open('./simulateDataBases/userid.txt', 'rb') as fp:
                try:
                    while True:
                        self.userList = pickle.load(fp)
                except EOFError:
                    for i in self.userList:
                        self.nameList.append(i.name)
                        self.uidList.append(i.userid)

        if os.path.getsize('./simulateDataBases/cardid.txt') > 0:
            with open('./simulateDataBases/cardid.txt', 'rb') as fp:
                try:
                    while True:
                        self.cardList = pickle.load(fp)
                except EOFError:
                    for i in self.cardList:
                        self.cardIdList.append(i.cardid)

    # データ記入
    def store(self):
        with open('./simulateDataBases/userid.txt', 'ab') as fp:
            pickle.dump(self.userList, fp)
        with open('./simulateDataBases/cardid.txt', 'ab') as fp:
            pickle.dump(self.cardList, fp)

    # ユーザ登録
    def register(self):
        username = self.__getusername()
        userid = self.__getuserid()
        phoneNumber = self.__getphoneNumber()
        cardid = 100000 + len(self.userList)
        while str(cardid) in self.cardIdList:  # 再発行問題防止用
            cardid += 1
        cardid = str(cardid)
        pw = self.__getpassword()
        user = User(username, userid, phoneNumber, cardid)
        card = Card(cardid, pw)
        self.cardList.append(card)
        self.userList.append(user)
        self.nameList.append(username)
        self.uidList.append(userid)
        self.cardIdList.append(cardid)
        print(f"登録しました！，カードナンバーは{cardid}です")
        self.store()

    # 残高照会
    def checkbalance(self):
        flag = self.login()
        if flag != 'n':
            print(f"カードナンバー：{self.cardList[flag].cardid},残高：{self.cardList[flag].money}")

    # 引き出す
    def withdraw(self):
        flag = self.login()
        if flag != 'n':
            while True:
                num = int(input("引き出す金額を入力してください："))
                if num > self.cardList[flag].money:
                    print("残高が足りません！")
                    continue
                else:
                    if self.input_pw(self.cardIdList[flag]):
                        self.cardList[flag].money -= num
                        print(f"カードナンバー：{self.cardList[flag].cardid},残高：{self.cardList[flag].money}")
                        file_url = f'./Transaction_records/{self.cardList[flag].cardid}.txt'
                        content = time.strftime(
                            '%Y-%m-%d %H:%M:%S') + f'引き出す：{num}円，残高：{self.cardList[flag].money}円\n'
                        with open(file_url, 'a+', encoding='utf-8') as fp:
                            fp.write(content)
                        self.store()
                        break
                    else:
                        print("操作失敗、もう一度試してください！")
                        break

    # 預け入れ
    def deposit(self):
        flag = self.login()
        if flag != 'n':
            while True:
                num = int(input("預け入れる金額を入力してください："))
                if self.input_pw(self.cardIdList[flag]):
                    self.cardList[flag].money += num
                    print(f"カードナンバー：{self.cardList[flag].cardid},残高：{self.cardList[flag].money}")
                    file_url = f'./Transaction_records/{self.cardList[flag].cardid}.txt'
                    content = time.strftime(
                        '%Y-%m-%d %H:%M:%S') + f'預け入れ：{num}円，残高：{self.cardList[flag].money}円\n'
                    with open(file_url, 'a+', encoding='utf-8') as fp:
                        fp.write(content)
                    self.store()
                    break
                else:
                    print("預け入れ失敗、もう一度試してください！！")
                    break

    # 振り込み
    def transfer(self):
        idx = self.login()
        if idx != 'n':
            flag = 1
            while flag:
                cardid = input("振込先を入力してください：")
                if cardid not in self.cardIdList:
                    print("振込先が存在していません!")
                    continue
                else:
                    tf_account = self.cardIdList.index(cardid)
                    while True:
                        num = int(input("振り込む金額を入力してください："))
                        if num > self.cardList[idx].money:
                            print("残高が足りません！")
                            continue
                        else:
                            if self.input_pw(self.cardIdList[idx]):
                                self.cardList[idx].money -= num
                                self.cardList[tf_account].money += num
                                print(f"カードナンバー：{self.cardList[idx].cardid},残高：{self.cardList[idx].money}")
                                self.store()
                                flag = 0
                                file_url = f'./Transaction_records/{self.cardList[idx].cardid}.txt'
                                content = time.strftime(
                                    '%Y-%m-%d %H:%M:%S') + f'##卡号：{self.cardList[idx].cardid}，转账：{num}元，余额：{self.cardList[idx].money}元\n'
                                with open(file_url, 'a+', encoding='utf-8') as fp:
                                    fp.write(content)
                                break
                            else:
                                print("パスワードの入力内容に誤りがあります、振り込み失敗！")
                                break

    # ロック
    def lock(self, idx):
        if idx == 'l':
            print("自分でロックすることができません。")
        else:
            self.cardList[idx].islock = True
            self.store()

    # ロック解除
    def unlock(self):
        flag = 1
        while flag:
            userid = input("マイナンバーを入力してください：")
            if userid not in self.uidList:
                print("該当のナンバーを見つかりませんでした！")
                continue
            else:
                while True:
                    cardid = input("カードナンバーを入力してください：")
                    if cardid not in self.cardIdList:
                        print("該当のカードナンバーを見つかりませんでした。")
                        continue
                    else:
                        if self.uidList.index(userid) != self.cardIdList.index(cardid):
                            print("マイナンバーとカードナンバーの入力に誤りがあります、ロック解除失敗しました！")
                        else:
                            self.cardList[self.uidList.index(userid)].islock = False
                            print("ロック解除成功しました！")
                            self.store()
                            flag = 0
                            break

    def change_pw(self):
        idx = self.login()
        flag = 1
        while flag:
            password = input("新しいパスワード（6桁）を入力してください：")
            if len(password) == 6:
                for i in range(6):
                    if password[i] not in self.data_List:
                        print("パスワードは数字オンリーです!")
                        break
                    if i == 5:
                        self.cardList[idx].password = password
                        print("パスワード更新成功しました！")
                        flag = 0
                        self.store()
                        break
            else:
                print("パスワードは6桁です!")

    def input_pw(self, cardid):
        user_index = self.cardIdList.index(cardid)
        pwd = input("パスワードを入力してください：")
        num = 2
        while num:
            if pwd == self.cardList[user_index].password:
                return True
            else:
                num -= 1
                pwd = input(f"パスワードの入力内容に誤りがあります、入力回数残り：{num + 1}回：")
        print("ロックされました！")
        self.lock(user_index)
        return False

    def login(self):
        while True:
            cardid = input("カードのナンバーを入力してください：")
            if cardid in self.cardIdList:
                user_index = self.cardIdList.index(cardid)
                # チェックカード状態
                if not self.cardList[user_index].islock:
                    if self.input_pw(cardid):
                        return user_index
                    else:
                        return 'n'
                else:
                    print("カードはロックされています、ロック解除してください！")
                    return 'n'
            else:
                print("該当のカードナンバーがございません！")

    def __getusername(self):
        while True:
            username = input("お名前を入力してください：")
            if username[0] in self.data_List:
                print("最初の一文字は数字禁止です!")
                continue
            else:
                if username not in self.nameList:
                    return username
                else:
                    print("ユーザはすでに存在しています!")

    def __getuserid(self):
        while True:
            userid = input("十二桁のマイナンバー（数字）を入力してください：")
            if len(userid) == 12:
                for i in range(12):
                    if userid[i] not in self.data_List:
                        print("マイナンバーは数字オンリーです!")
                        break
                    # 既存チェック
                    if i == 11:
                        if userid not in self.uidList:
                            return userid
                        else:
                            print("入力したマイナンバーすでに存在ています!")
            else:
                print("マイナンバーは十二桁です!")

    def __getpassword(self):
        while True:
            password = input("パスワードを六桁入力してください：")
            if len(password) == 6:
                for i in range(6):
                    if password[i] not in self.data_List:
                        print("パスワードは数字オンリーです!")
                        break
                    if i == 5:
                        return password
            else:
                print("パスワードは6桁です")

    def __getphoneNumber(self):
        while True:
            phoneNumber = input("電話番号（11桁）を入力してください：")
            if len(phoneNumber) == 11:
                for i in range(11):
                    if phoneNumber[i] not in self.data_List:
                        print("電話番号は数字オンリーです!")
                        break
                    if i == 10:
                        return phoneNumber
            else:
                print("電話番号は11桁です")
