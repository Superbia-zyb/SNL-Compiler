import copy

arr = []
left = set()
right = set()
first = {"": set()}
follow = {"": set()}
predict = {0: set()}


def f(x, only_right):
    i = 0
    flag = 0
    for i in range(2, len(x)):  # 遍历右边的串
        if x[i] in only_right:  # 遇到终极符了
            first[x[0]].add(x[i])
            flag = 1
            break
        elif "NULL" not in first[x[i]]:  # 都非空了
            first[x[0]] = first[x[0]].union(first[x[i]])
            flag = 1
            break
        else:  # 还没到终极符并且有非空
            first[x[0]] = first[x[0]].union(first[x[i]]) - {"NULL"}
    if flag == 0 and ("NULL" in first[x[len(x) - 1]]):
        first[x[0]].add("NULL")


def h(x, i, only_right):
    j = i + 1
    while j < len(x) and (x[j] not in only_right) and ("NULL" in first[x[j]]):
        # 退出：j超了，是终极符，非终但是没有null
        follow[x[i]] = follow[x[i]].union(first[x[j]]) - {"NULL"}
        j = j + 1
    if (j == len(x)):
        follow[x[i]] = follow[x[i]].union(follow[x[0]])
    elif (x[j] in only_right):
        follow[x[i]].add(x[j])
    else:
        follow[x[i]] = follow[x[i]].union(first[x[j]])


def p(x, i, only_right):  # i是行号，x是行
    j = 2
    while j < len(x) and (x[j] not in only_right) and ("NULL" in first[x[j]]):
        # 退出：j超了，是终极符，非终但是没有null
        predict[i] = predict[i].union(first[x[j]]) - {"NULL"}
        j = j + 1
    if j == len(x):  # 超过了
        predict[i] = predict[i].union(follow[x[0]])
    elif x[j] in only_right and x[j] != "NULL":  # 非空外的终极符
        predict[i].add(x[j])
    elif x[j] in only_right and x[j] == "NULL":  # 是空的终极符
        predict[i] = predict[i].union(follow[x[0]])
    else:  # 全部没有Null
        predict[i] = predict[i].union(first[x[j]])


def getPredict():
    with open("../data/grammar.txt") as file:
        lines = file.readlines()
        for line in lines:  # 得到left和right
            line = str(line).replace("\n", "")
            pos = line.split(" ", 20)
            arr.append(pos)
            left.add(pos[0])  # left
            for x in pos[2:]:  # right
                right.add(x)
        only_right = right - left  # 只出现的右边的终极符

        for x in arr:  # 把一眼得到的first加进去
            if x[0] not in first.keys():  # 过了以后就都有关键字了
                first.update({x[0]: set()})
                follow.update({x[0]: set()})
            if x[2] in only_right:  # 右边第一个是终极符
                first[x[0]].add(x[2])
        t = copy.copy(first)
        while True:
            for y in arr:
                if y[2] not in only_right:
                    f(y, only_right)
            if t == first:
                break
            t = copy.copy(first)

        follow.update({arr[0][0]: {"#"}})
        t = copy.copy(follow)
        while True:
            for x in arr:
                for i in range(2, len(x)):
                    if x[i] not in follow.keys() and x[i] not in only_right:  # 还没有关键词并且需要创建关键词
                        follow.update({x[i]: set()})
                    if x[i] not in only_right:  # 只对非终极符进行函数调用
                        h(x, i, only_right)
            if t == follow:
                break
            t = copy.copy(follow)
        k = 1
        t = copy.copy(predict)
        while True:
            for x in arr:
                if k not in follow.keys():
                    predict.update({k: set()})
                p(x, k, only_right)
                k = k + 1
            if t == predict:
                break
            t = copy.copy(predict)
            k = 1
        # print(first)
        # print(follow)
        # for key in predict:
        #     print(key, predict[key])

        return predict, left, only_right
