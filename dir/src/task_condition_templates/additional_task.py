import random

from src.task_condition_templates.visitors import ListVisitor, DictVisitor


class AdditionalTask:

    def __init__(self):
        self.questions_pull = []

    def create_questions_pull(self, tree):
        changer = ListVisitor()
        changer.visit(tree)
        if changer.count > 0:
            file = open("C:/Users/Acer/PycharmProjects/mse1h2024-task-gen/src/task_condition_templates/lists.txt", "r",
                        encoding='utf-8')
            for line in file.readlines():
                line = line.replace(r"\n", "\n")
                self.questions_pull.append(line.replace("[]", random.choice(changer.name)))

        changer = DictVisitor()
        changer.visit(tree)
        if changer.count > 0:
            file = open("C:/Users/Acer/PycharmProjects/mse1h2024-task-gen/src/task_condition_templates/dict.txt", "r",
                        encoding='utf-8')
            for line in file.readlines():
                line = line.replace(r"\n", "\n")
                self.questions_pull.append(line.replace("[]", random.choice(changer.name)))

        file = open("C:/Users/Acer/PycharmProjects/mse1h2024-task-gen/src/task_condition_templates/loops.txt", "r",
                    encoding='utf-8')
        for line in file.readlines():
            line = line.replace(r"\n", "\n")
            self.questions_pull.append(line)

    def get_questions(self, tree, complexity):
        self.create_questions_pull(tree)
        if complexity < 20:
            return "Вопросов нет"
        if complexity < 60:
            return random.choice(self.questions_pull)
        else:
            arr = random.sample(set(self.questions_pull), 2)
            return arr[0] + arr[1]

    def print_questions_pull(self):
        print(self.questions_pull)
