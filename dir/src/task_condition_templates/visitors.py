import ast


class ListVisitor(ast.NodeTransformer):

    def __init__(self):
        self.count = 0
        self.name = []

    def visit_Assign(self, node):
        if isinstance(node.value, ast.List):
            self.name.append(node.targets[0].id)
            self.count += 1
        return node

    def get_count(self):
        return self.count

    def get_name(self):
        return self.name


class DictVisitor(ast.NodeTransformer):

    def __init__(self):
        self.count = 0
        self.name = []

    def visit_Assign(self, node):
        if isinstance(node.value, ast.Dict):
            self.name.append(node.targets[0].id)
            self.count += 1
        return node

    def get_count(self):
        return self.count

    def get_name(self):
        return self.name
