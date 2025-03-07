import re
import pandas as pd

# Loading the physics problems I have
physicsProblems = pd.read_csv("Practice Problems Initial Stage - Sheet1.csv")

# List of units (currently that I have) that should be split into individual characters that it doesn't recognize
units = ["kg","mv","mph", "N", "cm", "mm", "J", "W", "s²","IV"]

# Creating a regex pattern for the units that do not already seperate naturally
unitsRE = r"|".join(units)  
patternRE = rf'\d+\.\d+|\d+|{unitsRE}|[a-zA-Z]+|[^\s\w]'

newtokenizedProblems = []

# Looking through each token, and if it is in the units list, then it will be split into individual characters 
def splitNewUnits(token):
  if token in units:
    return list(token) 
  else:
    return [token]  

# Going through each token in the each sentence, and checking if unit list
for index, row in physicsProblems.iterrows():
    sentence = str(row['Practice Problem']) 
    tokens = re.findall(patternRE, sentence)

    processedTokensinProblem = []
    for token in tokens:
      for tok in splitNewUnits(token):
        processedTokensinProblem.append(tok)
        
    newtokenizedProblems.append(processedTokensinProblem)  

# Saved into a new CSV file
physicsProblems['Tokens'] = newtokenizedProblems
physicsProblems.to_csv("tokenizedPracticeProblems.csv", index=False)
