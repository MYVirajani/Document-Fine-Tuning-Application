import sys
from pathlib import Path

from services.fine_tune import fine_tune_model
from services.preprocessing import clean_and_save_document

def preprocess_documents(user_id: int, module_code: str):
    raw_dir = Path(f"data/user_{user_id}/{module_code}/raw")
    latest_dir = Path(f"data/user_{user_id}/{module_code}/latest")
    latest_dir.mkdir(parents=True, exist_ok=True)

    found_any = False
    for file_path in raw_dir.iterdir():
        if file_path.suffix.lower() in [".pdf", ".docx", ".pptx", ".txt"]:
            cleaned_file = clean_and_save_document(file_path)
            cleaned_file.rename(latest_dir / cleaned_file.name)
            print(f"Processed: {file_path.name}")
            found_any = True

    if not found_any:
        raise ValueError(f"No supported files found in {raw_dir}")

def main():
    if len(sys.argv) != 3:
        print("Usage: python train_llama.py <user_id> <moduleCode>")
        sys.exit(1)

    user_id = int(sys.argv[1])
    module_code = sys.argv[2]

    print("Step 1: Preprocessing raw documents...")
    preprocess_documents(user_id, module_code)

    print("Step 2: Starting fine-tuning...")
    fine_tune_model(user_id, module_code)

if __name__ == "__main__":
    main()
