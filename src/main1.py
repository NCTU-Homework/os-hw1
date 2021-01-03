import sys
from threading import Thread, Lock
import multiprocessing as mp
from multiprocessing import Process
from hashlib import sha256
from time import time as currentTimeInSeconds
import asyncio
from typing import List, Optional, Tuple
from random import randrange, shuffle
from math import ceil
import grequests
import requests
from lxml.html import fromstring


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def currentTimeInMilli():
    return int(currentTimeInSeconds() * 1000)


R_ASCII = 0x7e
L_ASCII = 0x21
LEN_ASCII = R_ASCII - L_ASCII + 1


def getPrefixCandidate(index: int):
    ret = ''
    for i in range(5):
        ret += chr(index % LEN_ASCII + L_ASCII)
        index = index // LEN_ASCII
    return ret


def getRandomPrefixCandidate():
    return getPrefixCandidate(randrange(LEN_ASCII ** 5))


def hash(s: str):
    return sha256(s.encode()).hexdigest()


def findPrefix(list: List[str]):
    for s in list:
        while True:
            p = getRandomPrefixCandidate()
            tested = p + s
            h = hash(tested)
            if h[:5] == '00000':
                print(tested)
                break

async def findPrefixAsync(suffix: str):
    while True:
        p = getRandomPrefixCandidate()
        tested = p + suffix
        h = hash(tested)
        if h[:5] == '00000':
            print(tested)
            break

def findTitle(urls: List[str]):
    for url in urls:
        r = requests.get(url)
        tree = fromstring(r.content)
        title = tree.findtext('.//title')
        print(title)

async def findTitleAsync(url: str):
    r = await grequests.get(url)
    tree = fromstring(r.content)
    title = tree.findtext('.//title')
    print(title)

def solveByThreads(m: int, data: List[str], threadCount: int):
    n = len(data)

    threadList = []
    qn = ceil(n / threadCount)
    tar = findPrefix if m == 1 else findTitle
    for i in range(threadCount):
        t = Thread(target=tar, args=(data[i * qn:i * qn + qn], ))
        t.daemon = True
        threadList.append(t)
    
    t0 = currentTimeInMilli()
    for t in threadList:
        t.start()
    for t in threadList:
        t.join()
    t1 = currentTimeInMilli()

    return t1 - t0


def solveByProcesses(m: int, data: List[str], processCount: int):
    n = len(data)

    processList = []
    qn = n // processCount
    tar = findPrefix if m == 1 else findTitle
    for i in range(processCount):
        p = Process(target=tar, args=(data[i*qn:i*qn+qn], ))
        p.daemon = True
        processList.append(p)
    
    t0 = currentTimeInMilli()
    for p in processList:
        p.start()
    for p in processList:
        p.join()
    t1 = currentTimeInMilli()

    return t1 - t0


async def solveByCoroutine(m: int, data: List[str]):
    n = len(data)
    tar = findPrefixAsync if m == 1 else findTitleAsync
    t0 = currentTimeInMilli()
    await asyncio.gather(*(list(tar(v) for v in data)))
    t1 = currentTimeInMilli()
    return t1 - t0


def main():
    workloadId = int(input())
    measurement = list(int(x) for x in input().split())

    n = int(input())
    data = []
    for _ in range(n):
        data.append(input())
    shuffle(data)

    if measurement[0] == 1:
        t = solveByThreads(workloadId, data, measurement[1])
    elif measurement[0] == 2:
        t = solveByProcesses(workloadId, data, measurement[1])
    elif measurement[0] == 3:
        t = asyncio.run(solveByCoroutine(workloadId, data))
    eprint(str(t))


if __name__ == '__main__':
    main()
