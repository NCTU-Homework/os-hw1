#!/bin/bash

mkdir -p out
rm -f out/b_*.out

# test 1 thread 4 times
for i in {1..4}; do
    python3.8 src/main1.py<data/b_t1.in >/dev/null 2>>out/b_t1.out
done

# test 2 thread 4 times
for i in {1..4}; do
    python3.8 src/main1.py<data/b_t2.in >/dev/null 2>>out/b_t2.out
done

# test 4 thread 4 times
for i in {1..4}; do
    python3.8 src/main1.py<data/b_t4.in >/dev/null 2>>out/b_t4.out
done

# test 100 thread 4 times
for i in {1..4}; do
    python3.8 src/main1.py<data/b_t100.in >/dev/null 2>>out/b_t100.out
done

# test 1 process 4 times
for i in {1..4}; do
    python3.8 src/main1.py<data/b_p1.in >/dev/null 2>>out/b_p1.out
done

# test 2 prcoess 4 times
for i in {1..4}; do
    python3.8 src/main1.py<data/b_p2.in >/dev/null 2>>out/b_p2.out
done

# test 4 process 4 times
for i in {1..4}; do
    python3.8 src/main1.py<data/b_p4.in >/dev/null 2>>out/b_p4.out
done

# test 100 process 4 times
for i in {1..4}; do
    python3.8 src/main1.py<data/b_p100.in >/dev/null 2>>out/b_p100.out
done

# test coroutine 4 times
for i in {1..4}; do
    python3.8 src/main1.py<data/b_c.in >/dev/null 2>>out/b_c.out
done
