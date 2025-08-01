# backend/services/inference.py

from pathlib import Path

def run_inference(user_id: int, moduleCode: str, prompt: str):
    model_path = Path(f"models/user_{user_id}/{moduleCode}/trained_model.txt")

    if not model_path.exists():
        return None

    # Simulate response generation from fine-tuned text
    with open(model_path, "r", encoding="utf-8") as f:
        knowledge_base = f.read()

    # Simple keyword-based matching
    if prompt.lower() in knowledge_base.lower():
        return f"Relevant information found in moduleCode '{moduleCode}'."
    else:
        return f"No direct match found. Here is some context: {knowledge_base[:200]}..."
