from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from openai import OpenAI 
import os

router = APIRouter()
client = OpenAI (api_key = os.getenv("")) 

class TextInput (BaseModel):
    text: str
    language: str = "ta"

@router.post ("/prompt_chain")
async def prompt_chain (input: TextInput):


    summary = client.chat.completions.create (
        model = "gpt-4", 
        messages = [
            {"role": "system", "content" : "Summarize the following text"},
            {"role" : "user","content" : input.text}
        ], 
        temperature = 0.4
    ).choices[0].message.content.strip()
    
    improved_text = client.chat.completions.create (
    model = "gpt-4", 
    messages = [
        {"role": "system", "content" : "Improve grammar and clarity of this text"},
        {"role" : "user","content" : input.text}
    ], 
    temperature = 0.3
).choices[0].message.content.strip()

    translated_text = client.chat.completions.create (
    model = "gpt-4", 
    messages = [
        {"role": "system", "content" : f"Translate the following text to {input.language}."},
        {"role" : "user","content" : improved_text}
    ], 
    temperature = 0.3
    ).choices[0].message.content.strip()

    return {
        "summary" : summary,
        "improved_text" : improved_text,
        "translated_text" : translated_text
    }

    