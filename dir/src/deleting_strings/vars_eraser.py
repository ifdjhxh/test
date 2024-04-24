import ast
import random

'''
    Удаляет название переменных при объявлении или изменении их значения
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
        # if self.i == self.number or random.random() < 0.4:
        #     if random.random() < 0.5:
        #         node.value = None
        #     else:
        #         node = None
        # print(node.targets[0].id)

        if self.this_count >= self.max_count:
            return node
        if self.i == self.number or random.random() < 0.3:
            node.targets[0].id = ""
            self.this_count += 1
        self.i += 1
        return node

def varsEraser(tree):
    collection = VariableCollector()
    collection.visit(tree)
    count = collection.get_count()
    if count > 0:
        number = my_random(0, int(count - 1))
    else:
        number = 0

    replacer = ReturnArgReplace(count, number, 8)
    return replacer.visit(tree)
