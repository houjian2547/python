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
        self.func(*self.args)

def player(song_file,time):
    for i in range(2):
        print("start player %s . %s"%(song_file,ctime()) )
    sleep(time)

if __name__ == '__main__':
    # main()
    threadNum = 5
    while threadNum:
        MyThread(1, "Thread-" + str(threadNum)).start()
        threadNum -= 1

        threads = []
        d = {'body.mp3': 3, "Avater.mp4": 5, "You and me.mp3": 6}

        t = MyThread(player)
        threads.append(t)
        t.start()

        for i in threads:
            t.join()