import ast
import random

'''
    Удаление параметров, которые передаются в функцию (удаляются только параметры, представляющие
    собой переменные)
'''

def my_random(min, max):
    return random.randint(min, max)

class VariableCollector(ast.NodeVisitor):

    def __init__(self):
        self.count = 0

    def visit_Call(self, node):

        self.count += 1

    def get_count(self):
        return self.count

class ReturnArgReplace(ast.NodeTransformer):
    def __init__(self, count, number, max_count):
        self.max_count = max_count
        self.this_count = 0
        self.count = count
        self.number = number
        self.i = 0

    def visit_Call(self, node):
        len_args = len(node.args)
        j = 0
        alpha = 0.7/len_args
        for i in range(len_args):
            # print("Type = ", end="")
            # print(type(node.args[j]), end="\t")
            if str(type(node.args[j])) != "<class 'ast.Name'>":
                continue
            if random.random() < alpha:
                node.args.pop(j)
                j -= 1
            j += 1
        return node

def callParamsEraser(tree):
    collection = VariableCollector()
    collection.visit(tree)
    count = collection.get_count()
    if count > 0:
        number = my_random(0, int(count - 1))
    else:
        number = 0
    # print(count)

    replacer = ReturnArgReplace(count, number, 2)
    return replacer.visit(tree)

