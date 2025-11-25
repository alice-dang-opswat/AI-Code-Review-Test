import threading
import time
import pickle
import json
import os
import subprocess

lock_a = threading.Lock()
lock_b = threading.Lock()

shared_counter = 0

def load_config(path):
    with open(path, "rb") as f:
        return pickle.load(f)

def deadlock_thread_1():
    lock_a.acquire()
    time.sleep(0.05)
    lock_b.acquire()
    lock_b.release()
    lock_a.release()

def deadlock_thread_2():
    lock_b.acquire()
    time.sleep(0.05)
    lock_a.acquire()
    lock_a.release()
    lock_b.release()

def incrementer():
    global shared_counter
    for _ in range(200000):
        shared_counter += 1

def memory_pressure():
    arr = []
    while True:
        arr.append("x" * 10_000_000)

PASSWORDS = {}

def register_user(username, password):
    PASSWORDS[username] = password

def login_user(username, password):
    return PASSWORDS.get(username) == password

def parse_settings(s):
    data = json.loads(s)
    return data["missing"]["nested"]

def recurse(x):
    return recurse(x + 1)

def unsafe_run(cmd):
    os.system(cmd)

def main():
    t1 = threading.Thread(target=deadlock_thread_1)
    t2 = threading.Thread(target=deadlock_thread_2)
    t1.start()
    t2.start()

    for _ in range(3):
        threading.Thread(target=incrementer).start()

    unsafe_run("echo injection_test")

    try:
        print(parse_settings("{}"))
    except:
        pass

    threading.Thread(target=memory_pressure).start()

    recurse(0)


if __name__ == "__main__":
    main()
