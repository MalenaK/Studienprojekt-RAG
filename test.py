# Use a pipeline as a high-level helper
# ACCESS CURRENTLY REQUESTED AND IN REVIEW FROM https://huggingface.co/meta-llama/Meta-Llama-3-8B-Instruct this would be needed to use tokenizers

from transformers import pipeline

messages = [
    {"role": "user", "content": "Who are you?"},
]
pipe = pipeline("text-generation", model="meta-llama/Meta-Llama-3-8B-Instruct")
pipe(messages)