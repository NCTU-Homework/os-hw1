#!/bin/bash
set -e

mkdir -p out
rm -f out/a_*.out

# test 1 thread 4 times
for i in {1..4}; do
    python3.8 src/main1.py<data/a_t1.in >/dev/null 2>>out/a_t1.out
done

# test 2 thread 4 times
for i in {1..4}; do
    python3.8 src/main1.py<data/a_t2.in >/dev/null 2>>out/a_t2.out
done

# test 4 thread 4 times
for i in {1..4}; do
    python3.8 src/main1.py<data/a_t4.in >/dev/null 2>>out/a_t4.out
done

# test 100 thread 4 times
for i in {1..4}; do
    python3.8 src/main1.py<data/a_t100.in >/dev/null 2>>out/a_t100.out
done

# test 1 process 4 times
for i in {1..4}; do
    python3.8 src/main1.py<data/a_p1.in >/dev/null 2>>out/a_p1.out
done

# test 2 prcoess 4 times
for i in {1..4}; do
    python3.8 src/main1.py<data/a_p2.in >/dev/null 2>>out/a_p2.out
done

# test 4 process 4 times
for i in {1..4}; do
    python3.8 src/main1.py<data/a_p4.in >/dev/null 2>>out/a_p4.out
done

# test 100 process 4 times
for i in {1..4}; do
    python3.8 src/main1.py<data/a_p100.in >/dev/null 2>>out/a_p100.out
done

# test coroutine 4 times
for i in {1..4}; do
    python3.8 src/main1.py<data/a_c.in >/dev/null 2>>out/a_c.out
done
