import threading
from time import ctime, sleep

class MyThread (threading.Thread):
    def __init__(self, func, args, name=""):
        threading.Thread.__init__(self)
        self.func = func
        self.args = args
        self.name = name

    # 　调用start自动执行的函数
    def run(self):
        self.func(self.args)

def player(args):
    print("start player " + str(args))
    sleep(1)

if __name__ == '__main__':
    threadNum = 5
    while threadNum:
        threadNum -= 1
        threads = []
        t = MyThread(player, threadNum)
        t.start()
        threads.append(t)
        for i in threads:
            t.join()