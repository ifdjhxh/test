import ast
import random

'''
001 версия подтипа "Синтаксис: изменение кол-ва переменных"
Программа изменяет кол-во итераций в цикле for c вероятностью 100% 
'''


class ChangeIterations(ast.NodeTransformer):
    def visit_For(self, node):
        """Посещает все for и меняет кол-во итераций"""
        if probability_100():
            if len(node.iter.args) > 1:
                node.iter.args[1].value += get_random()
            elif len(node.iter.args) == 1:
                node.iter.args[0].value += get_random()

        return ast.For(target=node.target, iter=node.iter, body=node.body, orelse=node.orelse)


def probability_100():
    """В зависимости от переданной сложности будем изменять вероятность"""
    return random.random() < 1


def get_random():
    """Генерирует случайное число"""
    return int(round(random.random(), 2) * 100)
