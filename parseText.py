import pandas as pd
import os
from striprtf.striprtf import rtf_to_text

companies = sorted(["3M Co", "American Express Co", "Amgen Inc", "Apple Inc", "Boeing Co", "Caterpillar Inc", "Cisco Systems Inc", "Chevron Corp", "Goldman Sachs Group Inc", "Home Depot Inc", "Honeywell International Inc", "International Business Machines Corp", "Intel Corp", "Johnson & Johnson", "Coca-Cola Co", "JPMorgan Chase & Co", "McDonald’s Corp", "Merck & Co Inc", "Microsoft Corp", "Nike Inc", "Procter & Gamble Co", "Travelers Companies Inc", "UnitedHealth Group Inc", "Salesforce.Com Inc", "Verizon Communications Inc", "Visa Inc", "Walgreens Boots Alliance Inc", "Walmart Inc", "Walt Disney Co", "Dow Inc"], key=str.casefold)

positiveWords = pd.read_csv("/Users/George/Documents/class/FIN 4450/Loughran_Mcdonald_word_list/LoughranMcDonald_Positive.csv", header=None, squeeze=True)

scores = {}
count = 0

directory = "/Users/George/Documents/class/FIN 4450/Articles"

for index, filename in enumerate(sorted(os.listdir(directory), key=str.casefold)):
    with open(os.path.join(directory, filename), 'r') as file:
        for line in file:
            line = rtf_to_text(line).split()
            for word in line:
                if word.upper() in positiveWords.values:
                    count += 1;
    scores[companies[index]] = count
    count = 0

sortedScores = {}
sortedKeys = sorted(scores, key=scores.get, reverse=True)

for k in sortedKeys:
    sortedScores[k] = scores[k]

print(sortedScores)
