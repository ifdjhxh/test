import ast
import random
import string


class RewriteFunctionName(ast.NodeTransformer):
    """Класс, в котором переопределяются стандартные функции библиотеки AST для изменения дерева"""

    def check_if_contains_russian_letters(self, string):
        """
        Проверяет, содержит ли строка буквы русского алфавита.
        Args:
            string (str): сторока для проверки.
        Returns:
            bool: True если строка содержит кириллицу, False если нет.
        """
        russian_letters = "абвгдежзийклмнопрстуфхцчшщъыьэюя"
        for char in string:
            if char.lower() in russian_letters:
                return True
        return False

    def visit_FunctionDef(self, node):
        """
        Меняет названия определенных функций (латинские буквы на русские) с вероятностью 50%.
        Args:
            ast.node: вершины AST дерева (определения функции).
        Returns:
            ast.node: вершины AST дерева c новым название функции.
        """
        old_name = list(node.name)
        values_dictionary = {'a': 'а',
                             'c': 'с',
                             'e': 'е',
                             'o': 'о',
                             'y': 'у'}
        new_name = ''
        max_iter = 5
        # проверяем поменялись ли значения
        while not self.check_if_contains_russian_letters(new_name) and max_iter > 0:
            for i in range(len(old_name)):
                if old_name[i] in values_dictionary.keys() and random.randint(-10, 10) > 0:
                    new_name += values_dictionary[old_name[i]]
                else:
                    new_name += old_name[i]
            max_iter -= 1

        new_node = ast.FunctionDef(name=new_name, args=node.args, body=node.body, decorator_list=node.decorator_list)
        print(f"replacing function name \"{node.name}\" -> \"{new_node.name}\" at lineno: {node.lineno}")
        return new_node
