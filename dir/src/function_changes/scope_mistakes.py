import ast
import random

'''logic mistakes: ошибки, связанные с областью видимости.
Для использования этого функционала в созданной функции должна быть объявлена переменная и вывод её с помощью print.
В функции main создается переменная с таким же именем, как и у переменной из функции.
Затем эта переменная выводится. Соответственно, если вызвать функцию, то значение этой переменной будет иным.
'''

class PrintVariableArgumentExtractor(ast.NodeVisitor):

    def __init__(self):
        self.argument = None

    def visit_FunctionDef(self, node):
        for stmt in node.body:
            if isinstance(stmt, ast.Expr) and isinstance(stmt.value, ast.Call) and isinstance(stmt.value.func, ast.Name) and stmt.value.func.id == 'print':
                if len(stmt.value.args) > 0:
                    l = len(stmt.value.args)
                    for arg in stmt.value.args:
                        if isinstance(arg, ast.Name):
                            self.argument = arg.id
                            return node
                        # Дополнительно можно обработать другие типы переменных
        self.generic_visit(node)

    def visit_Module(self, node):
        if not self.argument:
            self.generic_visit(node)
            # Создаем узел для новой переменной
            random_var = random.randint(1, 100)
            random_var_node = ast.Assign(targets=[ast.Name(id=self.argument, ctx=ast.Store())],
                                         value=ast.Num(n=random_var), lineno=0, col_offset=0)
            node.body.append(random_var_node)
            # Создаем узел для новой функции print
            print_node = ast.Expr(value=ast.Call(func=ast.Name(id='print', ctx=ast.Load()),
                                                 args=[ast.Name(id=self.argument, ctx=ast.Load())],
                                                 keywords=[]), lineno=0, col_offset=0)
            node.body.append(print_node)
        return node

