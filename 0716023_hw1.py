#!/usr/bin/python3

from threading import Thread
from threading import Lock
from multiprocessing import Process
from hashlib import sha256
from time import time as currentTimeInSeconds
import sys
from random import randrange as rand


def currentTimeInMicorseconds():
    return int(currentTimeInSeconds() * 1000000)


class WorkloadA:

    L_ASCII = 0x21
    R_ASCII = 0x7e
    RND_RANGE = (R_ASCII - L_ASCII) ** 5

    def getCandidate(self, index: int) -> str:
        ret = ''
        for i in range(5):
            ret += chr(index % (self.R_ASCII - self.L_ASCII + 1) + self.L_ASCII)
            index = index // (self.R_ASCII - self.L_ASCII + 1)
        return ret

    def solveByThreads(self, suffix: str, threadCount: int):
        self.flag = True

        threadList = []
        t0 = currentTimeInMicorseconds()
        for i in range(threadCount):
            t = Thread(target=self.task, args=(suffix, ))
            t.daemon = True
            threadList.append(t)
            t.start()
        for t in threadList:
            t.join()
        t1 = currentTimeInMicorseconds()

        return self.answer + suffix, t1 - t0

    def solveByProcesses(self, suffix: str, processCount: int):
        self.flag = True

        processList = []
        t0 = currentTimeInMicorseconds()
        for i in range(processCount):
            p = Process(target=self.task, args=(suffix, ))
            p.daemon = True
            processList.append(p)
            p.start()
        for p in processList:
            p.join()
        t1 = currentTimeInMicorseconds()

        return self.answer + suffix, t1 - t0

    def solveByCoroutine(self, suffix: str):
        self.flag = True

        async def calc(prefix: str):
            tested = prefix + suffix
            hashValue = sha256(tested.encode()).hexdigest()
            if hashValue[:5] == '00000':
                self.answer = prefix
                self.flag = False

        t0 = currentTimeInMicorseconds()
        while self.flag:
            prefix = self.counter.next()
            calc(prefix)
        t1 = currentTimeInMicorseconds()
        return self.answer + suffix, t1 - t0

    def task(self, suffix: str):
        while self.flag:
            prefix = self.getCandidate(rand(self.RND_RANGE))
            tested = prefix + suffix
            hashValue = sha256(tested.encode()).hexdigest()
            if hashValue[:5] == '00000':
                self.answer = prefix
                self.flag = False

def main():
    dev = False
    if len(sys.argv) == 2 and sys.argv[1] == '--dev':
        dev = True

    workloadId = int(input())
    measurement = list(int(x) for x in input().split())


    if workloadId == 1:
        workload = WorkloadA()
    else:
        print('TODO')
        exit(-1)
    
    n = int(input())
    for _ in range(n):
        suffix = input()
        if measurement[0] == 1:
            result = workload.solveByThreads(suffix, measurement[1])
        elif measurement[0] == 2:
            result = workload.solveByProcesses(suffix, measurement[1])
        else:
            result = workload.solveByCoroutine(suffix)
        print(result if dev else result[0])


if __name__ == '__main__':
    main()
