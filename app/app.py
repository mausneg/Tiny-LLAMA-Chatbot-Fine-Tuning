from fastapi import FastAPI, Request
from peft import AutoPeftModelForCausalLM
import os
from transformers import pipeline, AutoTokenizer
from utils.io import download_dir
from utils.data_model import Message

app = FastAPI()

MODEL_NAME = 'TinyLlama-1.1B-Chat-v1.1'
MODEL_PATH = f'saved_models/{MODEL_NAME}'

if not os.path.exists(MODEL_PATH):
    download_dir(MODEL_PATH, MODEL_NAME)

model = AutoPeftModelForCausalLM.from_pretrained(
    MODEL_PATH,
    device_map='auto',
    load_in_8bit=True,
)

merged_model = model.merge_and_unload()

tokenizer = AutoTokenizer.from_pretrained('TinyLlama/TinyLlama-1.1B-intermediate-step-1431k-3T', trust_remote_code=True)
tokenizer.pad_token = '<PAD>'
tokenizer.padding_size = 'left'

pipe = pipeline('text-generation', model=merged_model, tokenizer=tokenizer)

conversation_history = []

def add_to_conversation(role, message):
    conversation_history.append(f"<|{role}|>\n{message}")

def get_full_prompt():
    return "\n".join(conversation_history) + "\n<|assistant|>\n"

def get_recent_messages(n=6):
    return "\n".join(conversation_history[-n:]) + "\n<|assistant|>\n"

@app.post("/api/v1/conversation")
async def conversation_endpoint(data: Message):
    user_message = "\n".join(data.content)
    add_to_conversation("user", user_message)
    full_prompt = get_recent_messages(n=4)
    response = pipe(full_prompt)
    assistant_message = response[0]['generated_text']
    add_to_conversation("assistant", assistant_message)
    return {"response": assistant_message}