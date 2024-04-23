# Import needed libraries
import csv
import sys
import random
import copy
'''To start: python3 promptly.py prompt.txt dictionary.csv 1'''
# Store number of random prompts to generate
num_prompts = int(sys.argv[3])

# Set up our data structures for the prompt
replacements = []

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
        replacement_word = choose_random_word(replacement_key, prmpt)
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


# Read in from our test csv file to store items
prompt_file = open(sys.argv[1], 'r')
original_prompt = prompt_file.read()
csv_file_name = sys.argv[2]
with open(csv_file_name, newline='') as csv_file:
    reader = csv.DictReader(csv_file)
    for row in reader:
        try:
            descriptors.index(row['descriptor'])
        except ValueError:
            descriptors.append(row['descriptor'])

        phrases.append(('[' + row['descriptor'] + ']', row['phrase']))

    process_prompt(original_prompt)
