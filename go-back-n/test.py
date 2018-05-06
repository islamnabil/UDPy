import subprocess
from threading import Thread

threadpool = []


def fun():
    subprocess.call('python GBN_Client.py', stdout=subprocess.PIPE,
                    shell=True)


for i in range(5):
    thread = Thread(target=fun, args=())
    threadpool.append(thread)
    thread.start()

for i in range(5):
    threadpool[i].join()
