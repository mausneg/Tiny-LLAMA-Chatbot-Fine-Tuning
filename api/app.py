from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from peft import AutoPeftModelForCausalLM
import os
from transformers import pipeline, AutoTokenizer
from utils.io import download_dir
from utils.data_model import Message
import re

app = FastAPI(title="TinyLlama Chat API", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

MODEL_NAME = 'TinyLlama-1.1B-Chat-v1.2'
MODEL_PATH = f'saved_models/{MODEL_NAME}'
MAX_LENGTH = 2048

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
    prompt = "\n".join(conversation_history) + "\n<|assistant|>\n"
    tokens = tokenizer.encode(prompt, add_special_tokens=False)
    if len(tokens) > MAX_LENGTH:
        tokens = tokens[-MAX_LENGTH:]
    trimmed_prompt = tokenizer.decode(tokens, skip_special_tokens=True)
    return trimmed_prompt

def get_recent_messages(n=4):
    return "\n".join(conversation_history[-n:]) + "\n<|assistant|>\n"

@app.post("/api/v1/conversation")
async def conversation_endpoint(data: Message):
    user_message = "\n".join(data.content)
    add_to_conversation("user", user_message)
    full_prompt = get_full_prompt()
    response = pipe(full_prompt)
    assistant_message = response[0]['generated_text']
    add_to_conversation("assistant", assistant_message)
    return {"response": assistant_message}

@app.delete("/api/v1/conversation")
async def clear_conversation():
    global conversation_history
    conversation_history = []
    return {"message": "Conversation cleared", "status": "success"}