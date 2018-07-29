import time
import threading

# for i in range(100000):
#     percent = 1.0 * i / 100000 * 100
#     print('complete percent:%10.8s%s' % (str(percent), '%'), end='\r')
#     time.sleep(0.1)


# html = '<a "="" target="_blank"><span style="COLOR: black">淘宝网购物</span></a>'
# labelOfAs = html.find_all('a')
# for labelOfA in labelOfAs:
#     print(labelOfA['href'])

exitFlag = 0

class myThread (threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
    def run(self):
        print ("开始线程：" + self.name)
        print_time(self.name, self.counter, 5)
        print ("退出线程：" + self.name)

def print_time(threadName, delay, counter):
    while counter:
        # if exitFlag:
        #     print('exitFlag')
        #     threadName.exit()
        time.sleep(delay)
        print ("%s: %s" % (threadName, time.ctime(time.time())))
        counter -= 1

def main():
    # 创建新线程
    thread1 = myThread(1, "Thread-1", 1)
    thread2 = myThread(2, "Thread-2", 2)
    # 开启新线程
    thread1.start()
    thread2.start()
    thread1.join()
    thread2.join()
    print("退出主线程")

if __name__ == '__main__':
    main()
