# # backend/services/fine_tune.py

# from pathlib import Path
# from datasets import Dataset
# from transformers import (
#     AutoTokenizer,
#     AutoModelForCausalLM,
#     TrainingArguments,
#     Trainer
# )
# from peft import LoraConfig, get_peft_model
# import torch


# def fine_tune_model(user_id: int, moduleCode: str):
#     base_model = "meta-llama/Llama-2-7b-hf"  # Update if you're using local path
#     data_path = Path(f"data/user_{user_id}/{moduleCode}/latest")
#     output_dir = Path(f"models/user_{user_id}/{moduleCode}/llama_adapter")
#     output_dir.mkdir(parents=True, exist_ok=True)

#     # Load and concatenate cleaned training data
#     raw_text = ""
#     for file in data_path.glob("*.cleaned.txt"):
#         raw_text += file.read_text(encoding="utf-8") + "\n"

#     if not raw_text.strip():
#         raise ValueError(f"No valid data found in {data_path}")

#     dataset = Dataset.from_dict({"text": [raw_text]})

#     # Load tokenizer and base model
#     tokenizer = AutoTokenizer.from_pretrained(base_model, trust_remote_code=True)
#     tokenizer.pad_token = tokenizer.eos_token

#     model = AutoModelForCausalLM.from_pretrained(
#         base_model,
#         torch_dtype=torch.float32,  # Can also be torch.bfloat16 or torch.float16 if supported
#     )

#     # Configure LoRA
#     peft_config = LoraConfig(
#         r=8,
#         lora_alpha=32,
#         target_modules=["q_proj", "v_proj"],
#         lora_dropout=0.05,
#         bias="none",
#         task_type="CAUSAL_LM",
#     )
#     model = get_peft_model(model, peft_config)

#     # Tokenization
#     def tokenize_function(examples):
#         return tokenizer(examples["text"], padding="max_length", truncation=True, max_length=512)

#     tokenized_dataset = dataset.map(tokenize_function, batched=True)

#     # Training arguments
#     training_args = TrainingArguments(
#         output_dir=str(output_dir),
#         per_device_train_batch_size=2,
#         num_train_epochs=3,
#         logging_dir=str(output_dir / "logs"),
#         save_strategy="epoch",
#         logging_steps=10,
#         report_to="none",
#     )

#     trainer = Trainer(
#         model=model,
#         args=training_args,
#         train_dataset=tokenized_dataset,
#         tokenizer=tokenizer,
#     )

#     trainer.train()

#     # Save model and tokenizer
#     model.save_pretrained(str(output_dir))
#     tokenizer.save_pretrained(str(output_dir))

#     return str(output_dir)


from pathlib import Path
from datasets import Dataset
from transformers import AutoTokenizer, AutoModelForCausalLM, TrainingArguments, Trainer
from peft import LoraConfig, get_peft_model
import torch
import os
from config import HF_TOKEN

def fine_tune_model(user_id: int, moduleCode: str):
    print("Fine-tuning started!")
    base_model = "meta-llama/Llama-2-7b-hf"  # HF gated model
    
    # Optional: Use environment variable HF_TOKEN or replace with your token string here
    hf_token = HF_TOKEN  # make sure this is set
    if not hf_token:
        raise ValueError("HF_TOKEN is not set. Please set it in your environment or .env file.")
    
    data_path = Path(f"data/user_{user_id}/{moduleCode}/latest")
    output_dir = Path(f"models/user_{user_id}/{moduleCode}/llama_adapter")
    output_dir.mkdir(parents=True, exist_ok=True)

    # Load and concatenate cleaned training data
    raw_text = ""
    for file in data_path.glob("*.cleaned.txt"):
        raw_text += file.read_text(encoding="utf-8") + "\n"

    if not raw_text.strip():
        raise ValueError(f"No valid data found in {data_path}")

    dataset = Dataset.from_dict({"text": [raw_text]})

    # Load tokenizer and base model with authentication token
    tokenizer = AutoTokenizer.from_pretrained(
        base_model,
        trust_remote_code=True,
        # use_auth_token=hf_token,
        token=hf_token
    )
    tokenizer.pad_token = tokenizer.eos_token

    model = AutoModelForCausalLM.from_pretrained(
        base_model,
        torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
        trust_remote_code=True,
        # use_auth_token=hf_token,
        token=hf_token
    )

    # Configure LoRA
    peft_config = LoraConfig(
        r=8,
        lora_alpha=32,
        target_modules=["q_proj", "v_proj"],
        lora_dropout=0.05,
        bias="none",
        task_type="CAUSAL_LM",
    )
    model = get_peft_model(model, peft_config)

    # Tokenization function
    def tokenize_function(examples):
        return tokenizer(
            examples["text"],
            padding="max_length",
            truncation=True,
            max_length=512,
        )

    tokenized_dataset = dataset.map(tokenize_function, batched=True)

    # Training arguments
    training_args = TrainingArguments(
        output_dir=str(output_dir),
        per_device_train_batch_size=1,  # very large model, keep small batch
        num_train_epochs=3,
        logging_dir=str(output_dir / "logs"),
        save_strategy="epoch",
        logging_steps=10,
        report_to="none",
        fp16=torch.cuda.is_available(),
        push_to_hub=False,
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=tokenized_dataset,
        tokenizer=tokenizer,
    )

    trainer.train()

    # Save fine-tuned model and tokenizer
    model.save_pretrained(str(output_dir))
    tokenizer.save_pretrained(str(output_dir))

    print(f"Fine-tuning completed. Model saved at {output_dir}")
    return str(output_dir)


if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("Usage: python fine_tune.py <user_id> <moduleCode>")
        sys.exit(1)
    user_id = int(sys.argv[1])
    module_code = sys.argv[2]
    fine_tune_model(user_id, module_code)
