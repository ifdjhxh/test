import ast

from replacing_signs import replacing_signs

from IDE_error_generation.syntax_error_generation import RewriteFunctionName

from changing_iterations.changing_iterations import ChangeIterations
from replacing_types.replacing_types import RewriteType
from function_changes import change_return, swap_parameters, scope_mistakes
from deleting_strings.erasers import eraser


class Changer:
    def __init__(self, new_tree):
        self.tree = new_tree

    def change_sign_in_logic(self, probability=0.5):
        exec_tree(self.tree)
        changer = replacing_signs.BoolOpVisitor()
        changer.set_probability(probability)
        new_tree = changer.visit(self.tree)
        new_tree = ast.fix_missing_locations(new_tree)
        changer = replacing_signs.CompareVisitor()
        changer.set_probability(probability)
        new_tree = changer.visit(self.tree)
        new_tree = ast.fix_missing_locations(new_tree)
        exec_tree(new_tree)

    def changing_iterations(self):
        exec_tree(self.tree)
        type = ChangeIterations()
        new_tree = type.visit(self.tree)
        new_tree = ast.fix_missing_locations(new_tree)
        exec_tree(new_tree)

    def replacing_types(self):
        exec_tree(self.tree)
        type = RewriteType()
        new_tree = type.visit(self.tree)
        new_tree = ast.fix_missing_locations(new_tree)
        exec_tree(new_tree)

    def change_function(self):
        exec_tree(self.tree)
        prob = swap_parameters.generate_probability()
        function_extractor = swap_parameters.FunctionNameExtractor()
        function_extractor.visit(self.tree)
        function_names = function_extractor.get_function_names()
        swapper = swap_parameters.ArgumentSwapper(function_names, prob)
        new_tree = swapper.visit(self.tree)
        exec_tree(new_tree)

        collection = change_return.VariableCollector()
        collection.visit(self.tree)
        arg_names = collection.get_args_names()
        replacer = change_return.ReturnArgReplace(arg_names)
        new_tree = replacer.visit(self.tree)
        exec_tree(new_tree)

        extractor = scope_mistakes.PrintVariableArgumentExtractor()
        new_tree = extractor.visit(self.tree)
        exec_tree(new_tree)

    def deleting_strings(self):
        exec_tree(eraser(self.tree))

    def change_function_name(self):
        exec_tree(self.tree)
        type = RewriteFunctionName()
        new_tree = type.visit(self.tree)
        new_tree = ast.fix_missing_locations(new_tree)  # надо ли?
        exec_tree(new_tree)
        return new_tree


class FileDealer:
    @staticmethod
    def open_file(file_name):
        f = open(file_name, 'r')
        text = f.read()
        return text

    @staticmethod
    def output(text, file_name="output.txt"):
        f = open(file_name, 'w')
        f.write(text)


def exec_tree(tree):

    tree_fixed = ast.fix_missing_locations(tree)
    print(ast.unparse(tree_fixed))
    FileDealer.output(ast.unparse(tree_fixed))


def switch(match):
    if match == "1":
        changer.change_function_name()
        return True
    elif match == "2":
        changer.deleting_strings()
        return True
    elif match == "3":
        changer.change_function()
        return True
    elif match == "4":
        changer.replacing_types()
        return True
    elif match == "5":
        changer.changing_iterations()
        return True
    elif match == "6":
        changer.change_sign_in_logic()
        return True
    elif match == "help":
        print("Введите цифру команды:\n 1 - Изменить названия функций \n 2 - Удалить строки \n 3 - Изменить "
              "аргументы передаваемые в функцию/возвращаемые функцией и область видимости \n 4 - Заменить тип "
              "переменных \n 5 - Изменить количество повторений в цикле for \n 6 - Поменять операции сравнения и "
              "булевы операции \n help - Для вывода подсказки \n exit - Для выхода \n")
        return True
    elif match == "exit":
        return False
    else:
        return True



if __name__ == "__main__":
    tree = ast.parse(FileDealer.open_file("code.txt"))

    changer = Changer(tree)

    choose = input("Введите цифру команды:\n 1 - Изменить названия функций \n 2 - Удалить строки \n 3 - Изменить "
                   "аргументы передаваемые в функцию/возвращаемые функцией и область видимости \n 4 - Заменить тип "
                   "переменных \n 5 - Изменить количество повторений в цикле for \n 6 - Поменять операции сравнения и "
                   "булевы операции \n help - Для вывода подсказки \n exit - Для выхода \n")

    while switch(choose):
        tree = ast.parse(FileDealer.open_file("code.txt"))
        changer = Changer(tree)
        choose = input()
