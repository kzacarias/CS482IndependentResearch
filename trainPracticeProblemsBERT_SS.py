import pandas as pd
from datasets import Dataset
from transformers import AutoTokenizer, AutoModelForTokenClassification, TrainingArguments, Trainer

# Creating each of the lists as list
csvFile = pd.read_csv("labeledPracticeProblems_SS.csv")
csvFile["Tokens"] = csvFile["Tokens"].apply(eval)
csvFile["Labels"] = csvFile["Labels"].apply(eval)

# Building a dictionary based on the tokens and the labels corresponding to them
dictION = []
for index, row in csvFile.iterrows():
    dictION.append({
        "tokens": row["Tokens"],
        "labels": row["Labels"]
    })
dataset = Dataset.from_list(dictION)

# Create label mappings through enumeration (like in the example provided)
labels = set()
for row in dictION:
    labels.update(row["labels"])
labelNames = sorted(list(labels))
label2id = {label: i for i, label in enumerate(labelNames)}
id2label = {i: label for label, i in label2id.items()}

# Creating the tokenizer object w/ Bert uncased
tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")

def tokenize_and_align_labels(dictION):
    tokenized_inputs = tokenizer(
        dictION["tokens"],
        truncation=True,
        is_split_into_words=True,
        padding="max_length",
        max_length=128
    )

    labels = []
    for i, label in enumerate(dictION["labels"]):
        word_ids = tokenized_inputs.word_ids(batch_index=i)
        previous_word_idx = None
        label_ids = []
        for word_idx in word_ids:
            if word_idx is None:
                label_ids.append(-100)
            elif word_idx != previous_word_idx:
                label_ids.append(label2id[label[word_idx]])
            else:
                label_ids.append(-100)
            previous_word_idx = word_idx
        labels.append(label_ids)

    tokenized_inputs["labels"] = labels
    return tokenized_inputs

tokenized_dataset = dataset.map(
    tokenize_and_align_labels,
    batched=True,
    remove_columns=dataset.column_names
)


model = AutoModelForTokenClassification.from_pretrained("bert-base-uncased",num_labels=len(label2id),id2label=id2label,label2id=label2id)

training_args = TrainingArguments(
    output_dir="./results",
    evaluation_strategy="epoch",
    logging_strategy="epoch",
    save_strategy="epoch",
    per_device_train_batch_size=8,
    num_train_epochs=3,
    weight_decay=0.01,
    save_total_limit=2,
    logging_dir="./logs"
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset,
    eval_dataset=tokenized_dataset,
    tokenizer=tokenizer
)


trainer.train()

trainer.save_model("savedModelPracticeProblems_SS") 
tokenizer.save_pretrained("savedModelPracticeProblems_SS")