import json


class Node:
    def __init__(self, line, val, deep):
        self.child = []
        self.val = val
        self.deep = deep
        self.line = line
        self.converse(val)

    def print(self):
        print(str(json.dumps(self.__dict__)))

    def converse(self, val):
        vals = val.split(" ")
        self.nodeKind = vals[0]
        self.rawline = vals[1]
        vals = vals[2:]

        self.kind = ""
        self.idnum = 0  # 一个节点中的标识符的个数
        self.name = []
        self.attr = {}

        # ProK, PheadK, TypeK, VarK, ProDecK, StmLK, DecK, Stmtk, ExpK
        if self.nodeKind == 'DecK':
            if vals[0] == 'valparamType' or vals[0] == "varparamType":
                self.attr['paramt'] = vals[0]
                vals = vals[1:]
            self.kind = vals[0]
            vals = vals[1:]
            # ArrayK, CharK, IntegerK, RecordK, IdK
            if self.kind == 'ArrayK':
                self.attr['low'] = vals[0]
                self.attr['up'] = vals[1]
                self.attr['childType'] = vals[2]
                vals = vals[3:]
        elif self.nodeKind == 'StmtK':
            # IfK WhileK AssignK ReadK WriteK CallK ReturnK
            self.kind = vals[0]
            vals = vals[1:]
        elif self.nodeKind == 'ExpK':
            # OpK ConstK IdK
            self.kind = vals[0]
            vals = vals[1:]
            if vals[0] in ("IdV", "ArrayMembV", "FieldMembV"):
                self.attr['varkind'] = vals[0]
                vals = vals[1:]
            if self.kind == 'OpK':
                self.attr['op'] = vals[0]
            if self.kind == 'ConstK':
                self.attr['val'] = vals[0]
        for x in vals:
            if x != "":
                self.idnum += 1
                self.name.append(x)
        # self.type_name = type_name


def dfs(node):
    for x in node.child:
        print(node.val, "->", x.val)
    for x in node.child:
        dfs(x)


level_list = {}


def generate_node(tree_path):
    with open(tree_path) as f:
        lines = f.readlines()
        for i in range(len(lines)):
            line = lines[i].replace("\n", "")
            bn = 0
            i = 0
            for i in range(len(line)):
                if line[i] != " ":
                    break
                else:
                    bn += 1
            line = line[i:]
            level = int(bn / 3)
            node = Node(i, line, level)
            if level not in level_list:
                level_list[str(level)] = [node]
                if level > 0:
                    list = level_list[str(level - 1)]
                    list[len(list) - 1].child.append(node)
    # dfs(level_list.get("0")[0])


class DefaultKind:
    def __init__(self, kind):
        self.kind = kind


class Kind:
    def __init__(self, node, body=None):
        self.kind = node.kind
        self.size = 0
        if node.kind == 'ArrayK':
            indexTy = {"low": node.attr["low"], "up": node.attr["up"]}
            elemTy = Kind(DefaultKind(node.attr["childType"])).__dict__
            self.arrayAttr = {"indexTy": indexTy, "elemTy": elemTy}
            self.size = elemTy["size"] * (int(node.attr["up"]) - int(node.attr["low"]))
        if node.kind == 'RecordK':
            for x in body:
                self.size += x.size
        if node.kind == 'IntegerK':
            self.size = 2
        if node.kind == 'CharK':
            self.size = 1


class SymbolTable:
    def __init__(self, node, name, level, off, body=None):
        self.kind = node.kind
        self.name = name
        self.level = level
        self.off = off
        self.body = None
        if body != None:
            tmp = []
            for x in body:
                tmp.append(Kind(x))
            self.body = tmp
        self.typePtr = Kind(node, self.body)

    def __str__(self):
        s = ""
        if self.body != None:
            for x in self.body:
                s += str(x.__dict__)
        return f"kind:{self.kind}, name:{self.name}, level:{self.level}, typePtr:{self.typePtr.__dict__}, body:{s}"


all_scope = [[]]
scope = [[]]
sl = 0
off = 0


def check_varName(name):
    for i in range(sl, -1, -1):
        for x in reversed(scope[sl]):
            if name == x.name:
                return 1
            print(x.name)
    return 0


def generate_table(node):
    global sl, scope
    if node.nodeKind == "DecK":
        for x in node.name:
            err = check_varName(x)
            if err:
                print("val repeated")
                continue

            body = None
            if node.kind == "RecordK":
                body = []
                for y in node.child:
                    body.append(y)
            tab = SymbolTable(node, x, level=sl, off=off, body=body)
            scope[sl].append(tab)
            all_scope[sl].append(tab)
            print(str(tab))
            if node.kind == "RecordK":
                return
    if node.nodeKind == "ProcDecK" and node.idnum > 0:
        sl += 1
        scope.append([])
        all_scope.append([])
    for x in node.child:
        generate_table(x)
    if node.nodeKind == "ProcDecK" and node.idnum > 0:
        sl -= 1
        scope = scope[:-1]
    return


def table_print(table):
    for i in range(len(table)):
        for x in table[i]:
            print(f"i:{i}, ", str(x))


def semantic(tree_path):
    generate_node(tree_path)
    generate_table(level_list.get("0")[0])
    print("all_scope:")
    table_print(all_scope)
