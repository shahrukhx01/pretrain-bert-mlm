import pandas as pd
from tqdm import tqdm
import time
from transformers import BertTokenizer
from transformers import LineByLineTextDataset
from transformers import BertForMaskedLM
from transformers import DataCollatorForLanguageModeling
from transformers import Trainer, TrainingArguments


## load model and tokenizer
tokenizer = BertTokenizer.from_pretrained("shahrukhx01/chemical-bert-uncased")
model = BertForMaskedLM.from_pretrained("shahrukhx01/chemical-bert-uncased")

## load dataset
dataset = LineByLineTextDataset(
    tokenizer=tokenizer,
    file_path="./dataset.txt",
    block_size=128,
)

## create data collator for Mask Language Modelling
data_collator = DataCollatorForLanguageModeling(
    tokenizer=tokenizer, mlm=True, mlm_probability=0.15
)

## training arguments for pretraining
training_args = TrainingArguments(
    output_dir="./chemical_bert",
    overwrite_output_dir=True,
    num_train_epochs=5,
    per_device_train_batch_size=64,
    save_steps=10_000,
    save_total_limit=2,
)

## create PyTorch Lightning trainer
trainer = Trainer(
    model=model,
    args=training_args,
    data_collator=data_collator,
    train_dataset=dataset,
)

## pretrain the model
trainer.train()


## save model to disk once training is done
trainer.save_model("./chemical-bert-uncased")
tokenizer.save_pretrained("./chemical-bert-uncased")
