import ast
import random

'''
    Удаление части строк кода или нескольких строк кода.
    В python, чтобы можно было понять, что вставить в код, пока реализовано только частичное
    или полное удаление строки return. Может приводить к ошибкам в компиляции
    из-за особенностей языка python.
'''

def my_random(min, max):
    return random.randint(min, max)


class VariableCollector(ast.NodeVisitor):

    def __init__(self):
        self.count = 0

    def visit_Return(self, node):
        self.count += 1

    def get_count(self):
        return self.count

class ReturnArgReplace(ast.NodeTransformer):
    def __init__(self, count, number):
        self.count = count
        self.number = number
        self.i = 0

    def visit_Return(self, node):
        if self.i == self.number or random.random() < 0.4:
            if random.random() < 0.5:
                node.value = None
            else:
                node = None

        self.i += 1
        return node

def returnEraser(tree):
    # print(ast.dump(tree, indent=4))
    collection = VariableCollector()
    collection.visit(tree)
    count = collection.get_count()
    # print(count)
    if count > 0:
        number = my_random(0, int(count - 1))
    else:
        number = 0
    replacer = ReturnArgReplace(count, number)
    # print(number)
    return replacer.visit(tree)

