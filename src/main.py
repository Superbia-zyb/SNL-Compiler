from LL1 import LL1
from LexicalaAnalyzer import lex
from Recursion import recurse
from SemanticAnalysis import semantic

pro_path = "../data/p2.txt"
token_path = "../data/token.txt"
tree_path = "../data/syntax_tree.txt"
gram_path = "../data/grammar.txt"

def work(col=1):
    err = lex(pro_path, token_path)
    if err != 0:
        return
    message = ""
    if col:
        # err = ll1(token_path, tree_path)
        ll1 = LL1(gram_path, token_path, tree_path)
        ll1.run()
        err, message = ll1.showError(show=True)
    else:
        err = recurse(token_path)
    if err != 0:
        print("Gramma analysis failed")
        return
    print("Gramma analysis success")
    err = semantic(tree_path)
    if err != 0:
        print("Semantic analysis failed")
        return
    print("Semantic analysis success")

work(1)
