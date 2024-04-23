import ast
import random

'''logic mistakes: неверный возвращаемый аргумент в функции.
В классе VariableCollector происходит поиск всех переменных, объявленных в функциях. 
Затем в классе ReturnArgReplace осуществляется замена возвращаемого аргумента одним из списка переменных.
'''

class VariableCollector(ast.NodeVisitor):

    def __init__(self):
        self.variables = set()
        self.inside_function = False

    def visit_FunctionDef(self, node):
        self.inside_function = True
        self.generic_visit(node)
        self.inside_function = False
        # self.variables.clear()

    def visit_Assign(self, node):
        if self.inside_function:
            for target in node.targets:
                if isinstance(target, ast.Name):
                    self.variables.add(target.id)
            self.generic_visit(node)

    def get_args_names(self):
        names = self.variables
        return names



class ReturnArgReplace(ast.NodeTransformer):
    def __init__(self, args):
        self.argsuments = args

    def visit_Return(self, node):
        if isinstance(node.value, ast.Name):
            new_elem = self.choose_elem(node.value.id)
            if new_elem:
                node.value = ast.Name(id=new_elem)
        return node

    def choose_elem(self, value):
        if value in self.argsuments:
            self.argsuments.remove(value)
            return random.choice(list(self.argsuments))
        else:
            return None

