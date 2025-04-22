# Krelyn Zacarias
# reTokenizer_SS
import re
import pandas as pd

# Loaded Practice Problems CSV from Google Sheets
csvFile = pd.read_csv("UpdatedProblemSets_SmallSet.csv")
practiceProblems = csvFile["Practice Problem"].astype(str).tolist()

# Using RE to tokenize and seperate the specific variables I want it to seperate in the problem
units = ["kg", "mv", "mph", "N", "cm", "mm", "J", "W", "s²", "IV", "m/s2"]
unitsRE = r"|".join(units)
patternRE = rf'\d+\.\d+|\d+|{unitsRE}|[a-zA-Z]+|[^\s\w]'

# Function to split units if needed
def splitNewUnits(token):
    if token in units: # Seperate if found in units
        return list(token)
    else:
        return [token]

# Tokenizing each practice problem 
tokenizedPracticeProblems = []

# Going through each word/variable and making sure it is being seperated
for problem in practiceProblems:
    tokens = re.findall(patternRE, problem)
    processed = []
    for token in tokens:
        processed.extend(splitNewUnits(token))
    tokenizedPracticeProblems.append(processed)

# Add tokens to a new CSV file
csvFile["Tokens"] = tokenizedPracticeProblems
csvFile.to_csv("tokenizerPracticeProblems_SS.csv", index=False)