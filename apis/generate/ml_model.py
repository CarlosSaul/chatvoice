from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
import os
os.environ['TRANSFORMERS_CACHE'] = '/apis/.cache/models'

model = None

def init_transformer(model_name, tokenizer=None):
    global model

    if tokenizer is None:
        tokenizer = model_name

    tokenizer = AutoTokenizer.from_pretrained(tokenizer, cache_dir="/apis/.cache/models")
    model__ = AutoModelForCausalLM.from_pretrained(model_name, cache_dir="/apis/.cache/models")

    generator = pipeline("text-generation", model=model__, tokenizer=tokenizer)
    model = generator
    return model


def pre_process(text, use_lower=True):
    # If transform to lower
    if use_lower:
        text = text.lower()
    return text


def generate_transformer(text, candidate_labels, hypothesis_template, **args):
    global model

    text_ = pre_process(text, **args)
    res = model(text_)
    return res[0]['generated_text'], (text_, )
