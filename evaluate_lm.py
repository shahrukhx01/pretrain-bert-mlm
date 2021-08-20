from transformers import pipeline

fill_mask = pipeline(
    "fill-mask",
    model="shahrukhx01/chemical-bert-uncased",
    tokenizer="shahrukhx01/chemical-bert-uncased",
)
fill_mask("we create [MASK]")
