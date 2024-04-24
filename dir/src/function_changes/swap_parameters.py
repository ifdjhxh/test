import ast
import random
import math

'''logic mistakes: неправильный порядок аргументов, подаваемых в функцию
В классе FunctionNameExtractor происходит поиск имен созданных функций. Класс ArgumentSwapper отвечает за изменение порядка аргументов. Изменения будут происходить в зависимости от поданой вероятности. Если вероятность < 0.6, произойдет изменение порядка аргументов, поданных при вызове функции, если больше, то аргументы затрутся.
'''

def generate_probability():
    return round(random.random(), 1)

class FileDealer:
    def open_file(self, file_name):
        f = open(file_name, 'r')
        text = f.read()
        # print(text)
        return text

    def output(self, text, file_name="output.txt"):
        f = open(file_name, 'w')
        f.write(text)

class FunctionNameExtractor(ast.NodeVisitor):

    def __init__(self):
        self.function_names = []

    def visit_FunctionDef(self, node):
        self.function_names.append(node.name)
        self.generic_visit(node)

    def get_function_names(self):
        names = self.function_names
        return names

class ArgumentSwapper(ast.NodeTransformer):
    def __init__(self, function_names, prob):
        self.function_names = function_names
        self.argsuments = []
        self.probability = prob
        self.count = 0

    def visit_Call(self, node):
        if isinstance(node.func, ast.Name) and node.func.id in self.function_names:
            if self.probability<0.6 and len(node.args) != 1 and self.count <= math.ceil(self.probability*len(self.function_names)):
                self.count += 1
                for arg in node.args:
                    self.argsuments.append(arg)
                temp = list(self.argsuments)
                random.shuffle(self.argsuments)
                if temp == self.argsuments:
                    new_args = self.argsuments[::-1]
                else:
                    new_args = self.argsuments
                node.args = new_args
                self.argsuments = []
            elif len(node.args) != 0 and self.count < math.ceil(self.probability*len(self.function_names)/2):
                n = math.ceil(self.probability * len(self.function_names) / 2)
                self.count += 1
                node.args = []
        return node

