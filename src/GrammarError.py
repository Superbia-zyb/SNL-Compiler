import copy

class dealError:
    def __init__(self, left, table_row, table_col, grammar):
        self.left = left
        self.table_row = table_row
        self.table_col = table_col
        self.grammar = grammar
        self.reservedWords = [
            "PROGRAM",
            "TYPE",
            "VAR",
            "PROCEDURE",
            "IF",
            "THEN",
            "ELSE",
            "FI",
            "WHILE",
            "DO",
            "ENDWH",
            "BEGIN",
            "END",
            "READ",
            "WRITE",
            "ARRAY",
            "OF",
            "RECORD",
            "RETURN",
            "INTEGER",
            "CHAR",
        ]  # 保留字
        self.delimiters = [
            ".",
            ":=",
            "=",
            "<",
            "+",
            "-",
            "*",
            "/",
            ",",
            "[",
            "]",
            "..",
            ";",
            "(",
            ")",
        ]  # 运算符、限界符

    # 判断修改是否正确：
    def __judgeRepair2(self, SignStack, TokenStack):
        num = 10
        while (not SignStack.isEmpty()) and num > 0:
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
            if sign in self.left:  # 如果是非终极符，则用语法进行替换
                row = self.table_row[sign]
                judge = self.table_col[row][token]
                if judge != -1:
                    SignStack.pop()
                    rig = self.grammar[judge]['right']
                    length = len(rig)
                    for i in range(length):
                        if rig[length - 1 - i] != 'NULL':
                            SignStack.push(rig[length - 1 - i])
                else:
                    return False
            else:
                if sign == token:  # 相等则进行匹配
                    SignStack.pop()
                    TokenStack.pop()
                else:  # 不相等出错
                    return False
            num -= 1
        return True

    # 判断修改是否正确：
    def __judgeRepair(self, sign, token):
        if sign in self.left:  # 如果是非终极符，则用语法进行替换
            row = self.table_row[sign]
            judge = self.table_col[row][token]
            if judge != -1:
                return True
            else:
                return False
        else:
            if sign == token:  # 相等则进行匹配
                return True
            else:  # 不相等出错
                return False

    def run(self, SignStack, TokenStack):
        ErrImag = ' '
        judge = False
        for i in range(3):
            judge, ErrImag = self.__repair(i + 1, SignStack, TokenStack)
            if judge:
                break
        if not judge:
            ErrImag = 'Other unclear wrong'
        return judge, ErrImag

    def __repair(self, num, SignStack, TokenStack):
        self.sign = SignStack.peek()
        toke = TokenStack.peek()
        if toke[1] == 'ID':
            self.token = 'ID'
        elif toke[1] == 'INTC':
            self.token = 'INTC'
        elif toke[1] == 'CHARC':
            self.token = 'CHARC'
        else:
            self.token = toke[2]
        if num == 1:
            judge, ErrImag = self.__error1(SignStack, TokenStack)
        elif num == 2:
            judge, ErrImag = self.__error2(SignStack, TokenStack)
        elif num == 3:
            judge, ErrImag = self.__error3(SignStack, TokenStack)
        return judge, ErrImag

    def __error1(self, SignStack, TokenStack):
        # 缺少保留字
        for i in range(len(self.reservedWords)):
            ReWord = self.reservedWords[i]
            S1 = copy.deepcopy(SignStack)
            T1 = copy.deepcopy(TokenStack)
            T1.push(['0', 'Reserved_word', ReWord])
            if self.__judgeRepair2(S1, T1):
                TokenStack.push(['0', 'Reserved_word', ReWord])
                message = '缺少' + ReWord
                return True, message
        return False, ' '

    def __error2(self, SignStack, TokenStack):
        # 缺少运算数
        if self.__judgeRepair(self.sign, 'INTC'):
            TokenStack.push(['0', 'INTC', 'error'])
            return True, '缺少常量'
        else:
            return False, ' '

    def __error3(self, SignStack, TokenStack):
        # 缺少符号
        for i in range(len(self.delimiters)):
            Deli = self.delimiters[i]
            S1 = copy.deepcopy(SignStack)
            T1 = copy.deepcopy(TokenStack)
            T1.push(['0', 'Other', Deli])
            if self.__judgeRepair2(S1, T1):
                TokenStack.push(['0', 'Other', Deli])
                message = '缺少' + Deli
                return True, message
        return False, ' '