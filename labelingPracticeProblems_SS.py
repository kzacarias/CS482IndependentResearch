import pandas as pd
import re

csvFile = pd.read_csv("tokenizerPracticeProblems_SS.csv")
csvFile["Tokens"] = csvFile["Tokens"].apply(eval)

# For each subject, there are different labeling rules for the variables
labelingRules = {
    "Kinematics": {
        "m": "METER",
        "v": "VELOCITY",
        "t": "TIME"
    },
    "Force and Torque": {
        "m": "MASS",
        "f": "FORCE"
    },
    "Centre of Mass": {
        "m": "MASS"
    },
    "Motion of Blocks on a Plane": {
        "m": "MASS"
    },
    "Motion on Incline": {
        "m": "MASS"
    },
    "Moment of Inertia": {
        "v": "VOLUME"
    },
    "Field and Potential": {
        "v": "VOLUME",
    },
    "Gauss's Law": {
        "v": "VOLTAGE"
    },
    "Collisions": {
        "p": "MOMENTUM"
    },
    "Rotational Dynamics": {
        "p": "MOMENTUM",
        "t": "TIME"
    },
    "Electric Circuits": {
        "p": "POWER"
    },
    "Rotational Kinematics": {
       "p": "PRESSURE"
    },
    "Oscillations": {
        "p": "PRESSURE"
    },
    "Fluid Dynamics": {
        "p": "PRESSURE"
    },
    "Particle Dynamics": {
        "f": "FORCE",
        "t": "TIME"
    },
    "Gravitation": {
        "m": "MASS",
        "f": "FORCE",
        "t": "TIME"
    },
    "Motion in a Horizontal Plane": {
        "f": "FREQUENCY"
    },
    "Waves": {
        "f": "FREQUENCY"
    },
    "Heat and Matter": {
        "t": "TEMPERATURE"
    },
    "Simple Harmonic Motion": {
        "t": "PERIOD"
    }
}

#Applying labels to specific varibles. If not in rules, then 'O' is provided as a filler
def labelTokens(row):
    tokens = row["Tokens"]
    subject = row["Subject"]
    rules = labelingRules.get(subject, {})
    labels = []
    for token in tokens:
        lowerToken = token.lower()
        label = rules.get(lowerToken, "O")
        labels.append(label)
    return labels

#Saving into a new CSV file with labels column
csvFile["Labels"] = csvFile.apply(labelTokens, axis=1)
csvFile.to_csv("labeledPracticeProblems_SS.csv", index=False)
