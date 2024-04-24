# Import needed libraries
import csv
import sys
import random
import copy
'''To start: python3 promptly.py prompt.txt dictionary.csv 1'''
# Store number of random prompts to generate
num_prompts = 1

# Set up our data structures for the prompt
replacements = []
word = ""

# Set up our data structures for the CSV files
descriptors = []
phrases = []


# Test that phrases are properly saved
def print_phrases():
    for phrase in phrases:
        print(str(phrase))


# Test that prompt is correctly processed
def print_prompt_replacements():
    for replacement_phrase in replacements:
        print(str(replacement_phrase))


# Choose a random item from the supplied list of phrases
def choose_random_word(descriptor_phrase, existing_text):
    reduced_list = []
    for item in phrases:
        if item[0] == descriptor_phrase:
            reduced_list.append(item[1])

            # Check for duplicates and replace the word if it's already been used

    def choose_word_and_check_for_duplicates():
        new_index = random.randint(0, len(reduced_list) - 1)
        proposed_word = reduced_list[new_index]
        try:
            existing_text.index(proposed_word)
            choose_word_and_check_for_duplicates()
        except ValueError:
            return proposed_word

    new_word = str(choose_word_and_check_for_duplicates())
    return new_word


# Generate a random individual prompt by replacing descriptor fragments
def generate_random_prompt(prmpt, replacements_to_make):
    if (len(replacements_to_make) > 0):
        replacement_key = replacements_to_make.pop(0)
        replacement_word = word
        tmp_prmpt = prmpt.replace(replacement_key, replacement_word, 1)
        generate_random_prompt(tmp_prmpt, replacements_to_make)
    else:
        print(prmpt)


# Generate a number of random prompts as specified in the program arguments
def generate_random_prompts():
    i = 0
    while i < num_prompts:
        replacements_list = copy.deepcopy(replacements)
        generate_random_prompt(original_prompt, replacements_list)
        i += 1


# Process the prompt given
def process_prompt(prompt):
    try:
        next_replacement_start = prompt.index('[')
        next_replacement_end = prompt.index(']')
        replacements.append(prompt[int(next_replacement_start): int(next_replacement_end) + 1])
        new_prompt = prompt[int(next_replacement_end) + 1:]
        process_prompt(new_prompt)

    except ValueError:
        generate_random_prompts()

def switch(match):
    global word
    if match == "1":
        word = "Синтаксис"
        return True
    elif match == "2":
        word = "Затирание"
        return True
    elif match == "3":
        word = "Логика"
        return True
    elif match == "4":
        word = "Синтаксис"
        return True
    elif match == "5":
        word = "Логика"
        return True
    elif match == "6":
        word = "Логика"
        return True
    elif match == "help":
        print("Введите цифру команды:\n 1 - Изменить названия функций \n 2 - Удалить строки \n 3 - Изменить "
              "аргументы передаваемые в функцию/возвращаемые функцией и область видимости \n 4 - Заменить тип "
              "переменных \n 5 - Изменить количество повторений в цикле for \n 6 - Поменять операции сравнения и "
              "булевы операции \n help - Для вывода подсказки \n exit - Для выхода \n")
        return True
    elif match == "exit":
        return False
    else:
        return True

choose = input("Введите цифру команды:\n 1 - Изменить названия функций \n 2 - Удалить строки \n 3 - Изменить "
                   "аргументы передаваемые в функцию/возвращаемые функцией и область видимости \n 4 - Заменить тип "
                   "переменных \n 5 - Изменить количество повторений в цикле for \n 6 - Поменять операции сравнения и "
                   "булевы операции \n help - Для вывода подсказки \n exit - Для выхода \n")
while switch(choose):
# Read in from our test csv file to store items
    prompt_file = open("prompt.txt", 'r', encoding='utf-8')
    original_prompt = prompt_file.read()
    csv_file_name = "Dictionary.csv"
    with open(csv_file_name, newline='', encoding='utf-8') as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            try:
                descriptors.index(row['descriptor'])
            except ValueError:
                descriptors.append(row['descriptor'])

            phrases.append(('[' + row['descriptor'] + ']', row['phrase']))

        process_prompt(original_prompt)

    choose = input()