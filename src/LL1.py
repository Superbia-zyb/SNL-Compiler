from config.LL1_config import Stack, Tree
from GrammarProcess import predict1
from predict import getPredict
from GrammarError import dealError

class LL1:
    def __init__(self, grammarPath, tokenPath, TreePath):
        self.TokenStack = Stack()
        self.SignStack = Stack()
        self.grammar = []
        self.predict, self.left, self.only_right = getPredict()
        self.TreePath = TreePath
        with open(grammarPath) as file:
            lines = file.readlines()
            for line in lines:
                line = str(line).replace("\n", "")
                pos = line.split(" ", 20)
                x = {'left': pos[0], 'right': pos[2:]}
                self.grammar.append(x)
        with open(tokenPath) as file:
            lines = file.readlines()
            nums = len(lines)
            for i in range(nums):
                line = lines[nums - i - 1]
                line = str(line).replace("\n", "")
                pos = line.split(" ", 20)
                self.TokenStack.push(pos)
        self.SignStack.push('Program')
        # 建立分析表
        self.table_row, self.table_col = self.__CreateAnaTable(self.predict, self.grammar, self.only_right)
        self.dealError = dealError(self.left, self.table_row, self.table_col, self.grammar)
        self.errImag = []
        self.runJudge = False

    # 分析表建立函数
    def __CreateAnaTable(self, predict, grammar, only_right):
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

    # LL1驱动程序
    def run(self):
        syntax_tree = Tree()
        PreNode = syntax_tree.root
        while not self.SignStack.isEmpty():
            sign = self.SignStack.peek()
            toke = self.TokenStack.peek()
            if toke[1] == 'ID':
                token = 'ID'
            elif toke[1] == 'INTC':
                token = 'INTC'
            elif toke[1] == 'CHARC':
                token = 'CHARC'
            else:
                token = toke[2]
            if sign in self.left:  # 如果是非终极符，则用语法进行替换
                row = self.table_row[sign]
                judge = self.table_col[row][token]
                if judge != -1:
                    self.SignStack.pop()
                    rig = self.grammar[judge]['right']
                    length = len(rig)
                    for i in range(length):
                        if rig[length - 1 - i] != 'NULL':
                            self.SignStack.push(rig[length - 1 - i])
                    PreNode = predict1(judge + 1, syntax_tree, toke, PreNode)
                    # if toke[0] == '21':
                    # print(judge + 1)
                    # syntax_tree.getInfNode()
                else:
                    errJudge, ErrImag = self.dealError.run(self.SignStack, self.TokenStack)
                    Err = {'line':0, 'message':' '}
                    Err['line'] = int(toke[0])
                    Err['message'] = ErrImag
                    self.errImag.append(Err)
                    if not errJudge:
                        break
            else:
                if sign == token:  # 相等则进行匹配
                    self.SignStack.pop()
                    self.TokenStack.pop()
                else:  # 不相等出错
                    errJudge, ErrImag = self.dealError.run(self.SignStack, self.TokenStack)
                    Err = {'line': 0, 'message': ' '}
                    Err['line'] = int(toke[0])
                    Err['message'] = ErrImag
                    self.errImag.append(Err)
                    if not errJudge:
                        break
        if self.TokenStack.peek()[2] != 'EOF':
            if len(self.errImag) == 0:
                Err = {'line': 0, 'message': ' '}
                Err['line'] = int(self.TokenStack.peek()[0])
                Err['message'] = '符号栈仍有残余'
                self.errImag.append(Err)
        else:
            self.runJudge = True
        syntax_tree.getInfNode(self.TreePath)
        self.syntax_tree = syntax_tree

    def showError(self, show=False):
        if show:
            if self.runJudge:
                print('语法树生成成功，可以继续运行')
            else:
                print('有语法错误，且尝试修复失败，语法树生成失败，不可继续运行')
            for i in range(len(self.errImag)):
                print(self.errImag[i])
        return not self.runJudge, self.errImag

# ll1 = LL1("../data/grammar.txt", "../data/token.txt")
# ll1.run()
# ll1.showError()