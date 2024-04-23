import ast
import random

from replacing_signs.enums import SignType


class Visitor:
    """
    Общий класс для Visitor'ов, который содержит методы для установки вероятности
    """

    def __init__(self):
        self.probability = 0.5

    def set_probability(self, probability):
        self.probability = probability


class BoolOpVisitor(ast.NodeTransformer, Visitor):
    """Класс для посещения всех булевых операций в ast дереве"""

    def __init__(self):
        super().__init__()

    def visit_BoolOp(self, node):
        """Посещает все булевы операции and/or"""
        self.generic_visit(node)  # Посещение вложенных узлов
        if type(node.op) is ast.Or:
            if random.choices([True, False], weights=[self.probability, 1 - self.probability])[0]:
                return ast.BoolOp(op=ast.And(), values=node.values)
            else:
                return node
        else:
            if random.choices([True, False], weights=[self.probability, 1 - self.probability])[0]:
                return ast.BoolOp(op=ast.Or(), values=node.values)
            else:
                return node


class CompareVisitor(ast.NodeTransformer, Visitor):
    """Класс для посещения всех сравнений в ast дереве"""
    def __init__(self):
        super().__init__()

    def visit_Compare(self, node):
        """Посещает все узлы сравнения в дереве"""
        try:
            if random.choices([True, False], weights=[self.probability, 1 - self.probability])[0]:
                new_left = node.left
                new_ops = [random.choice(list(SignType)).value]  # Получаем случайную операцию сравнения из перечисления
                new_comparators = node.comparators
                new_node = ast.Compare(new_left, new_ops, new_comparators)
                return new_node
            else:
                return node
        except AttributeError:
            print("Compare visit error")
            return node
