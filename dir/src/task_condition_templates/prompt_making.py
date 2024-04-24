def question_making(question):
    prompt_file = open("C:/Users/Acer/PycharmProjects/mse1h2024-task-gen/src/task_condition_templates/prompt.txt", 'r', encoding='utf-8')
    text = prompt_file.readline()
    return text.replace('[mistake]', question)