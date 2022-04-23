import copy
import json
import re
import sys  # 导入sys模块
from visualTree import visTree

sys.setrecursionlimit(3000)
flag = False

class Node:
    def __init__(self, line, val, deep):
        self.child = []
        self.val = val
        self.deep = deep
        self.line = str(line + 1)
        self.converse(val)

    def __str__(self):
        return str(self.__dict__)

    def print(self):
        print(str(json.dumps(self.__dict__)))

    def converse(self, val):
        vals = val.split(" ")
        self.nodeKind = vals[0]
        self.rawline = str(int(vals[1]) + 1)
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
            if self.kind == "IdK":
                self.realKind = vals[0]
                vals = vals[1:]
            # ArrayK, CharK, IntegerK, RecordK, IdK
            if self.kind == 'ArrayK':
                self.attr['low'] = vals[0]
                self.attr['up'] = vals[1]
                self.attr['childType'] = vals[2]
                vals = vals[3:]
        elif self.nodeKind == 'StmtK':
            # IfK WhileK AssignK ReadK WriteK CallK ReturnK
            if vals[0] != "" or vals[0] != " ":
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

def error(*param):
    global flag
    flag = True
    s = ""
    for x in param:
        if type(x) == "str":
            s += x
        else:
            s = s + str(x) + " "
    #print(f"\033[31m{s}\033[0m")
    print(s)

def dfs(node):
    for x in node.child:
        print(node.val, "->", x.val)
    for x in node.child:
        dfs(x)

def generate_node(tree_path):
    level_list = {}
    with open(tree_path) as f:
        lines = f.readlines()
        for i in range(len(lines)):
            line = lines[i].replace("\n", "")
            bn = 0
            j = 0
            for j in range(len(line)):
                if line[j] != " ":
                    break
                else:
                    bn += 1
            line = line[j:]
            level = int(bn / 3)
            node = Node(i, line, level)
            if level not in level_list:
                level_list[str(level)] = [node]
                if level > 0:
                    list = level_list[str(level - 1)]
                    list[len(list) - 1].child.append(node)
    return level_list.get("0")[0]
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
            self.arrayKind = elemTy["kind"]
        if node.kind == 'RecordK':
            for x in body:
                self.size += x.size
        if node.kind == 'IntegerK':
            self.size = 2
        if node.kind == 'CharK':
            self.size = 1

    def __str__(self):
        return str(self.__dict__)

class SymbolTable:
    def __init__(self, node, name, level, off, body=None, params=None, ifType=False):
        self.kind = node.kind
        self.name = name
        self.level = level
        self.off = off
        self.body = None
        self.params = None
        self.ifType = ifType
        if params is not None:
            self.params = params

        if body is not None:
            tmp = []
            for x in body:
                flag = False
                for i in tmp:
                    if x.name[0] == i.name:
                        flag = True
                if flag:
                    error(node.rawline, f"record {name} field member {x.name[0]} duplicated")
                    continue
                y = Kind(x)
                y.name = x.name[0]
                tmp.append(y)

            self.body = tmp
        self.typePtr = Kind(node, self.body)

    def __str__(self):
        s = ""
        if self.body is not None:
            for x in self.body:
                s += str(x.__dict__)
        return f"kind:{self.kind}, name:{self.name}, level:{self.level}, typePtr:{self.typePtr.__dict__}, body:{s}, params:{self.params}, ifType:{self.ifType}"

def CallSymbolTable(node, name, level, off, body=None, params=None, ifType=False):
    if node.kind == 'IdK':
        v = find(node.realKind, type=True)
        if v is None:
            error(node.rawline, f"unknown kind: {node.realKind}")
            return None
        tab = copy.deepcopy(v)
        tab.ifType = False
        tab.name = name
        return tab
    return SymbolTable(node, name, level, off, body=body, params=params, ifType=ifType)

all_scope = [[]]
scope = [[]]
sl = 0
off = 0

def find(name, exist=None, type=False):
    # print("----")
    # for i in range(sl, -1, -1):
    #     for x in reversed(scope[i]):
    #         print(x)
    # print("find name:", name)
    if exist is not None:
        low = sl - 1
    else:
        low = -1
    for i in range(sl, low, -1):
        for x in reversed(scope[i]):
            if name == x.name and x.ifType == type:
                return x
    return None

def ck(kind, vkind):
    if kind == "IdV" and vkind in ("IntegerK", "CharK"):
        return True
    if kind == "ArrayMembV" and vkind == "ArrayK":
        return True
    if kind == "FieldMembV" and vkind == "RecordK":
        return True
    return False

def getFieldKind(field):
    if field.kind in ("IntegerK", "CharK"):
        return field.kind
    if field.kind == "ArrayK":
        return field.arrayKind
    return None

def createName(node):
    if "varkind" in node.attr and node.attr["varkind"] == "FieldMembV":
        return node.name[0] + '.' + node.child[0].name[0]
    else:
        return node.name[0]

def getKind(node):
    if node.kind == "ConstK":
        if str.isdigit(node.name[0]):
            return "IntegerK"
        if re.match(r"\'[a-zA-Z]\'", node.name[0]):
            return "CharK"

    if node.kind == "IdK":
        kind = node.attr["varkind"]
        v = find(node.name[0])
        if v is None:
            error(node.rawline, "val find failed:", node.name[0])
            return None
        if ck(kind, v.kind) is False:
            error(node.rawline, "val kind errored:", node.name[0], kind, v.kind)
            return None
        if kind == "IdV":
            return v.kind
        if kind == "ArrayMembV":
            if len(node.child) == 1:
                x = node.child[0]
                id = x.name[0]
                l = int(v.typePtr.arrayAttr["indexTy"]["low"])
                r = int(v.typePtr.arrayAttr["indexTy"]["up"])
                if str.isdigit(id) is False:
                    if getKind(x) != "IntegerK":
                        error(node.rawline, f"array index illegal: {createName(x)}, kind: {getKind(x)}")
                elif int(id) < l or int(id) >= r:
                    error(node.rawline, "array index over range:", f"index:{id}, l:{l}, r:{r}")
            else:
                error(node.rawline, "array cant operate directed:", node.name[0])
            return v.typePtr.arrayKind
        if kind == "FieldMembV":
            nd = None
            for x in v.body:
                if x.name == node.child[0].name[0]:
                    nd = x
            if nd is None:
                error(node.rawline, f"record {node.name[0]} not have the member {node.child[0].name[0]}")
                return None
            if ck(node.child[0].attr["varkind"], nd.kind) is False:
                error(node.rawline, f"record {node.name[0]} member {node.child[0].name[0]} kind err: {nd.kind}, ",
                      node.child[0].attr["varkind"])
                return None
            for x in node.child:
                for y in x.child:
                    generate_table(y)
            return getFieldKind(nd)
    if node.kind == 'OpK':
        return operator(node, node.name[0])

def operator(node, op):
    kindList = []
    for x in node.child:
        kindList.append(generate_table(x))
    if len(kindList) == 0:
        error(node.rawline, "operate not have child")
        return None
    for i in range(len(kindList)):
        if kindList[i] is None:
            return None
        elif kindList[i] not in ("IntegerK", "CharK"):
            error(node.rawline, op, "illegal operate kind:", kindList[i])
        elif kindList[i] != kindList[0]:
            error(node.rawline, op, "operate failed:",
                  [(node.child[x].name[0], kindList[x]) for x in range(len(kindList))])
            return None
        elif op in ("+", "-", "*", "/") and kindList[i] == "CharK":
            error(node.rawline, op, "can't sub char",
                  [(node.child[x].name[0], kindList[x]) for x in range(len(kindList))])
            return None

    return kindList[0]

def generate_table(node):
    global sl, scope
    # ProK, PheadK, TypeK, VarK, ProDecK, StmLK, DecK, Stmtk, ExpK
    if node.nodeKind == "DecK":
        for x in node.name:
            if find(x, exist=True) is not None:
                error(node.rawline, "val duplicated:", x)
                continue

            body = None
            if node.kind == "RecordK":
                body = []
                for y in node.child:
                    body.append(y)

            tab = CallSymbolTable(node, x, level=sl, off=off, body=body)
            scope[sl].append(tab)
            all_scope[sl].append(tab)
            if node.kind == "RecordK":
                return
            for x in node.child:
                generate_table(x)
    elif node.nodeKind == "ProcDecK" and node.idnum > 0:
        if find(node.name[0], exist=True) is not None:
            error(node.rawline, "val duplicated:", node.name[0])
            return
        params = []
        for x in node.child:
            if x.nodeKind == "DecK":
                for y in x.name:
                    if y != " " and y != "":
                        params.append({"kind": x.kind, "name": y})
        node.kind = "ProcDecK"
        tab = CallSymbolTable(node, node.name[0], level=sl, off=off, params=params)
        scope[sl].append(tab)
        all_scope[sl].append(tab)

        sl += 1
        scope.append([])
        all_scope.append([])
        for x in node.child:
            generate_table(x)
        sl -= 1
        scope = scope[:-1]
    elif node.nodeKind == "StmtK":
        # IfK WhileK AssignK ReadK WriteK CallK ReturnK
        # print("kind:", node.kind)
        if node.kind == "CallK":
            pro = find(node.name[0])
            if pro is None:
                error(node.rawline, "procDeck find failed:", node.name[0])
                return
            elif pro.kind != "ProcDecK":
                error(node.rawline, "procDeck kind error:", node.name[0], pro.kind)
                return
            params = []
            for x in node.child:
                if x.kind == "OpK":
                    kind = operator(x, x.name[0])
                    if kind is None:
                        return
                else:
                    kind = getKind(x)
                    if kind is None:
                        error(x.rawline, "val find failed:", x.name[0])
                        return
                params.append(kind)
            proParams = [x["kind"] for x in pro.params]
            # print(params, pro.params)
            if len(params) != len(proParams):
                error(node.rawline, "call failed:", params, proParams)
                return
            for i in range(len(params)):
                if params[i] != proParams[i]:
                    error(node.rawline, "call failed:", params, proParams)
                    return
            return
        if node.kind == "IfK":
            for x in node.child:
                generate_table(x)
        if node.kind == "AssignK":
            if node.child[0].kind != "IdK":
                error(node.rawline, "AssignK left kind illegal", node.name[0])
            return operator(node, "=")
        if node.kind == "ReadK":
            if find(node.name[0]) is None:
                error(node.rawline, "val find failed:", node.name[0])
            return
        if node.kind == "WriteK":
            return operator(node, "write")
        if node.kind == "ReturnK":
            return
        if node.kind == "WhileK":
            for x in node.child:
                generate_table(x)
            return
    elif node.nodeKind == "ExpK":
        # OpK ConstK IdK
        if node.kind == "OpK":
            return operator(node, node.name[0])

        if node.kind in ("IdK", "ConstK"):
            return getKind(node)
    elif node.nodeKind == "TypeK":
        for x in node.child:
            if x.kind == "RecordK":
                generate_table(x)
                continue
            if find(x.name[0], exist=True) is not None:
                error(node.rawline, "type duplicated:", x.name[0])
                continue
            tab = CallSymbolTable(x, x.name[0], level=sl, off=off, ifType=True)
            scope[sl].append(tab)
            all_scope[sl].append(tab)
    else:
        for x in node.child:
            generate_table(x)
    return

def table_print(table):
    for i in range(len(table)):
        for x in table[i]:
            print(f"i:{i}, ", str(x))

root = None

def init():
    global root, all_scope, sl, off, flag, scope
    root = None
    all_scope = [[]]
    scope = [[]]
    sl = 0
    off = 0
    flag = False

def semantic(tree_path):
    global root
    init()
    root = generate_node(tree_path)
    visTree(root)
    generate_table(root)
    with open('../data/semanticTables.txt', "w") as f:
        for i in range(len(all_scope)):
            for x in all_scope[i]:
                f.write(f"i:{i}, " + str(x) + '\n\n')
    # print("all_scope:")
    # table_print(all_scope)
    if flag:
        return -1
    return 0
