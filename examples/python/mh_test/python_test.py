from multiprocessing import Process
import os
from time import time

def info(title):
    print(title)
    print('module name:', __name__)
    print('parent process:', os.getppid())
    print('process id:', os.getpid())

def f(name):
    info('function f')
    print('hello', name)

if __name__ == '__main__':
    info('main line')
    p = Process(target=f, args=('bob', ))
    p.start()
    t = time()
    while time() - t < 3:
        continue

    
    p.join()


