from packages.viewclass import Views
from packages.controller import Controller
import time


class main:
    def __init__(self):
        view = Views()
        obj = Controller()
        while True:
            num = input("ご要件のナンバーを入力してください：")
            if num == '1':
                obj.deposit()
                time.sleep(2)
                view.show_operator()
            elif num == '2':
                obj.withdraw()
                time.sleep(2)
                view.show_operator()
            elif num == '3':
                obj.transfer()
                time.sleep(2)
                view.show_operator()

            elif num == '4':
                obj.checkbalance()
                time.sleep(2)
                view.show_operator()

            elif num == '5':
                obj.register()
                time.sleep(2)
                view.show_operator()

            elif num == '6':
                obj.lock('l')
                time.sleep(2)
                view.show_operator()
            elif num == '7':
                obj.unlock()
                time.sleep(2)
                view.show_operator()
            elif num == '8':
                obj.new_card()
                time.sleep(2)
                view.show_operator()
            elif num == '9':
                obj.change_pwd()
                time.sleep(2)
                view.show_operator()
            elif num == '0':
                obj.store()
                break
        else:
            print("您的输入有误，请重新输入：")
            view.show_operator()

run = main()
