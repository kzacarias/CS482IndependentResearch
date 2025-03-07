import pandas as pd
from transformers import BertTokenizer

# Importing the physics problems
physicsProblems = pd.read_csv("Practice Problems Initial Stage - Sheet1.csv")

# Loading BERT tokenizer
tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")

# Applying BERT tokenizer to each sentence
def tokenizeProblem(problem):
    problemString= str(problem) 
    return tokenizer.tokenize(problemString)

# Going through each sentence in the dataframe, and applying the tokenizer
physicsProblems['BERTTokens'] = physicsProblems['Practice Problem'].apply(tokenizeProblem)

# Saving tokenized problems into a new CSV file
physicsProblems.to_csv("tokenizedPracticeProblemsBERT.csv", index=False)

