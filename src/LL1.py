from config.LL1_config import Stack, Tree
from grammarProcess import predict1
from predict import getPredict


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
                x[g] = i
            table_col.append(x)
            pre = grammar[i]['left']
        else:
            row = table_row[grammar[i]['left']]  # 处理左端相同的文法
            for g in predict[i + 1]:
                table_col[row][g] = i
    return table_row, table_col


# 初始化
TokenStack = Stack()
SignStack = Stack()
grammar = []
predict, left, only_right = getPredict()
with open("../data/grammar.txt") as file:
    lines = file.readlines()
    for line in lines:
        line = str(line).replace("\n", "")
        pos = line.split(" ", 20)
        x = {'left': pos[0], 'right': pos[2:]}
        grammar.append(x)
with open("../data/token.txt") as file:
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

# LL1驱动程序
syntax_tree = Tree()
PreNode = syntax_tree.root
while not SignStack.isEmpty():
    sign = SignStack.peek()
    toke = TokenStack.peek()
    if toke[1] == 'ID':
        token = 'ID'
    elif toke[1] == 'INTC':
        token = 'INTC'
    elif toke[1] == 'CHARC':
        token = 'CHARC'
    else:
        token = toke[2]
    if sign in left:  # 如果是非终极符，则用语法进行替换
        row = table_row[sign]
        judge = table_col[row][token]
        if judge != -1:
            SignStack.pop()
            rig = grammar[judge]['right']
            length = len(rig)
            for i in range(length):
                if rig[length - 1 - i] != 'NULL':
                    SignStack.push(rig[length - 1 - i])
            PreNode = predict1(judge + 1, syntax_tree, toke, PreNode)
            # if toke[0] == '21':
            # print(judge + 1)
            # syntax_tree.getInfNode()
        else:
            print('error1')
            break
    else:
        if sign == token:  # 相等则进行匹配
            SignStack.pop()
            TokenStack.pop()
        else:  # 不相等出错
            print('error2')
            break
if TokenStack.peek()[2] != 'EOF':
    print('error3')
else:
    print('success')
syntax_tree.getInfNode()
