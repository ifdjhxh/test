import ast
import random

'''logic mistakes: неправильный порядок аргументов, подаваемых в функцию
В классе FunctionNameExtractor происходит поиск имен созданных функций. Класс ArgumentSwapper отвечает за изменение порядка аргументов. Изменения будут происходить во всех найденных функциях. Если после изменения порядка случайным образом аргументы остались на тех же местах, то их порядок будет изменен на обратный.
'''

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
    def __init__(self, function_names):
        self.function_names = function_names
        self.argsuments = []

    def visit_Call(self, node):
        if isinstance(node.func, ast.Name) and node.func.id in self.function_names and len(node.args) != 1:
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
        return node

if __name__ == "__main__":
    fileDealer = FileDealer()
    tree = ast.parse(fileDealer.open_file("code.txt"))
    function_extractor = FunctionNameExtractor()
    function_extractor.visit(tree)
    function_names = function_extractor.get_function_names()
    swapper = ArgumentSwapper(function_names)
    new_tree = swapper.visit(tree)
    fileDealer.output(ast.unparse(new_tree))

