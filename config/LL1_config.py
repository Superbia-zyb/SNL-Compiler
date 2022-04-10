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


class Node:
    def __init__(self, nodeKind, Lineno=0, type_name='none', judge=False):
        self.nodeKind = nodeKind
        self.child = []
        self.Sibling = None
        self.Lineno = Lineno
        self.kind = {'dec': ' ', 'stmt': ' ', 'exp': ' '}
        self.idnum = 0  # 一个节点中的标识符的个数
        self.name = []
        self.type_name = type_name
        ArrayAttr = {'low': 0, 'up': 0, 'childType': ' '}
        procAttr = {'paramt': ' '}
        ExpAttr = {'op': ' ', 'val': 0, 'varkind': ' ', 'type': ' '}
        attr = []
        attr.append(ArrayAttr)
        attr.append(procAttr)
        attr.append(ExpAttr)
        self.attr = attr
        self.judge = judge
        self.dela = False
        self.ProFirst = True


class Tree(object):
    def __init__(self):
        root = Node('ProK', judge=True)
        self.root = root
        self.stack = Stack()
        self.NumStack = Stack()
        self.SignStack = Stack()
        self.getExpResult = True
        self.getExpResult2 = True
        self.expflag = 0
        self.root.child.append(Node('PheadK'))
        self.root.child.append(Node('TypeK'))
        self.root.child.append(Node('StmLK'))
        self.stack.push(self.root.child[2])
        self.stack.push(self.root.child[1])
        self.stack.push(self.root.child[0])

    def getInfNode(self, priJudge=False):
        stack1 = Stack()
        stack1.push(self.root)
        stackLine = Stack()
        stackLine.push(0)
        with open("../data/syntax_tree.txt", "w") as file:
            while not stack1.isEmpty():
                node = stack1.pop()
                Line = stackLine.pop()
                stm = ''
                if Line > 0:
                    for i in range(Line):
                        stm += '  '
                stm += node.nodeKind
                stm = stm + ' ' + str(node.Lineno)
                if node.nodeKind == 'DecK':
                    if node.attr[1]['paramt'] != ' ':
                        stm = stm + ' ' + node.attr[1]['paramt']
                    stm = stm + ' ' + node.kind['dec']
                    if node.kind['dec'] == 'ArrayK':
                        stm = stm + ' ' + str(node.attr[0]['low']) + ' ' + str(node.attr[0]['up']) + ' ' + node.attr[0][
                            'childType']
                elif node.nodeKind == 'StmtK':
                    stm = stm + ' ' + node.kind['stmt']
                elif node.nodeKind == 'ExpK':
                    stm = stm + ' ' + node.kind['exp']
                    if node.attr[2]['varkind'] != ' ':
                        stm = stm + ' ' + node.attr[2]['varkind']
                if not (node.nodeKind == 'ProcDecK' and node.ProFirst and node.judge):
                    for i in range(node.idnum):
                        stm = stm + ' ' + str(node.name[i])
                b = ['TypeK', 'VarK', 'ProcDecK']
                if node.judge or ((not node.judge) and (node.nodeKind in b)):
                    if priJudge:
                        print(stm)
                    stm += '\n'
                    file.write(stm)
                if node.Sibling != None:
                    if not (node.nodeKind == 'ProcDecK' and node.Sibling.nodeKind == 'ProcDecK' and (
                            not node.Sibling.judge)):
                        stack1.push(node.Sibling)
                        stackLine.push(Line)
                num = len(node.child)
                if node.nodeKind == 'ProcDecK' and node.ProFirst and node.judge:
                    node.ProFirst = False
                    stack1.push(node)
                    stackLine.push(Line + 1)
                elif num > 0:
                    for i in range(num):
                        stack1.push(node.child[num - 1 - i])
                        stackLine.push(Line + 1)
