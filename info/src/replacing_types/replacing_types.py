import ast
import random
from collections import Counter

'''
003 версия подтипа "Синтаксис: замена типа переменных"
Программа заменяет типы rvalue значений на другие c вероятностью 50% 
(в данной версии любое на любое, если это поддерживается языком)
'''


class RewriteType(ast.NodeTransformer):
    def visit_Constant(self, node):
        """Функция посещает все узлы-константы и меняет тип значения внутри на другой логически возможный"""
        new_node = node
        if probability_50():
            new_node = random_type(node)
        return new_node

    def visit_List(self, node):
        """Функция посещает все списки и меняет int->int/float/str; float->float/str; other->other/str"""
        new_elts = []
        main_type = defining_a_list_type(node.elts)
        tmp = random.random()
        if probability_50():
            for i in range(len(node.elts)):
                if main_type == int:
                    try:
                        if tmp < 0.5:
                            new_value = ast.Constant(float(node.elts[i].value))
                            new_elts.append(new_value)
                        else:
                            new_value = ast.Constant(str(node.elts[i].value))
                            new_elts.append(new_value)

                    except (ValueError, TypeError):
                        new_elts.append(ast.Constant(node.elts[i].value))

                elif main_type == float:
                    try:
                        new_value = ast.Constant(str(node.elts[i].value))
                        new_elts.append(new_value)

                    except (ValueError, TypeError):
                        new_elts.append(ast.Constant(node.elts[i].value))

                else:
                    try:
                        new_value = ast.Constant(str(node.elts[i].value))
                        new_elts.append(new_value)

                    except (ValueError, TypeError):
                        new_elts.append(ast.Constant(node.elts[i].value))

            return ast.List(elts=new_elts, ctx=node.ctx)

        return ast.List(elts=node.elts, ctx=node.ctx)


def defining_a_list_type(arr):
    """Определяет самый встречающийся тип в списке"""
    type_arr = []
    for i in range(len(arr)):
        type_arr.append(type(arr[i].value))

    most_common_type = Counter(type_arr).most_common()
    return most_common_type[0][0]


def random_type(node):
    """Возвращает любой тип"""
    value = node.value
    tmp = random.random()

    if value is None:
        tmp2 = random.random()
        if tmp2 < 0.5:
            return ast.Constant(str(value))
        else:
            return ast.Constant(bool(value))

    if isinstance(value, str):
        tmp3 = random.random()
        if tmp3 < 0.5:
            return ast.Constant(None)
        else:
            return ast.Constant(bool(value))

    if tmp < 0.2:
        return ast.Constant(str(value))

    elif tmp < 0.4 and not isinstance(value, float):
        return ast.Constant(int(value))

    elif tmp < 0.6:
        return ast.Constant(float(value))

    elif tmp < 0.8:
        return ast.Constant(None)

    elif tmp < 1:
        return ast.Constant(bool(value))

    else:
        return ast.Constant(value)


def probability_50():
    """В зависимости от переданной сложности будем изменять вероятность"""
    return random.random() < 0.5

