from clang.cindex import Index, CursorKind, TypeKind, Config
Config.set_library_file('./libclang.dll')

# Список типов узлов AST, которые мы хотим сохранить
interesting_node_types = [
    CursorKind.CLASS_DECL,
    CursorKind.FUNCTION_DECL,
    CursorKind.VAR_DECL,
    CursorKind.PARM_DECL,
    CursorKind.INTEGER_LITERAL,
    CursorKind.FLOATING_LITERAL,
    CursorKind.STRING_LITERAL,
    CursorKind.WHILE_STMT,
    CursorKind.DO_STMT,
    CursorKind.FOR_STMT
]


# Функция для преобразования AST в нужный формат вывода
def ast_to_custom_format(node):
    '''
        Функция принимает на вход узел AST-дерева
        Для каждого узла записывает его основные характеристики, затем рекурсивно вызыввается для его детей
        Возращает AST-дерево от переданного узла в виде вложенного словаря
    '''
    if node.kind == CursorKind.CLASS_DECL:
        result = {'class': {'name': '', 'children': []}}
        result['class']['name'] = node.spelling
        for c in node.get_children():
            result['class']['children'].append(ast_to_custom_format(c))
        return result

    elif node.kind == CursorKind.FUNCTION_DECL:
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
                break
        result['function']['args'].append(args_list)

        for c in node.get_children():
            if c.kind == CursorKind.VAR_DECL:
                result['function']['variables'].append(ast_to_custom_format(c))

        for c in node.get_children():
            result['function']['children'].append(ast_to_custom_format(c))
        return result

    elif node.kind == CursorKind.VAR_DECL:
        result = {'variable': {'name': '', 'type': ''}}

        #имя переменной
        result['variable']['name'] = node.spelling

        if node.type.kind != TypeKind.INVALID:
            result['variable']['type'] = node.type.spelling
        else:
            result['variable']['type'] = 'None'

        for c in node.get_children():
            if c.kind == CursorKind.INTEGER_LITERAL or c.kind == CursorKind.FLOATING_LITERAL or c.kind == CursorKind.STRING_LITERAL:
                result['variable']['value'] = c.spelling

        parent = node.semantic_parent
        while parent is not None and parent.kind != CursorKind.FUNCTION_DECL:
            parent = parent.semantic_parent

        if parent is not None and parent.kind == CursorKind.FUNCTION_DECL:
            result['variable']['function'] = parent.spelling
        return result

    elif node.kind == CursorKind.WHILE_STMT:
        result = {'while_loop': {'children': []}}

        for c in node.get_children():
            result['while_loop']['children'].append(ast_to_custom_format(c))

        return result

    elif node.kind == CursorKind.FOR_STMT:
        result = {'for_loop': {'children': []}}

        for c in node.get_children():
            result['for_loop']['children'].append(ast_to_custom_format(c))

        return result

    elif node.kind == CursorKind.DO_STMT:
        result = {'do_while_loop': {'children': []}}

        for c in node.get_children():
            result['do_while_loop']['children'].append(ast_to_custom_format(c))

        return result

    elif node.kind == CursorKind.COMPOUND_STMT:
        result = {'compound_stmt': {'children': []}}
        for c in node.get_children():
            result['compound_stmt']['children'].append(ast_to_custom_format(c))

    elif node.kind == CursorKind.DECL_STMT:
        result = {'decl_stmt': {'children': []}}
        for c in node.get_children():
            result['decl_stmt']['children'].append(ast_to_custom_format(c))

    elif node.kind == CursorKind.VAR_DECL:
        result = {'var_decl': {'children': []}}
        for c in node.get_children():
            result['var_decl']['children'].append(ast_to_custom_format(c))

    elif node.kind == CursorKind.CALL_EXPR:
        result = {'call_expr': {'children': []}}
        for c in node.get_children():
            result['call_expr']['children'].append(ast_to_custom_format(c))

    elif node.kind == CursorKind.RETURN_STMT:
        result = {'return_stmt': {'children': []}}
        for c in node.get_children():
            result['return_stmt']['children'].append(ast_to_custom_format(c))

    elif node.kind == CursorKind.IF_STMT:
        result = {'if_stmt': ''}
        result['if_stmt'] = {'condition': ast_to_custom_format(list(node.get_children())[0]),
                             'then': ast_to_custom_format(list(node.get_children())[1]), 'else': None}
        if len(list(node.get_children())) > 2:
            result['if_stmt']['else'] = ast_to_custom_format(list(node.get_children())[2])

    # elif node.kind == CursorKind.BINARY_OPERATOR:
    #     result = {'binary_operator': ''}
    #     print(node.type)
    #     result['binary_operator'] = {
    #         'operator': node.spelling,
    #         'left_operand': ast_to_custom_format(list(node.get_children())[0]),
    #         'right_operand': ast_to_custom_format(list(node.get_children())[1])
    #     }


    # elif node.kind == CursorKind.INTEGER_LITERAL:
    #     # Проверяем, что строка не пустая, перед преобразованием в целое число
    #     result = {'integer_literal': ''}
    #     result['integer_literal'] = int(node.spelling)  # Установим значение по умолчанию, если строка пустая


    else:
        result = {'node': {'kind': node.kind.name}}

    return result

# Парсинг кода и преобразование AST в нужный формат
def parse_and_convert_to_custom_format(code):
    '''
        Функция принимает на вход код
        Возвращает AST-дерево в виде вложенного словаря
    '''
    result = {'root': {'children': []}}
    index = Index.create()
    tu = index.parse('example.cpp', args=['-std=c++11'], unsaved_files=[('example.cpp', code)])
    for c in tu.cursor.get_children():
        result['root']['children'].append(ast_to_custom_format(c))
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
    print(cpp_code)
    # Преобразование и вывод AST в нужном формате
    custom_format = parse_and_convert_to_custom_format(cpp_code)
    # print(custom_format)
    print_nested_dict(custom_format)
