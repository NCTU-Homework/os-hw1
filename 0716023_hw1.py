#!/usr/bin/python3

from threading import Thread
from threading import Lock
from multiprocessing import Process, Queue
from hashlib import sha256
from time import time as currentTimeInSeconds
import sys
from random import randrange as rand
from ctypes import c_wchar_p
from queue import Empty

def currentTimeInMicroseconds():
    return int(currentTimeInSeconds() * 1000000)


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
    answer = [None] * n
    taskQueue = Queue()
    for i, v in enumerate(suffices):
        taskQueue.put((i, v))

    # 0x21 ~ 0x7e
    def worker():
        while True:
            try:
                ansIdx, suffix = taskQueue.get_nowait()
            except Empty:
                break
            i = 0
            while True:
                prefix = getCandidate(i)
                tested = prefix + suffix
                hashValue = sha256(tested.encode()).hexdigest()
                if hashValue[:5] == '00000':
                    answer[ansIdx] = tested
                    break
                i = i + 1

    threadList = []
    t0 = currentTimeInMicroseconds()
    for _ in range(threadCount):
        t = Thread(target=worker)
        t.daemon = True
        threadList.append(t)
        t.start()
    for t in threadList:
        t.join()
    t1 = currentTimeInMicroseconds()
    return answer, t1 - t0


def waSolveByProcesses(suffices, processCount: int):
    n = len(suffices)
    resultQueue = Queue()
    taskQueue = Queue()
    for i, v in enumerate(suffices):
        taskQueue.put((i, v))

    # 0x21 ~ 0x7e
    def worker():
        while True:
            try:
                ansIdx, suffix = taskQueue.get_nowait()
            except Empty:
                break
            i = 0
            while True:
                prefix = getCandidate(i)
                tested = prefix + suffix
                hashValue = sha256(tested.encode()).hexdigest()
                if hashValue[:5] == '00000':
                    resultQueue.put((ansIdx, prefix + suffix))
                    break
                i = i + 1

    processList = []
    t0 = currentTimeInMicroseconds()
    for _ in range(processCount):
        p = Process(target=worker)
        p.daemon = True
        processList.append(p)
        p.start()
    for p in processList:
        p.join()
    t1 = currentTimeInMicroseconds()
    
    result = []
    while not resultQueue.empty():
        result.append(resultQueue.get())
    result.sort(key=lambda a: a[0])
    return list(v[1] for v in result), t1 - t0


def main():
    dev = False
    if len(sys.argv) == 2 and sys.argv[1] == '--dev':
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
        for v in result[0]:
            print(v)
        if dev:
            ms = (result[1]) // 1000
            print('time:', ms, 'ms')


if __name__ == '__main__':
    main()
