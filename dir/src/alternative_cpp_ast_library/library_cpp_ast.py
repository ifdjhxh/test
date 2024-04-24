import pprint
# Prints the nicely formatted dictionary


def f_open(name):
    f = open(name, "r")
    s = f.read()

    f.close()
    return s

def skip_spaces(file, index):
    while True:
        while index < len(file) and (file[index] == ' ' or file[index] == '\t' or file[index] == '\n'):
            index += 1
        if index >= len(file):
            break
        if index + 1 < len(file) and file[index: index + 2] == '//':
            while index < len(file) and file[index] != '\n':
                index += 1
            continue
        if index + 1 < len(file) and file[index: index + 2] == '/*':
            while index + 1 < len(file) and file[index: index + 2] != '*/':
                index += 1
            continue
        break

    return index

def check_function(file, index):
    flag = True
    while index < len(file) and (file[index] == ' ' or file[index] == '\t' or file[index] == '\n'):
        index += 1
    index = skip_spaces(file, index)
    while index < len(file) and (file[index] == ' ' or file[index] == '\t' or file[index] == '\n' or file[index] != '('):
        index += 1
    index = skip_spaces(file, index)
    if index < len(file) and file[index] == '(':
        flag = True
    else:
        return False
    index = skip_spaces(file, index)
    while index < len(file) and file[index] != ')':
        index += 1
    if index < len(file) and file[index] == ')':
        return True
    else:
        return False


def check_up_statement(file, index):
    index = skip_spaces(file, index)
    if index >= len(file):
        return "E", index   # End
    elif file[index] == "#":
        return "D", index   # Directive
    elif file[index:index + 5] == "using":
        return "U", index   # Using
    elif file[index:index + 5] == "class":
        return "C", index   # Class
    elif file[index:index + 6] == "struct":
        return "S", index   # Struct
    elif check_function(file, index):
        return "F", index   # Function
    else:
        return "-", index   # Unknown

def analyze_directive(file, index):
    old_index = index
    while index < len(file) and file[index] != '\t' and file[index] != '\n' and file[index] != ' ':
        index += 1
    name_directive = file[old_index:index]
    index = skip_spaces(file, index)
    old_index = index
    while index < len(file) and file[index] != '\n':
        index += 1
    body_directive = file[old_index: index]
    return {
        "name": name_directive,
        "value": body_directive,
        "children": False
           }, index
    # Возможно, надо допилить, т.к. внутри названий директив могут быть пробелы

def analyze_using(file, index):
    index += 5
    index = skip_spaces(file, index)
    old_index = index
    while index < len(file) and file[index] != ';':
        index += 1

    body_using = file[old_index:index]
    if file[index] == ';':
        index += 1
    return {
        "name": "using",
        "value": body_using,
        "children": False
           }, index

def analyze_parameters(parameters):
    index = 1
    index = skip_spaces(parameters, index)
    ret_params = []
    while index < len(parameters)-1:
        params = {
            "type": None,
            "name": None
        }
        old_index = index
        while index < len(parameters)-1 and parameters[index] != '\t' and parameters[index] != '\n' and parameters[index] != ' ':
            index += 1
        params['type'] = parameters[old_index: index]
        index = skip_spaces(parameters, index)
        if parameters[index] == '*':
            while parameters[index] == '*':
                params['type'] += '*'
                index += 1
        index = skip_spaces(parameters, index)
        old_index = index
        while index < len(parameters)-1 and parameters[index] != '\t' and parameters[index] != '\n' and parameters[index] != ' ' and parameters[index] != ','and parameters[index] != ')':
            index += 1
        params['name'] = parameters[old_index: index]
        index += 1
        ret_params.append(params)
        index = skip_spaces(parameters, index)

    return ret_params

def check_symbol(symb, arr):
    for a in arr:
        if symb == a:
            return True
    return False

def slice_body(body):
    index = 1
    if index < len(body) - 1 and body[index] == '{':
        index += 1
    index = skip_spaces(body, index)
    arr = []
    while index < len(body) - 1:
        old_index = index
        while index < len(body) - 1 and body[index] != '{' and body[index] != ';':
            index += 1
            # do-while надо будет поправить и добавить switch
        if old_index + 6 < len(body) - 1:
            if (body[old_index: old_index + 3] == "for" and check_symbol(body[old_index+3], [' ','\n','\t','(','{'])) or (body[old_index: old_index + 5] == "while"and check_symbol(body[old_index+5], [' ','\n','\t','(','{'])) or (body[old_index: old_index + 2] == "do"and check_symbol(body[old_index+2], [' ','\n','\t','(','{'])) or (body[old_index: old_index + 2] == "if" and check_symbol(body[old_index+2], [' ','\n','\t','(','{'])):
                while index < len(body) - 1 and body[index] != '{':
                    index += 1
        if body[index] == ';':
            index += 1
            arr.append(body[old_index: index])
        elif body[index] == '{':
            count_scopes = 1
            index += 1
            while index < len(body) - 1 and count_scopes > 0:
                if body[index] == "{":
                    count_scopes += 1
                elif body[index] == "}":
                    count_scopes -= 1
                index += 1
            arr.append(body[old_index: index])
        index = skip_spaces(body, index)
    return arr

def check_statement_string(elem):
    index = 0
    old_index = index
    while index < len(elem)-1 and not check_symbol(elem[index], [';', '(', ' ', '\t', '\n', '<', '>']):
        index += 1
    word = elem[old_index: index]
    if word == "return":
        return "r"
    elif word == "const":
        return "c"
    elif word == "delete":
        return "d"
    else:
        index = skip_spaces(elem, index)
        if elem[index] == "(":
            return "f"  # function
        elif elem[index: index + 2] == "<<":
            return "o"  # output_stream
        elif elem[index: index + 2] == ">>":
            return "i"  # input_stream
        elif elem[index] == '=':
            return '='  # присваивание без объявления
        elif check_symbol(elem[index: index + 2], ['+=', '-=', '*=', '/=', '%=']):
            return elem[index: index + 2]
        else:
            old_index = index
            while index < len(elem) - 1 and not check_symbol(elem[index], [';', '(', ' ', '\t', '\n', '<', '>']):
                index += 1
            index = skip_spaces(elem, index)
            if elem[index] == ';':
                return 'a'  #initialise
            elif elem[index] == '=':
                return 'b'  #initialise_and_присваивание

def analyze_return(elem):
    index = skip_spaces(elem, 6)
    body = ""
    if elem[index] != ';':
        old_index = index
        while not check_symbol(elem[index], [';']):
            index += 1
        body = elem[old_index: index]
    return {
        "type": "return",
        "value": body
    }

def analyze_const(elem):
    index = skip_spaces(elem, 5)
    old_index = index
    while index < len(elem) - 1 and not check_symbol(elem[index], [';', '(', ' ', '\t', '\n', '<', '>']):
        index += 1
    const_type = elem[old_index: index]
    index = skip_spaces(elem, index)

    if elem[index] == '*':
        while elem[index] == '*':
            const_type += '*'
            index += 1
    index = skip_spaces(elem, index)

    old_index = index

    while index < len(elem) - 1 and not check_symbol(elem[index], [';', '(', ' ', '\t', '\n', '<', '>']):
        index += 1
    const_name = elem[old_index: index]
    index = skip_spaces(elem, index)
    index += 1
    index = skip_spaces(elem, index)
    old_index = index
    while index < len(elem) - 1 and not check_symbol(elem[index], [';', '(', ' ', '\t', '\n', '<', '>']):
        index += 1
    const_value = elem[old_index: index]
    return {
        "type": "const",
        "const_type": const_type,
        "const_name": const_name,
        "const_value": const_value
    }

def analyze_delete(elem):
    index = skip_spaces(elem, 6)
    body = ""
    if elem[index] != ';':
        old_index = index
        while not check_symbol(elem[index], [';', ' ', '\t', '\n', '[']):
            index += 1
        body = elem[old_index: index]
    return {
        "type": "delete",
        "value": body
    }

def analyze_output_stream(elem):
    index = skip_spaces(elem, 0)
    old_index = index
    arr = []
    while not check_symbol(elem[index], ['<', ' ', '\t', '\n']):
        index += 1
    command = elem[old_index: index]
    index = skip_spaces(elem, index)
    while elem[index] != ';':
        index += 2
        index = skip_spaces(elem, index)
        old_index = index
        while not check_symbol(elem[index], ['<', ' ', '\t', '\n', ';']):
            index += 1
        arr.append(elem[old_index: index])
        index = skip_spaces(elem, index)
    return {
        "type": "output_stream",
        "command": command,
        "operands": arr
    }

def analyze_input_stream(elem):
    index = skip_spaces(elem, 0)
    old_index = index
    arr = []
    while not check_symbol(elem[index], ['>', ' ', '\t', '\n']):
        index += 1
    command = elem[old_index: index]
    index = skip_spaces(elem, index)
    while elem[index] != ';':
        index += 2
        index = skip_spaces(elem, index)
        old_index = index
        while not check_symbol(elem[index], ['>', ' ', '\t', '\n', ';']):
            index += 1
        arr.append(elem[old_index: index])
        index = skip_spaces(elem, index)
    return {
        "type": "input_stream",
        "command": command,
        "operands": arr
    }

def analyze_assignment(elem):
    index = skip_spaces(elem, 0)
    old_index = index
    while index < len(elem) - 1 and not check_symbol(elem[index], [';', '(', ' ', '\t', '\n', '<', '>']):
        index += 1
    name = elem[old_index: index]
    index = skip_spaces(elem, index)
    index += 1
    index = skip_spaces(elem, index)

    old_index = index
    while index < len(elem) - 1 and elem[index] != ';':
        index += 1
    value = elem[old_index: index]
    return {
        "type": "assignment",
        "name": name,
        "value": value
    }

def analyze_definition(elem):
    index = skip_spaces(elem, 0)
    old_index = index
    while index < len(elem) - 1 and not check_symbol(elem[index], [';', '(', ' ', '\t', '\n', '<', '>']):
        index += 1
    var_type = elem[old_index: index]
    index = skip_spaces(elem, index)
    if elem[index] == '*':
        while elem[index] == '*':
            var_type += '*'
            index += 1
    index = skip_spaces(elem, index)
    old_index = index
    while index < len(elem) - 1 and elem[index] != ';':
        index += 1
    var_name = elem[old_index: index]
    return {
        "type": "assignment",
        "var_type": var_type,
        "var_name": var_name
    }

def analyze_definition_and_assigment(elem):
    index = skip_spaces(elem, 0)
    old_index = index
    while index < len(elem) - 1 and not check_symbol(elem[index], [';', '(', ' ', '\t', '\n', '<', '>']):
        index += 1
    var_type = elem[old_index: index]
    index = skip_spaces(elem, index)
    if elem[index] == '*':
        while elem[index] == '*':
            var_type += '*'
            index += 1
    index = skip_spaces(elem, index)
    old_index = index
    while index < len(elem) - 1 and elem[index] != '=':
        index += 1
    var_name = elem[old_index: index]

    index = skip_spaces(elem, index)
    index += 1
    index = skip_spaces(elem, index)

    old_index = index
    while index < len(elem) - 1 and elem[index] != ';':
        index += 1
    var_value = elem[old_index: index]
    return {
        "type": "definition_and_assignment",
        "var_type": var_type,
        "var_name": var_name,
        "var_value": var_value
    }

def analyze_call_func(elem):
    index = skip_spaces(elem, 0)
    old_index = index
    while index < len(elem) - 1 and not check_symbol(elem[index], ['(', ' ', '\t', '\n']):
        index += 1
    func_name = elem[old_index: index]
    index = skip_spaces(elem, index)
    index += 1
    arr = []
    index = skip_spaces(elem, index)
    while index < len(elem) - 1 and not check_symbol(elem[index], [')']):
        old_index = index
        while index < len(elem) - 1 and not check_symbol(elem[index], [',', ')']):
            index += 1
        arr.append(elem[old_index: index])
        index = skip_spaces(elem, index)
        index += 1
    return {
        "type": "call_func",
        "func_name": func_name,
        "params": arr
    }


def analyze_body(body):
    # print("from analyze_body")
    body = slice_body(body)
    # print(body)
    ret_body = []
    for b in body:
        obj = {
            "type": None,
            "value": None
        }
        if b[-1] == ';':
            symbol = check_statement_string(b)
            if symbol == 'r':
                ret_body.append(analyze_return(b))
            elif symbol == 'c':
                ret_body.append(analyze_const(b))
            elif symbol == 'd':
                ret_body.append(analyze_delete(b))
            elif symbol == 'f':
                ret_body.append(analyze_call_func(b))

            elif symbol == 'o':
                ret_body.append(analyze_output_stream(b))
            elif symbol == 'i':
                ret_body.append(analyze_input_stream(b))
            elif symbol == '=':
                ret_body.append(analyze_assignment(b))
            elif symbol == 'a':
                ret_body.append(analyze_definition(b))
            elif symbol == 'b':
                ret_body.append(analyze_definition_and_assigment(b))
            else:
                ret_body.append({
                    "type": "unknown",
                    "value": b
                })

    return ret_body



def analyze_func(file, index):
    index = old_index = skip_spaces(file, index)
    while index < len(file) and file[index] != '\t' and file[index] != '\n' and file[index] != ' ':
        index += 1
    type_func = file[old_index:index]
    # print(index)
    index = skip_spaces(file, index)
    # print(index)
    old_index = index
    if file[index] == '*':
        while file[index] == '*':
            type_func += '*'
            index += 1
    # print(type_func)
    index = skip_spaces(file, index)
    # print(index)
    old_index = index
    while index < len(file) and file[index] != '(' and file[index] != '\t' and file[index] != '\n' and file[index] != ' ':
        index += 1
    name_func = file[old_index:index]
    index = skip_spaces(file, index)

    # print(name_func)
    parameters = ""
    old_index = index
    if index+1 < len(file) and file[index: index + 2] == '()':
        parameters = ""
    else:
        if file[index+1] != ')':
            count_scopes = 1
            index += 1
            while index < len(file) and count_scopes > 0:
                if file[index] == "(":
                    count_scopes += 1
                elif file[index] == ")":
                    count_scopes -= 1
                index += 1
            parameters = file[old_index:index]
    # print(parameters)
    parameters = analyze_parameters(parameters)
    index = skip_spaces(file, index)
    old_index = index
    body = ""
    has_children = False
    if file[index] == "{":
        has_children = True
        count_scopes = 1
        index += 1
        while index < len(file) and count_scopes > 0:
            if file[index] == "{":
                count_scopes += 1
            elif file[index] == "}":
                count_scopes -= 1
            index += 1
        body = file[old_index: index]
    # print(body)
    body = analyze_body(body)
    return {
        "return_type": type_func,
        "name": name_func,
        "parameters": parameters,
        "body": body,
        "children": has_children
           }, index

    # return [type_func, name_func, parameters, body], index


def generate_str_using(node):
    pass

def generate_str_function(node):
    pass

def generate_str_include(node):
    pass


def ast_to_file(ast_tree):
    str = ""

    pass

if __name__ == '__main__':
    file_name = "example.cpp"
    s = f_open(file_name)

    ast = {
        "file": file_name,
        "main_children": []
    }
    station = "A"
    index = 0
    # counter = 0
    while station != 'E':
        station, index = check_up_statement(s, index)
        temp = None
        if station == 'E':
            break
        elif station == 'D':
            directive = {
                "type": "directive",
                "main_info": None,
                "children": None
            }
            main_info, index = analyze_directive(s, index)
            directive['main_info'] = main_info
            ast['main_children'].append(directive)
        elif station == 'U':
            using = {
                "type": "using",
                "main_info": None,
                "children": None
            }
            main_info, index = analyze_using(s, index)
            using['main_info'] = main_info
            ast['main_children'].append(using)
        elif station == 'C':
            pass
        elif station == 'S':
            pass
        elif station == 'F':
            func = {
                "type": "function",
                "main_info": None,
                "children": None
            }
            main_info, index = analyze_func(s, index)
            if main_info['children']:
                func['children'] = main_info['body']
            func['main_info'] = main_info
            ast['main_children'].append(func)
        elif station == '-':
            print('Произошла ошибка: Неизвестный тип или не предусмотрено программой')
            break
    print(pprint.pformat(ast))
    # print(ast)
