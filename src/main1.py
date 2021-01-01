import sys
from queue import Empty, Queue
from threading import Thread, Lock
import multiprocessing as mp
from multiprocessing import Process
from hashlib import sha256
from time import time as currentTimeInSeconds
import asyncio


def currentTimeInMilliseconds():
    return int(currentTimeInSeconds() * 1000)


R_ASCII = 0x7e
L_ASCII = 0x21


def getCandidate(index: int):
    ret = ''
    for i in range(5):
        ret += chr(index % (R_ASCII - L_ASCII + 1) + L_ASCII)
        index = index // (R_ASCII - L_ASCII + 1)
    return ret


def waSolveByThreads(suffices, threadCount: int):
    n = len(suffices)
    result = [None] * n
    taskQueue = Queue()
    for i, v in enumerate(suffices):
        taskQueue.put((i, v))

    # 0x21 ~ 0x7e
    def worker():
        while True:
            try:
                idx, suffix = taskQueue.get_nowait()
            except Empty:
                break
            i = 0
            while True:
                prefix = getCandidate(i)
                tested = prefix + suffix
                hashValue = sha256(tested.encode()).hexdigest()
                if hashValue[:5] == '00000':
                    result[idx] = tested
                    break
                i = i + 1

    threadList = []
    t0 = currentTimeInMilliseconds()
    for _ in range(threadCount):
        t = Thread(target=worker)
        t.daemon = True
        threadList.append(t)
        t.start()
    for t in threadList:
        t.join()
    t1 = currentTimeInMilliseconds()

    return result, t1 - t0


def waSolveByProcesses(suffices, processCount: int):
    n = len(suffices)
    resultQueue = mp.Queue()
    taskQueue = mp.Queue()
    for i, v in enumerate(suffices):
        taskQueue.put((i, v))

    # 0x21 ~ 0x7e
    def worker():
        while True:
            try:
                idx, suffix = taskQueue.get_nowait()
            except Empty:
                break
            i = 0
            while True:
                prefix = getCandidate(i)
                tested = prefix + suffix
                hashValue = sha256(tested.encode()).hexdigest()
                if hashValue[:5] == '00000':
                    resultQueue.put((idx, tested))
                    break
                i = i + 1

    processList = []
    t0 = currentTimeInMilliseconds()
    for _ in range(processCount):
        p = Process(target=worker)
        p.daemon = True
        processList.append(p)
        p.start()
    for p in processList:
        p.join()
    t1 = currentTimeInMilliseconds()

    result = [None] * n
    while not resultQueue.empty():
        idx, val = resultQueue.get()
        result[idx] = val
    return result, t1 - t0

async def waSolveByCoroutine(suffices):
    n = len(suffices)
    
    async def worker(suffix: str):
        i = 0
        while True:
            prefix = getCandidate(i)
            tested = prefix + suffix
            hashValue = sha256(tested.encode()).hexdigest()
            if hashValue[:5] == '00000':
                return tested
            i = i + 1
    
    t0 = currentTimeInMilliseconds()
    result = await asyncio.gather(*(list(worker(v) for v in suffices)))
    t1 = currentTimeInMilliseconds()
    return result, t1 - t0


def main():
    dev = False
    if '--dev' in sys.argv:
        dev = True

    workloadId = int(input())
    measurement = list(int(x) for x in input().split())

    if workloadId == 1:
        n = int(input())
        suffices = []
        for _ in range(n):
            suffices.append(input())
        if measurement[0] == 1:
            result = waSolveByThreads(suffices, measurement[1])
        elif measurement[0] == 2:
            result = waSolveByProcesses(suffices, measurement[1])
        elif measurement[0] == 3:
            result = asyncio.run(waSolveByCoroutine(suffices))
        for v in result[0]:
            print(v)
        
        print('time:', result[1], 'ms')


if __name__ == '__main__':
    main()
