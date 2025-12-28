# models/chat.py
from llama_cpp import Llama
import os
import json

# Download GGUF model on first run
MODEL_PATH = "mistral-7b-instruct-v0.3.Q4_K_M.gguf"
MODEL_REPO = "TheBloke/Mistral-7B-Instruct-v0.3-GGUF"

if not os.path.exists(MODEL_PATH):
    from huggingface_hub import hf_hub_download
    MODEL_PATH = hf_hub_download(
        repo_id=MODEL_REPO,
        filename="mistral-7b-instruct-v0.3.Q4_K_M.gguf"
    )

llm = Llama(
    model_path=MODEL_PATH,
    n_ctx=32768,
    n_threads=8,
    n_gpu_layers=0,  # CPU-only (no GPU needed)
    verbose=False
)

def generate_response(system_prompt: str, chat_history: list, user_input: str) -> str:
    """
    Generate a response using Mistral-7B (CPU-friendly GGUF)
    """
    messages = [{"role": "system", "content": system_prompt}]
    messages.extend(chat_history)
    messages.append({"role": "user", "content": user_input})
    
    try:
        response = llm.create_chat_completion(
            messages=messages,
            temperature=0.7,
            top_p=0.9,
            max_tokens=512,
            stop=["</s>", "User:", "Assistant:"]
        )
        return response["choices"][0]["message"]["content"].strip()
    except Exception as e:
        return f"Sorry, I'm having trouble thinking right now. Let's try again? 💬 ({str(e)[:50]}...)"