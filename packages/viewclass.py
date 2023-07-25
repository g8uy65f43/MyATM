import time


class Views:
    def __init__(self):
        self.__show_welcome()
        print("システムLoding...")
        time.sleep(1)
        self.show_operator()

    def __show_welcome(self):
        varstr = '''-----------------------------------------------------
|                                                     |
|                                                     |
|                       Hello!                        |
|                                                     |
|                                                     |
-----------------------------------------------------'''
        print(varstr)

    def show_operator(self):
        varstr_operator = '''
-----------------------------------------------------------------
|\t\t1、引き出し\t\t2、預け入れ\t\t|
|\t\t3、振り込み\t\t4、残高照会\t\t|
|\t\t5、申し込み\t\t6、カードロック\t\t|
|\t\t7、ロック解除\t\t8、再発行\t\t|
|\t\t9、パスワード変更\t0、EXIT\t\t\t|
------------------------------------------------------------------
'''
        print(varstr_operator)


if __name__ == '__main__':
    obj = Views()