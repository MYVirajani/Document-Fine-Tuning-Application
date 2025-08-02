# # backend/services/inference.py

# from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
# from peft import PeftModel
# from pathlib import Path
# import torch

# # Global caching
# tokenizer = None
# model = None

# def load_lora_model(base_model_path: str, adapter_path: Path):
#     global tokenizer, model

#     tokenizer = AutoTokenizer.from_pretrained(base_model_path, trust_remote_code=True)
#     base_model = AutoModelForCausalLM.from_pretrained(
#         base_model_path,
#         trust_remote_code=True,
#         torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32
#     )

#     tokenizer.pad_token = tokenizer.eos_token  # Prevent tokenizer errors

#     model = PeftModel.from_pretrained(base_model, adapter_path)

#     device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
#     model.to(device)

#     return tokenizer, model

# def generate_response(user_id: int, module_code: str, prompt: str) -> str:
#     global tokenizer, model

#     adapter_path = Path(f"models/user_{user_id}/{module_code}/llama_adapter")
#     if not adapter_path.exists():
#         raise FileNotFoundError(f"Adapter path not found: {adapter_path}")

#     base_model_path = "meta-llama/Llama-2-7b-hf"

#     if tokenizer is None or model is None:
#         tokenizer, model = load_lora_model(base_model_path, adapter_path)

#     pipe = pipeline(
#         "text-generation",
#         model=model,
#         tokenizer=tokenizer,
#         device=0 if torch.cuda.is_available() else -1
#     )

#     outputs = pipe(prompt, max_new_tokens=300, do_sample=True, temperature=0.7)
#     return outputs[0]["generated_text"][len(prompt):].strip()


from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
from peft import PeftModel
from pathlib import Path
import torch
import os

# Global cache
tokenizer = None
model = None

def load_lora_model(base_model_path: str, adapter_path: Path):
    global tokenizer, model

    hf_token = os.environ.get("HF_TOKEN")

    tokenizer = AutoTokenizer.from_pretrained(base_model_path, trust_remote_code=True, use_auth_token=hf_token)
    base_model = AutoModelForCausalLM.from_pretrained(
        base_model_path,
        trust_remote_code=True,
        torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
        use_auth_token=hf_token
    )

    tokenizer.pad_token = tokenizer.eos_token  # avoid errors

    model = PeftModel.from_pretrained(base_model, adapter_path)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)

    return tokenizer, model

def generate_response(user_id: int, module_code: str, prompt: str) -> str:
    global tokenizer, model

    adapter_path = Path(f"models/user_{user_id}/{module_code}/llama_adapter")
    if not adapter_path.exists():
        raise FileNotFoundError(f"Adapter path not found: {adapter_path}")

    base_model_path = "meta-llama/Llama-2-7b-hf"

    if tokenizer is None or model is None:
        tokenizer, model = load_lora_model(base_model_path, adapter_path)

    pipe = pipeline(
        "text-generation",
        model=model,
        tokenizer=tokenizer,
        device=0 if torch.cuda.is_available() else -1,
        max_length=512,
        do_sample=True,
        temperature=0.7,
        top_p=0.9,
        top_k=50,
        repetition_penalty=1.1,
    )

    output = pipe(prompt, max_new_tokens=300)
    generated_text = output[0]["generated_text"]

    # Remove prompt from generated output (to return only completion)
    if generated_text.startswith(prompt):
        generated_text = generated_text[len(prompt):]

    return generated_text.strip()
