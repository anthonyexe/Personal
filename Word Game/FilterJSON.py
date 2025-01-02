import json

with open('words_dictionary.json', 'r') as file:
    data = json.load(file)

three_dict = {}
four_dict = {}
five_dict = {}

for item in data:
    if len(item) == 3:
        three_dict[item] = 1
    if len(item) == 4:
        four_dict[item] = 1
    if len(item) == 5:
        five_dict[item] = 1

with open('three_letter_words.json', 'w') as threeFileOut:
    json.dump(three_dict, threeFileOut)

with open('four_letter_words.json', 'w') as fourFileOut:
    json.dump(four_dict, fourFileOut)

with open('five_letter_words.json', 'w') as fiveFileOut:
    json.dump(five_dict, fiveFileOut)