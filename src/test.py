class Node:
    def __init__(self):
        self.x = 1


tmp = Node()
list = []
list.append(tmp)
list.append(tmp)
print(list[1].x, list[0].x)
tmp.x = 2
print(list[1].x, list[0].x)
