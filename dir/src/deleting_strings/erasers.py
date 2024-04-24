from deleting_strings.call_params_eraser import callParamsEraser
from deleting_strings.list_eraser import listEraser
from deleting_strings.return_eraser import returnEraser
from deleting_strings.vars_eraser import varsEraser


def eraser(tree):

    # Начало операций

    tree = listEraser(tree)
    tree = returnEraser(tree)
    tree = varsEraser(tree)
    tree = callParamsEraser(tree)

    # Конец операций
    return tree