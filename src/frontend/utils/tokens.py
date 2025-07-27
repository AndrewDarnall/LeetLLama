""" Token Counter Utility """
from transformers import AutoTokenizer

# Cache globally so it's not reloaded every time
_tokenizer = None

def get_mistral_tokenizer():
    global _tokenizer
    if _tokenizer is None:
        _tokenizer = AutoTokenizer.from_pretrained("mistralai/Mistral-7B-v0.1", cache_dir="/app/tokenizer")
    return _tokenizer


def count_tokens(text: str) -> int:
    tokenizer = get_mistral_tokenizer()
    return len(tokenizer.encode(text))
