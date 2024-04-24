from clang.cindex import Index, CursorKind, TypeKind
import re

# Список типов узлов AST, которые мы хотим сохранить
interesting_node_types = [
    CursorKind.CLASS_DECL,
    CursorKind.FUNCTION_DECL,
    CursorKind.VAR_DECL,
    CursorKind.PARM_DECL,
    CursorKind.CONSTRUCTOR,
    CursorKind.CXX_METHOD
]


# Функция для преобразования AST в нужный формат вывода
def ast_to_custom_format(node, code):
    '''
        :param node: узел AST-дерева.
            Для каждого узла записывает его основные характеристики, затем рекурсивно вызыввается для его детей.
        :return: AST-дерево от переданного узла в виде вложенного словаря.
    '''

    def get_acsess(acsess_name):
        '''
            :param acsess_name: объект, который содержит информацию об модификаторе доступа
            :return: название модификатора доступа в виде строки (friend -> private)
        '''
        if str(acsess_name) == 'AccessSpecifier.PUBLIC':
            return 'public'
        elif str(acsess_name) == 'AccessSpecifier.PRIVATE':
            return 'private'
        elif str(acsess_name) == 'AccessSpecifier.PROTECTED':
            return 'protected'

    def variable_expression_parser(variable_name, code):
        '''
            :param variable_name: имя переменной, которое будем искать в исходном коде и анализировать.
            :return: Часть AST дерева, связанного с этой переменной.
        '''

        pattern = rf'{variable_name}\s*=\s*(\w+.\w+|\w+|"\w+")+\s*;'

        match = re.search(pattern, str(code))
        if match:
            objects = match.group(1).split(',')
            res = objects[0]
            return res
        else:
            return None

    if node.kind == CursorKind.VAR_DECL:
        result = {'variable': {'name': node.spelling, 'type': '', 'value': [], 'children': []}}

        if node.type.kind != TypeKind.INVALID:
            result['variable']['type'] = node.type.spelling
        else:
            result['variable']['type'] = 'None'

        result['variable']['value'] = variable_expression_parser(node.spelling, code)

        parent = node.semantic_parent
        while parent is not None and parent.kind != CursorKind.FUNCTION_DECL:
            parent = parent.semantic_parent

        if parent is not None and parent.kind == CursorKind.FUNCTION_DECL:
            result['variable']['function'] = parent.spelling
        return result



    # поля класса
    if node.kind == CursorKind.FIELD_DECL:  # ok
        result = {'class_field': {'name': node.spelling, 'type': node.type.spelling,
                                  'value': variable_expression_parser(node.spelling, code),
                                  'access': get_acsess(node.access_specifier)}}
        # for child in node.get_children():
        #     if child.kind == CursorKind.CALL_EXPR:
        #         argument_list = [arg.spelling for arg in child.get_arguments()]
        #         for arg in argument_list:
        #             variable_name = arg.split('=')[0].strip()
        #             variable_value = arg.split('=')[1].strip()
        #             print(f"Variable '{variable_name}' initialized with value '{variable_value}'")
        return result

    # дуструктор класса
    if node.kind == CursorKind.DESTRUCTOR:  # ok
        result = {'destructor': {'name': '', 'access': get_acsess(node.access_specifier), 'args': [], 'children': []}}

        # имя функции
        result['destructor']['name'] = node.spelling

        # аргументы
        args_list = []
        for arg in node.get_arguments():
            if node.get_arguments():
                args_list.append({'name': arg.spelling, 'type': arg.type.spelling})
            else:
                args_list.append('None')
                break
        result['destructor']['args'] = args_list

        for c in node.get_children():
            # если это весомый узел
            if c.spelling:
                result['destructor']['children'].append(ast_to_custom_format(c, code))
        return result

    # метод класса
    if node.kind == CursorKind.CXX_METHOD:  # ok
        result = {
            'method': {'name': '', 'access': get_acsess(node.access_specifier), 'return_type': '', 'args': [],
                       'children': []}}

        # имя функции
        result['method']['name'] = node.spelling

        # возвращаемый тип
        if node.result_type.kind != TypeKind.INVALID:
            result['method']['return_type'] = node.result_type.spelling
        else:
            result['method']['return_type'] = 'None'

        # аргументы
        args_list = []
        for arg in node.get_arguments():
            if node.get_arguments():
                args_list.append({'name': arg.spelling, 'type': arg.type.spelling})
            else:
                args_list.append('None')
                break
        result['method']['args'] = args_list

        for c in node.get_children():
            # если это весомый узел
            if c.spelling:
                result['method']['children'].append(ast_to_custom_format(c, code))
        return result

    # класс
    if node.kind == CursorKind.CLASS_DECL:  # ok
        result = {'class': {'name': '', 'children': []}}
        result['class']['name'] = node.spelling
        for c in node.get_children():
            if c.spelling:
                result['class']['children'].append(ast_to_custom_format(c, code))
        return result

    # конструктор класса
    if node.kind == CursorKind.CONSTRUCTOR:  # ok
        result = {'constructor': {'name': '', 'access': get_acsess(node.access_specifier), 'args': [], 'children': []}}

        # имя функции
        result['constructor']['name'] = node.spelling

        # аргументы
        args_list = []
        for arg in node.get_arguments():
            if node.get_arguments():
                args_list.append({'name': arg.spelling, 'type': arg.type.spelling})
            else:
                args_list.append('None')
                break
        result['constructor']['args'] = args_list

        for c in node.get_children():
            # если это весомый узел
            if c.spelling:
                result['constructor']['children'].append(ast_to_custom_format(c, code))
        return result

    # структура
    elif node.kind == CursorKind.STRUCT_DECL:  # ok
        result = {'struct': {'name': '', 'children': []}}
        result['struct']['name'] = node.spelling
        for c in node.get_children():
            # если это весомый узел
            if c.spelling:
                result['struct']['children'].append(ast_to_custom_format(c, code))
        return result

    # функция
    elif node.kind == CursorKind.FUNCTION_DECL:  # проблема - не видит детей!!!
        result = {'function': {'name': '', 'return_type': '', 'args': [], 'children': []}}

        # имя функции
        result['function']['name'] = node.spelling

        # возвращаемый тип
        if node.result_type.kind != TypeKind.INVALID:
            result['function']['return_type'] = node.result_type.spelling
        else:
            result['function']['return_type'] = 'None'

        # аргументы
        args_list = []
        for arg in node.get_arguments():
            if node.get_arguments():
                args_list.append({'name': arg.spelling, 'type': arg.type.spelling})
            else:
                args_list.append('None')
                # break
        result['function']['args'] = args_list

        for c in node.get_children():
            # если это весомый узел
            # if c.spelling:
            result['function']['children'].append(ast_to_custom_format(c, code))
        return result

    elif node.kind == CursorKind.WHILE_STMT:
        result = {'while_loop': {'children': []}}

        for c in node.get_children():
            result['while_loop']['children'].append(ast_to_custom_format(c, code))

        return result

    elif node.kind == CursorKind.FOR_STMT:
        result = {'for_loop': {'children': []}}

        for c in node.get_children():
            result['for_loop']['children'].append(ast_to_custom_format(c, code))

        return result

    elif node.kind == CursorKind.DO_STMT:
        result = {'do_while_loop': {'children': []}}

        for c in node.get_children():
            result['do_while_loop']['children'].append(ast_to_custom_format(c, code))

        return result

    elif node.kind == CursorKind.COMPOUND_STMT:
        result = {'compound_stmt': {'children': []}}
        for c in node.get_children():
            result['compound_stmt']['children'].append(ast_to_custom_format(c, code))

    elif node.kind == CursorKind.DECL_STMT:
        result = {'decl_stmt': {'children': []}}
        for c in node.get_children():
            result['decl_stmt']['children'].append(ast_to_custom_format(c, code))

    elif node.kind == CursorKind.VAR_DECL:
        result = {'var_decl': {'children': []}}
        for c in node.get_children():
            result['var_decl']['children'].append(ast_to_custom_format(c, code))

    elif node.kind == CursorKind.CALL_EXPR:
        result = {'call_expr': {'children': []}}
        for c in node.get_children():
            result['call_expr']['children'].append(ast_to_custom_format(c, code))

    elif node.kind == CursorKind.RETURN_STMT:
        result = {'return_stmt': {'children': []}}
        for c in node.get_children():
            result['return_stmt']['children'].append(ast_to_custom_format(c, code))

    elif node.kind == CursorKind.IF_STMT:
        result = {'if_stmt': ''}
        result['if_stmt'] = {'condition': ast_to_custom_format(list(node.get_children())[0], code),
                             'then': ast_to_custom_format(list(node.get_children())[1], code), 'else': None}
        if len(list(node.get_children())) > 2:
            result['if_stmt']['else'] = ast_to_custom_format(list(node.get_children())[2], code)
    else:
        result = {'node': {'kind': node.kind.name}}

    return result
    # сомнительно, но ОКЭЙ.
    # else:
    #     result = {'node': {'kind': node.kind.name}}
    #     return result


# Парсинг кода и преобразование AST в нужный формат
def parse_and_convert_to_custom_format(code):
    '''
        :param code: код
        :return: AST-дерево в виде вложенного словаря
    '''
    result = {'root': {'children': []}}
    index = Index.create()
    tu = index.parse('example.cpp', args=['-std=c++11'], unsaved_files=[('example.cpp', code)])
    for child in tu.cursor.get_children():
        result['root']['children'].append(ast_to_custom_format(child, code))
    return result


def file_open(name):
    file = open(name, "r")
    string = file.read()
    file.close()
    return string


def print_nested_dict(d, level=0):
    for key, value in d.items():
        print(f"{'--' * level}{key}:")
        if isinstance(value, dict):
            print_nested_dict(value, level + 1)
        elif isinstance(value, list):
            for i in range(len(value)):
                if not (value[i] is None):
                    print_nested_dict(value[i], level + 1)
        else:
            print(f"{'  ' * (level + 1)}{value}")


if __name__ == '__main__':
    cpp_code = file_open("example.cpp")
    # print(cpp_code)
    # Преобразование и вывод AST в нужном формате
    custom_format = parse_and_convert_to_custom_format(cpp_code)
    # print(custom_format)
    print_nested_dict(custom_format)
