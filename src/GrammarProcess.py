from config.LL1_config import Node


def Priosity(op):
    if op == 'END':
        pri = 0
    elif op == '<' or op == '=':
        pri = 1
    elif op == '+' or op == '-':
        pri = 2
    elif op == '*' or op == '/':
        pri = 3
    else:
        pri = -1
    return pri


def judgeType(op):
    a = ['+', '-', '*', '/', '=', '<']
    if op in a:
        b = 'OpK'
    elif op.isdigit() or ('\'' in op and len(op) == 3):
        b = 'ConstK'
    else:
        b = 'IdK'
    return b


def copyNode(x, y):
    x.nodeKind = y.nodeKind
    x.child = y.child
    x.Sibling = y.Sibling
    x.Lineno = y.Lineno
    x.kind = y.kind
    x.idnum = y.idnum  # 一个节点中的标识符的个数
    x.name = y.name
    x.type_name = y.type_name
    x.attr = y.attr
    x.judge = y.judge


def process1(Tree, toke, preNode):
    # Program ::= ProgramHead DeclarePart ProgramBody .
    return preNode


def process2(Tree, toke, preNode):
    # ProgramHead ::= PROGRAM ProgramName
    PheadK = Tree.stack.pop()
    PheadK.Lineno = toke[0]
    PheadK.judge = True
    return PheadK


def process3(Tree, toke, preNode):
    # ProgramName ::= ID
    preNode.name.append(str(toke[2]))
    preNode.idnum += 1
    return preNode


def process4(Tree, toke, preNode):
    return preNode


def process5(Tree, toke, preNode):
    return preNode


def process6(Tree, toke, preNode):
    return preNode


def process7(Tree, toke, preNode):
    TypeK = Tree.stack.pop()
    TypeK.Lineno = toke[0]
    TypeK.judge = True
    TypeK.child.append(Node('DecK'))
    TypeK.Sibling = Node('VarK')
    Tree.stack.push(TypeK.Sibling)
    Tree.stack.push(TypeK.child[0])
    return TypeK


def process8(Tree, toke, preNode):
    DecK = Tree.stack.pop()
    DecK.Lineno = toke[0]
    DecK.judge = True
    DecK.Sibling = Node('DecK')
    Tree.stack.push(DecK.Sibling)
    return DecK


def process9(Tree, toke, preNode):
    Tree.stack.pop()
    return preNode


def process10(Tree, toke, preNode):
    return preNode


def process11(Tree, toke, preNode):
    preNode.name.append(str(toke[2]))
    preNode.idnum += 1
    return preNode


def process12(Tree, toke, preNode):
    return preNode


def process13(Tree, toke, preNode):
    return preNode


def process14(Tree, toke, preNode):
    preNode.kind['dec'] = 'IdK'
    preNode.name.append(str(toke[2]))
    preNode.idnum += 1
    return preNode


def process15(Tree, toke, preNode):
    if preNode.kind['dec'] == 'ArrayK':
        preNode.attr[0]['childType'] = 'IntegerK'
    else:
        preNode.kind['dec'] = 'IntegerK'
    return preNode


def process16(Tree, toke, preNode):
    if preNode.kind['dec'] == 'ArrayK':
        preNode.attr[0]['childType'] = 'CharK'
    else:
        preNode.kind['dec'] = 'CharK'
    return preNode


def process17(Tree, toke, preNode):
    return preNode


def process18(Tree, toke, preNode):
    return preNode


def process19(Tree, toke, preNode):
    preNode.kind['dec'] = 'ArrayK'
    return preNode


def process20(Tree, toke, preNode):
    preNode.attr[0]['low'] = toke[2]
    return preNode


def process21(Tree, toke, preNode):
    preNode.attr[0]['up'] = toke[2]
    return preNode


def process22(Tree, toke, preNode):
    preNode.kind['dec'] = 'RecordK'
    preNode.Lineno = toke[0]
    preNode.child.append(Node('DecK'))
    Tree.stack.push(preNode)
    Tree.stack.push(preNode.child[0])
    return preNode


def process23(Tree, toke, preNode):
    DecK = Tree.stack.pop()
    DecK.Lineno = toke[0]
    DecK.judge = True
    DecK.Sibling = Node('DecK')
    Tree.stack.push(DecK.Sibling)
    return DecK


def process24(Tree, toke, preNode):
    DecK = Tree.stack.pop()
    DecK.Lineno = toke[0]
    DecK.judge = True
    DecK.Sibling = Node('DecK')
    Tree.stack.push(DecK.Sibling)
    return DecK


def process25(Tree, toke, preNode):
    Tree.stack.pop()
    preNode = Tree.stack.pop()
    # preNode.Lineno = toke[0]
    preNode.judge = True
    return preNode


def process26(Tree, toke, preNode):
    return preNode


def process27(Tree, toke, preNode):
    preNode.name.append(toke[2])
    preNode.idnum += 1
    return preNode


def process28(Tree, toke, preNode):
    return preNode


def process29(Tree, toke, preNode):
    return preNode


def process30(Tree, toke, preNode):
    return preNode


def process31(Tree, toke, preNode):
    return preNode


def process32(Tree, toke, preNode):
    VarK = Tree.stack.pop()
    if VarK.nodeKind == 'TypeK':
        VarK.Sibling = Node('VarK')
        VarK = VarK.Sibling
    VarK.judge = True
    VarK.Lineno = toke[0]
    VarK.child.append(Node('DecK'))
    VarK.Sibling = Node('ProcDecK')
    Tree.stack.push(VarK.Sibling)
    Tree.stack.push(VarK.child[0])
    return VarK


def process33(Tree, toke, preNode):
    DecK = Tree.stack.pop()
    DecK.Lineno = toke[0]
    DecK.judge = True
    DecK.Sibling = Node('DecK')
    Tree.stack.push(DecK.Sibling)
    return DecK


def process34(Tree, toke, preNode):
    Tree.stack.pop()
    return preNode


def process35(Tree, toke, preNode):
    return preNode


def process36(Tree, toke, preNode):
    preNode.name.append(toke[2])
    preNode.idnum += 1
    return preNode


def process37(Tree, toke, preNode):
    return preNode


def process38(Tree, toke, preNode):
    return preNode


def process39(Tree, toke, preNode):
    return preNode


def process40(Tree, toke, preNode):
    return preNode


def process41(Tree, toke, preNode):
    ProcDecK = Tree.stack.pop()
    if ProcDecK == 'VarK':
        ProcDecK.Sibling = Node('ProcDecK')
        ProcDecK = ProcDecK.Sibling
    elif ProcDecK == 'TypeK':
        ProcDecK.Sibling = Node('VarK')
        ProcDecK = ProcDecK.Sibling
        ProcDecK.Sibling = Node('ProcDecK')
        ProcDecK = ProcDecK.Sibling
    ProcDecK.judge = True
    ProcDecK.Lineno = toke[0]
    ProcDecK.child.append(Node('DecK'))
    ProcDecK.child.append(Node('TypeK'))
    ProcDecK.child.append(Node('StmLK'))
    ProcDecK.Sibling = Node('ProcDecK')
    Tree.stack.push(ProcDecK.Sibling)
    Tree.stack.push(ProcDecK.child[2])
    Tree.stack.push(ProcDecK.child[1])
    Tree.stack.push(ProcDecK.child[0])
    return ProcDecK


def process42(Tree, toke, preNode):
    return preNode


def process43(Tree, toke, preNode):
    return preNode


def process44(Tree, toke, preNode):
    preNode.name.append(toke[2])
    preNode.idnum += 1
    return preNode


def process45(Tree, toke, preNode):
    Tree.stack.pop()
    return preNode


def process46(Tree, toke, preNode):
    return preNode


def process47(Tree, toke, preNode):
    return preNode


def process48(Tree, toke, preNode):  # ???/??/?????????/
    Tree.stack.pop()
    return preNode


def process49(Tree, toke, preNode):
    return preNode


def process50(Tree, toke, preNode):
    DecK = Tree.stack.pop()
    DecK.Lineno = toke[0]
    DecK.judge = True
    DecK.attr[1]['paramt'] = 'valparamType'
    DecK.Sibling = Node('DecK')
    Tree.stack.push(DecK.Sibling)
    return DecK


def process51(Tree, toke, preNode):
    DecK = Tree.stack.pop()
    DecK.Lineno = toke[0]
    DecK.judge = True
    DecK.attr[1]['paramt'] = 'varparamtype'
    DecK.Sibling = Node('DecK')
    Tree.stack.push(DecK.Sibling)
    return DecK


def process52(Tree, toke, preNode):
    preNode.name.append(toke[2])
    preNode.idnum += 1
    return preNode


def process53(Tree, toke, preNode):
    return preNode


def process54(Tree, toke, preNode):
    return preNode


def process55(Tree, toke, preNode):
    return preNode


def process56(Tree, toke, preNode):
    return preNode


def process57(Tree, toke, preNode):
    Tree.stack.pop()
    StmLK = Tree.stack.pop()
    StmLK.Lineno = toke[0]
    StmLK.judge = True
    StmLK.child.append(Node('StmtK'))
    Tree.stack.push(StmLK.child[0])
    return StmLK


def process58(Tree, toke, preNode):
    return preNode


def process59(Tree, toke, preNode):
    Tree.stack.pop()
    return preNode


def process60(Tree, toke, preNode):
    return preNode


def process61(Tree, toke, preNode):
    StmtK = Tree.stack.pop()
    StmtK.Lineno = toke[0]
    StmtK.judge = True
    StmtK.kind['stmt'] = 'IfK'
    StmtK.Sibling = Node('StmtK')
    Tree.stack.push(StmtK.Sibling)
    return StmtK


def process62(Tree, toke, preNode):
    StmtK = Tree.stack.pop()
    StmtK.Lineno = toke[0]
    StmtK.judge = True
    StmtK.kind['stmt'] = 'WhileK'
    StmtK.Sibling = Node('StmtK')
    Tree.stack.push(StmtK.Sibling)
    return StmtK


def process63(Tree, toke, preNode):
    StmtK = Tree.stack.pop()
    StmtK.Lineno = toke[0]
    StmtK.judge = True
    StmtK.kind['stmt'] = 'ReadK'
    StmtK.Sibling = Node('StmtK')
    Tree.stack.push(StmtK.Sibling)
    return StmtK


def process64(Tree, toke, preNode):
    StmtK = Tree.stack.pop()
    StmtK.Lineno = toke[0]
    StmtK.judge = True
    StmtK.kind['stmt'] = 'WriteK'
    StmtK.Sibling = Node('StmtK')
    Tree.stack.push(StmtK.Sibling)
    return StmtK


def process65(Tree, toke, preNode):
    StmtK = Tree.stack.pop()
    StmtK.Lineno = toke[0]
    StmtK.judge = True
    StmtK.kind['stmt'] = 'ReturnK'
    StmtK.Sibling = Node('StmtK')
    Tree.stack.push(StmtK.Sibling)
    return StmtK


def process66(Tree, toke, preNode):
    StmtK = Tree.stack.pop()
    StmtK.Lineno = toke[0]
    StmtK.judge = True
    StmtK.child.append(Node('ExpK'))
    StmtK.child[0].name.append(toke[2])
    StmtK.child[0].Lineno = toke[0]
    StmtK.child[0].idnum += 1
    StmtK.child[0].judge = True
    StmtK.child[0].kind['exp'] = judgeType(toke[2])
    StmtK.Sibling = Node('StmtK')
    Tree.stack.push(StmtK.Sibling)
    return StmtK


def process67(Tree, toke, preNode):
    preNode.kind['stmt'] = 'AssignK'
    return preNode


def process68(Tree, toke, preNode):
    preNode.kind['stmt'] = 'CallK'
    preNode.name.append(preNode.child[0].name[0])
    preNode.idnum += 1
    preNode.child[0].attr[2]['varkind'] = 'IdV'
    preNode.child[0].judge = False
    return preNode


def process69(Tree, toke, preNode):
    preNode.child.append(Node('ExpK'))
    Tree.stack.push(preNode.child[1])
    t = Node('ExpK')
    t.name.append('END')
    Tree.SignStack.push(t)
    return preNode.child[0]


def process70(Tree, toke, preNode):
    preNode.child.append(Node('ExpK'))
    preNode.child.append(Node('StmtK'))
    preNode.child.append(Node('StmtK'))
    Tree.stack.push(preNode.child[2])
    Tree.stack.push(preNode.child[1])
    Tree.stack.push(preNode.child[0])
    return preNode


def process71(Tree, toke, preNode):
    preNode.child.append(Node('ExpK'))
    preNode.child.append(Node('StmtK'))
    Tree.stack.push(preNode.child[1])
    Tree.stack.push(preNode.child[0])
    return preNode


def process72(Tree, toke, preNode):
    return preNode


def process73(Tree, toke, preNode):
    preNode.name.append(toke[2])
    preNode.idnum += 1
    return preNode


def process74(Tree, toke, preNode):
    preNode.child.append(Node('ExpK'))
    Tree.stack.push(preNode.child[0])
    t = Node('ExpK')
    t.name.append('END')
    Tree.SignStack.push(t)
    return preNode


def process75(Tree, toke, preNode):
    return preNode


def process76(Tree, toke, preNode):
    preNode.child.append(Node('ExpK'))
    Tree.stack.push(preNode.child[1])
    return preNode


def process77(Tree, toke, preNode):
    Tree.stack.pop()
    return preNode


def process78(Tree, toke, preNode):
    t = Node('ExpK')
    t.name.append('END')
    Tree.SignStack.push(t)
    return preNode


def process79(Tree, toke, preNode):
    return preNode


def process80(Tree, toke, preNode):
    preNode.Sibling = Node('ExpK')
    Tree.stack.push(preNode.Sibling)
    return preNode


def process81(Tree, toke, preNode):
    t = Node('ExpK')
    t.name.append('END')
    Tree.SignStack.push(t)
    Tree.getExpResult = False
    return preNode


def process82(Tree, toke, preNode):  # ???//????/
    currentP = Node('ExpK')
    currentP.name.append(toke[2])
    currentP.Lineno = toke[0]
    currentP.idnum += 1
    currentP.judge = True
    currentP.kind['exp'] = judgeType(toke[2])
    while Priosity(Tree.SignStack.peek().name[0]) >= Priosity(currentP.name[0]):
        t = Tree.SignStack.pop()
        Rnum = Tree.NumStack.pop()
        Lnum = Tree.NumStack.pop()
        t.judge = True
        Lnum.judge = True
        Rnum.judge = True
        t.child.append(Lnum)
        t.child.append(Rnum)
        Tree.NumStack.push(t)
    Tree.SignStack.push(currentP)
    Tree.getExpResult = True
    return currentP


def process83(Tree, toke, preNode):
    return preNode


def process84(Tree, toke, preNode):
    if toke[2] == ')' and Tree.expflag != 0:
        while Tree.SignStack.peek().name[0] != '(':
            t = Tree.SignStack.pop()
            Rnum = Tree.NumStack.pop()
            Lnum = Tree.NumStack.pop()
            t.judge = True
            Lnum.judge = True
            Rnum.judge = True
            t.child.append(Lnum)
            t.child.append(Rnum)
            Tree.NumStack.push(t)
        Tree.SignStack.pop()
        Tree.expflag -= 1
    else:
        if Tree.getExpResult or Tree.getExpResult2:
            while Tree.SignStack.peek().name[0] != 'END':
                t = Tree.SignStack.pop()
                Rnum = Tree.NumStack.pop()
                Lnum = Tree.NumStack.pop()
                t.judge = True
                Lnum.judge = True
                Rnum.judge = True
                t.child.append(Lnum)
                t.child.append(Rnum)
                Tree.NumStack.push(t)
            Tree.SignStack.pop()
            currentP = Tree.stack.pop()
            t1 = Tree.NumStack.pop()
            copyNode(currentP, t1)
            Tree.getExpResult2 = False
            preNode = currentP
    return preNode


def process85(Tree, toke, preNode):
    currentP = Node('ExpK')
    currentP.name.append(toke[2])
    currentP.Lineno = toke[0]
    currentP.idnum += 1
    currentP.judge = True
    currentP.kind['exp'] = judgeType(toke[2])
    while Priosity(Tree.SignStack.peek().name[0]) >= Priosity(currentP.name[0]):
        t = Tree.SignStack.pop()
        Rnum = Tree.NumStack.pop()
        Lnum = Tree.NumStack.pop()
        t.judge = True
        Lnum.judge = True
        Rnum.judge = True
        t.child.append(Lnum)
        t.child.append(Rnum)
        Tree.NumStack.push(t)
    Tree.SignStack.push(currentP)
    return currentP


def process86(Tree, toke, preNode):
    return preNode


def process87(Tree, toke, preNode):
    return preNode


def process88(Tree, toke, preNode):
    currentP = Node('ExpK')
    currentP.name.append(toke[2])
    currentP.Lineno = toke[0]
    currentP.idnum += 1
    currentP.judge = True
    currentP.kind['exp'] = judgeType(toke[2])
    while Priosity(Tree.SignStack.peek().name[0]) >= Priosity(currentP.name[0]):
        t = Tree.SignStack.pop()
        Rnum = Tree.NumStack.pop()
        Lnum = Tree.NumStack.pop()
        t.judge = True
        Lnum.judge = True
        Rnum.judge = True
        t.child.append(Lnum)
        t.child.append(Rnum)
        Tree.NumStack.push(t)
    Tree.SignStack.push(currentP)
    return currentP


def process89(Tree, toke, preNode):
    currentP = Node('ExpK')
    currentP.name.append('(')
    currentP.Lineno = toke[0]
    Tree.SignStack.push(currentP)
    Tree.expflag += 1
    return currentP


def process90(Tree, toke, preNode):
    currentP = Node('ExpK')
    currentP.name.append(toke[2])
    currentP.Lineno = toke[0]
    currentP.idnum += 1
    currentP.judge = True
    currentP.kind['exp'] = judgeType(toke[2])
    Tree.NumStack.push(currentP)
    return currentP


def process91(Tree, toke, preNode):
    currentP = Node('ExpK')
    currentP.name.append(toke[2])
    currentP.Lineno = toke[0]
    currentP.idnum += 1
    currentP.judge = True
    currentP.kind['exp'] = judgeType(toke[2])
    Tree.NumStack.push(currentP)
    return currentP


def process92(Tree, toke, preNode):
    return preNode


def process93(Tree, toke, preNode):  # ??????????
    t = Node('ExpK')
    t.name.append(toke[2])
    t.Lineno = toke[0]
    t.idnum += 1
    t.judge = True
    Tree.NumStack.push(t)
    return t


def process94(Tree, toke, preNode):
    preNode.kind['exp'] = 'IdK'
    preNode.attr[2]['varkind'] = 'IdV'
    return preNode


def process95(Tree, toke, preNode):
    preNode.kind['exp'] = 'IdK'
    preNode.attr[2]['varkind'] = 'ArrayMembV'
    preNode.child.append(Node('ExpK'))
    Tree.stack.push(preNode.child[0])
    t = Node('ExpK')
    t.name.append('END')
    Tree.SignStack.push(t)
    Tree.getExpResult2 = True
    return preNode


def process96(Tree, toke, preNode):
    preNode.kind['exp'] = 'IdK'
    preNode.attr[2]['varkind'] = 'FieldMembV'
    preNode.child.append(Node('ExpK'))
    Tree.stack.push(preNode.child[0])
    return preNode


def process97(Tree, toke, preNode):
    ExpK = Tree.stack.pop()
    ExpK.Lineno = toke[0]
    ExpK.judge = True
    ExpK.name.append(toke[2])
    ExpK.idnum += 1
    ExpK.kind['exp'] = 'IdK'
    return ExpK


def process98(Tree, toke, preNode):
    preNode.attr[2]['varkind'] = 'IdV'
    return preNode


def process99(Tree, toke, preNode):
    preNode.attr[2]['varkind'] = 'ArrayMembV'
    preNode.child.append(Node('ExpK'))
    Tree.stack.push(preNode.child[0])
    t = Node('ExpK')
    t.name.append('END')
    Tree.SignStack.push(t)
    Tree.getExpResult2 = True
    return preNode


def process100(Tree, toke, preNode):
    return preNode


def process101(Tree, toke, preNode):
    return preNode


def process102(Tree, toke, preNode):
    return preNode


def process103(Tree, toke, preNode):
    return preNode


def process104(Tree, toke, preNode):
    return preNode


def process105(Tree, toke, preNode):
    return preNode


def predict1(num, tree, toke, preNode):
    if num == 1:
        t = process1(tree, toke, preNode)
    elif num == 2:
        t = process2(tree, toke, preNode)
    elif num == 3:
        t = process3(tree, toke, preNode)
    elif num == 4:
        t = process4(tree, toke, preNode)
    elif num == 5:
        t = process5(tree, toke, preNode)
    elif num == 6:
        t = process6(tree, toke, preNode)
    elif num == 7:
        t = process7(tree, toke, preNode)
    elif num == 8:
        t = process8(tree, toke, preNode)
    elif num == 9:
        t = process9(tree, toke, preNode)
    elif num == 10:
        t = process10(tree, toke, preNode)
    elif num == 11:
        t = process11(tree, toke, preNode)
    elif num == 12:
        t = process12(tree, toke, preNode)
    elif num == 13:
        t = process13(tree, toke, preNode)
    elif num == 14:
        t = process14(tree, toke, preNode)
    elif num == 15:
        t = process15(tree, toke, preNode)
    elif num == 16:
        t = process16(tree, toke, preNode)
    elif num == 17:
        t = process17(tree, toke, preNode)
    elif num == 18:
        t = process18(tree, toke, preNode)
    elif num == 19:
        t = process19(tree, toke, preNode)
    elif num == 20:
        t = process20(tree, toke, preNode)
    elif num == 21:
        t = process21(tree, toke, preNode)
    elif num == 22:
        t = process22(tree, toke, preNode)
    elif num == 23:
        t = process23(tree, toke, preNode)
    elif num == 24:
        t = process24(tree, toke, preNode)
    elif num == 25:
        t = process25(tree, toke, preNode)
    elif num == 26:
        t = process26(tree, toke, preNode)
    elif num == 27:
        t = process27(tree, toke, preNode)
    elif num == 28:
        t = process28(tree, toke, preNode)
    elif num == 29:
        t = process29(tree, toke, preNode)
    elif num == 30:
        t = process30(tree, toke, preNode)
    elif num == 31:
        t = process31(tree, toke, preNode)
    elif num == 32:
        t = process32(tree, toke, preNode)
    elif num == 33:
        t = process33(tree, toke, preNode)
    elif num == 34:
        t = process34(tree, toke, preNode)
    elif num == 35:
        t = process35(tree, toke, preNode)
    elif num == 36:
        t = process36(tree, toke, preNode)
    elif num == 37:
        t = process37(tree, toke, preNode)
    elif num == 38:
        t = process38(tree, toke, preNode)
    elif num == 39:
        t = process39(tree, toke, preNode)
    elif num == 40:
        t = process40(tree, toke, preNode)
    elif num == 41:
        t = process41(tree, toke, preNode)
    elif num == 42:
        t = process42(tree, toke, preNode)
    elif num == 43:
        t = process43(tree, toke, preNode)
    elif num == 44:
        t = process44(tree, toke, preNode)
    elif num == 45:
        t = process45(tree, toke, preNode)
    elif num == 46:
        t = process46(tree, toke, preNode)
    elif num == 47:
        t = process47(tree, toke, preNode)
    elif num == 48:
        t = process48(tree, toke, preNode)
    elif num == 49:
        t = process49(tree, toke, preNode)
    elif num == 50:
        t = process50(tree, toke, preNode)
    elif num == 51:
        t = process51(tree, toke, preNode)
    elif num == 52:
        t = process52(tree, toke, preNode)
    elif num == 53:
        t = process53(tree, toke, preNode)
    elif num == 54:
        t = process54(tree, toke, preNode)
    elif num == 55:
        t = process55(tree, toke, preNode)
    elif num == 56:
        t = process56(tree, toke, preNode)
    elif num == 57:
        t = process57(tree, toke, preNode)
    elif num == 58:
        t = process58(tree, toke, preNode)
    elif num == 59:
        t = process59(tree, toke, preNode)
    elif num == 60:
        t = process60(tree, toke, preNode)
    elif num == 61:
        t = process61(tree, toke, preNode)
    elif num == 62:
        t = process62(tree, toke, preNode)
    elif num == 63:
        t = process63(tree, toke, preNode)
    elif num == 64:
        t = process64(tree, toke, preNode)
    elif num == 65:
        t = process65(tree, toke, preNode)
    elif num == 66:
        t = process66(tree, toke, preNode)
    elif num == 67:
        t = process67(tree, toke, preNode)
    elif num == 68:
        t = process68(tree, toke, preNode)
    elif num == 69:
        t = process69(tree, toke, preNode)
    elif num == 70:
        t = process70(tree, toke, preNode)
    elif num == 71:
        t = process71(tree, toke, preNode)
    elif num == 72:
        t = process72(tree, toke, preNode)
    elif num == 73:
        t = process73(tree, toke, preNode)
    elif num == 74:
        t = process74(tree, toke, preNode)
    elif num == 75:
        t = process75(tree, toke, preNode)
    elif num == 76:
        t = process76(tree, toke, preNode)
    elif num == 77:
        t = process77(tree, toke, preNode)
    elif num == 78:
        t = process78(tree, toke, preNode)
    elif num == 79:
        t = process79(tree, toke, preNode)
    elif num == 80:
        t = process80(tree, toke, preNode)
    elif num == 81:
        t = process81(tree, toke, preNode)
    elif num == 82:
        t = process82(tree, toke, preNode)
    elif num == 83:
        t = process83(tree, toke, preNode)
    elif num == 84:
        t = process84(tree, toke, preNode)
    elif num == 85:
        t = process85(tree, toke, preNode)
    elif num == 86:
        t = process86(tree, toke, preNode)
    elif num == 87:
        t = process87(tree, toke, preNode)
    elif num == 88:
        t = process88(tree, toke, preNode)
    elif num == 89:
        t = process89(tree, toke, preNode)
    elif num == 90:
        t = process90(tree, toke, preNode)
    elif num == 91:
        t = process91(tree, toke, preNode)
    elif num == 92:
        t = process92(tree, toke, preNode)
    elif num == 93:
        t = process93(tree, toke, preNode)
    elif num == 94:
        t = process94(tree, toke, preNode)
    elif num == 95:
        t = process95(tree, toke, preNode)
    elif num == 96:
        t = process96(tree, toke, preNode)
    elif num == 97:
        t = process97(tree, toke, preNode)
    elif num == 98:
        t = process98(tree, toke, preNode)
    elif num == 99:
        t = process99(tree, toke, preNode)
    elif num == 100:
        t = process100(tree, toke, preNode)
    elif num == 101:
        t = process101(tree, toke, preNode)
    elif num == 102:
        t = process102(tree, toke, preNode)
    elif num == 103:
        t = process103(tree, toke, preNode)
    elif num == 104:
        t = process104(tree, toke, preNode)
    elif num == 105:
        t = process105(tree, toke, preNode)
    return t

# syntax_tree = Tree()
# process2(syntax_tree, 1)
# print(syntax_tree.root.child[1].judge)
