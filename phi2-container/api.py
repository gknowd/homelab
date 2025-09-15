from fastapi import FastAPI
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

app = FastAPI()

model = AutoModelForCausalLM.from_pretrained("/app/model")
tokenizer = AutoTokenizer.from_pretrained("/app/model")

@app.post("/generate")
async def generate_text(prompt: str):
    inputs = tokenizer(prompt, return_tensors="pt")
    outputs = model.generate(inputs.input_ids, max_length=200)
    return {"response": tokenizer.decode(outputs[0], skip_special_tokens=True)}
