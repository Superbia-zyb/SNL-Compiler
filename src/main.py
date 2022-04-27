from LL1 import LL1
from LexicalaAnalyzer import lex
from Recursion import recurse
from SemanticAnalysis import semantic

pro_path = "../data/program.txt"
token_path = "../data/token.txt"
tree_path = "../data/syntax_tree.txt"
gram_path = "../data/grammar.txt"

def work(col=1):
    err = lex(pro_path, token_path)
    if err != 0:
        return False
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
        return False
    print("Gramma analysis success")
    err = semantic(tree_path)
    if err != 0:
        print("Semantic analysis failed")
    else:
        print("Semantic analysis success")
    return True

# work(1)
#work(1)

if __name__ == '__main__':
    work()
