import ast
import random

'''
    Удаление некоторых элементов списка
'''

def my_random(min, max):
    return random.randint(min, max)

class VariableCollector(ast.NodeVisitor):

    def __init__(self):
        self.count = 0

    def visit_Assign(self, node):

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

    def visit_Assign(self, node):
        test = self.visit(node.value)
        if isinstance(node.value, ast.List):
            # print(test.elts)
            len_args = len(test.elts)
            j = 0
            alpha = 0.9 / len_args
            if alpha * 2 < 1 and random.random() < 0.7:
                alpha *= 2
            for i in range(len_args):
                if random.random() < alpha:
                    test.elts.pop(j)
                    j-=1
                j += 1

        return node

def listEraser(tree):
    collection = VariableCollector()
    collection.visit(tree)
    count = collection.get_count()
    if count > 0:
        number = my_random(0, int(count - 1))
    else:
        number = 0

    replacer = ReturnArgReplace(count, number, 2)
    return replacer.visit(tree)
