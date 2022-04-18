import os

from config.config import delimiters, reservedWords


class Token:
    def __init__(self, line, lex, sem):
        self.line = line
        self.lex = lex
        self.sem = sem


tokenList = []


def add(word, num, err=False):
    if err:
        tokenList.append(Token(num, "ERROR", word))
    elif str.isdigit(word):
        tokenList.append(Token(num, "INTC", int(word, 10)))
    elif word in delimiters:
        tokenList.append((Token(num, delimiters[word], word)))
    elif word in reservedWords:
        tokenList.append((Token(num, reservedWords[word], word)))
    elif word[0] == '\'' and word[-1] == '\'':
        tokenList.append((Token(num, "CHARC", word)))
    else:
        tokenList.append((Token(num, "ID", word)))


def work(lines):
    commentflag = False
    for num in range(0, len(lines)):
        line = lines[num].replace("\n", "", -1) + " "
        i = 0
        while i < len(line):
            c = line[i]
            if commentflag:
                if c == '}':
                    commentflag = False
            elif str.isdigit(c):
                word = c
                while str.isdigit(line[i + 1]):
                    word = word + line[i + 1]
                    i = i + 1
                add(word, num)
            elif str.isalpha(c):
                word = c
                while str.isdigit(line[i + 1]) or str.isalpha(line[i + 1]):
                    word = word + line[i + 1]
                    i = i + 1
                add(word, num)
            elif c == '.':
                if line[i + 1] == ".":
                    i = i + 1
                    add("..", num)
                else:
                    add(".", num)
            elif c == '\'':
                word = c
                i = i + 1
                while i < len(line):
                    word = word + line[i]
                    if line[i] == '\'':
                        add(word, num)
                        break
                    elif (str.isdigit(line[i]) or str.isalpha(line[i])) == False:
                        add(word, num, True)
                        break
                    i = i + 1
            elif c == '{':
                commentflag = True
            elif c == ':':
                if line[i + 1] == "=":
                    add(":=", num)
                else:
                    add(line[i] + line[i + 1], num, True)
                i = i + 1
            elif c in delimiters:
                add(c, num)
            elif c == " " or c == "	":
                _ = c
            else:
                add(line[i], num, True)
            i = i + 1
    tokenList.append(Token(len(lines), "EOF", "EOF"))
    return tokenList


def lex(pro_path, token_path):
    if not os.path.exists(pro_path):
        print(f"Open pro_path:{pro_path} failed")
        return -1
    with open(pro_path) as file:
        lines = file.readlines()
        work(lines)
        # print(f"line: {x.line}, lex: {x.lex}, sem: {x.sem}")

    with open(token_path, "w") as file:
        for x in tokenList:
            if x.sem in delimiters:
                file.write(f"{x.line} Other {x.sem}\n")
            elif x.sem in reservedWords:
                file.write(f"{x.line} Reserved_word {x.lex}\n")
            else:
                file.write(f"{x.line} {x.lex} {x.sem}\n")
    print("Generate token success")
    return 0
