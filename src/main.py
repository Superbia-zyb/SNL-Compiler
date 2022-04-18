from LL1 import ll1
from LexicalaAnalyzer import lex
from Recursion import recurse
from SemanticAnalysis import semantic

pro_path = "../data/p1.txt"
token_path = "../data/token.txt"
tree_path = "../data/syntax_tree.txt"


def work(col=1):
    err = lex(pro_path, token_path)
    if err != 0:
        return
    if col:
        err = ll1(token_path, tree_path)
    else:
        err = recurse(token_path)
    if err != 0:
        return
    print("Gramma alalysis success")
    err = semantic(tree_path)


work(0)
