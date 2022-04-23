import os
from subprocess import Popen, PIPE, STDOUT

def recurse(token_path):
    err = os.system("g++ -std=c++11 ./recursion.cpp -o work")
    if err != 0:
        return -1
    process = Popen('./work', stdout=PIPE, stderr=STDOUT, shell=True)
    with process.stdout:
        for line in iter(process.stdout.readline, b''):
            print(line.decode().strip())
    exitcode = process.wait()
    if err != 0:
        return -1
    return 0
