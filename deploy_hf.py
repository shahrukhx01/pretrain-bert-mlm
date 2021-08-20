## !apt-get install git-lfs
## git config --global user.email "sk28671@gmail.com"

from transformers import BertTokenizer
from transformers import BertForMaskedLM

model = BertForMaskedLM.from_pretrained("./chemical_bert")
model.push_to_hub("chemical-bert-uncased")

tokenizer = BertTokenizer.from_pretrained("./chemical_bert")
tokenizer.push_to_hub("chemical-bert-uncased")
