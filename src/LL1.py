from te import getPredict

# 定义栈
class Stack:
    def __init__(self):
        self.items = []

    def isEmpty(self):
        return self.items == []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        return self.items.pop()

    def peek(self):
        return self.items[len(self.items) - 1]

    def size(self):
        return len(self.items)

# 分析表建立函数
def CreateAnaTable(predict, grammar, only_right):
    pre = ''
    num = 0
    table_row = {}
    table_col = []
    for i in range(len(grammar)):
        if grammar[i]['left'] != pre:
            table_row[grammar[i]['left']] = num  # 设置行
            num += 1
            x = {}
            for j in only_right:  # 初始化列
                x[j] = -1
            for g in predict[i + 1]:  # 处理左端无相同的文法
                x[g] = i + 1
            table_col.append(x)
            pre = grammar[i]['left']
        else:
            row = table_row[grammar[i]['left']]  # 处理左端相同的文法
            for g in predict[i + 1]:
                table_col[row][g] = i + 1
    return table_row, table_col

# 初始化
TokenStack = Stack()
SignStack = Stack()
grammar = []
predict, left, only_right = getPredict()
with open("../data/3.txt") as file:
    lines = file.readlines()
    for line in lines:
        line = str(line).replace("\n", "")
        pos = line.split(" ", 20)
        x = {'left':pos[0],'right':pos[2:]}
        grammar.append(x)
with open("../data/TokenList.txt") as file:
    lines = file.readlines()
    nums = len(lines)
    for i in range(nums):
        line = lines[nums - i - 1]
        line = str(line).replace("\n", "")
        pos = line.split(" ", 20)
        TokenStack.push(pos)
SignStack.push('Program')

# 建立分析表
table_row, table_col = CreateAnaTable(predict, grammar, only_right)
