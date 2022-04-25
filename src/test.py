with open("../data/number.txt", "w") as f:
    for x in range(100):
        f.write(str(x+1) + '\n')
