import os


def recurse(token_path):
    err = os.system("g++ -std=c++11 ./recursion.cpp -o work")
    if err != 0:
        return -1
    err = os.system("./work")
    if err != 0:
        return -1
    return 0
