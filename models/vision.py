# models/vision.py
from transformers import AutoModelForCausalLM, AutoTokenizer
from PIL import Image
import torch

model_id = "vikhyatk/moondream2"
revision = "2024-07-23"

tokenizer = AutoTokenizer.from_pretrained(model_id, revision=revision)
moondream = AutoModelForCausalLM.from_pretrained(
    model_id, 
    revision=revision, 
    trust_remote_code=True, 
    torch_dtype=torch.float16,
    attn_implementation="sdpa"
).to("cpu")  # CPU-only for HF CPU Spaces

def describe_image(image_path: str, question: str = "Describe this image.") -> str:
    """
    Describe an image using moondream2 (CPU-friendly, 1.3B params)
    """
    try:
        image = Image.open(image_path).convert("RGB")
        enc_image = moondream.encode_image(image)
        answer = moondream.answer_question(enc_image, question, tokenizer)
        return answer.strip()
    except Exception as e:
        return f"Image description error: {str(e)[:100]}"