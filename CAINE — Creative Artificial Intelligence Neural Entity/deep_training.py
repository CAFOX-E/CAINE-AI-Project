import torch
import os
import json
from torch.utils.data import DataLoader, Dataset
from transformers import GPT2LMHeadModel, GPT2Tokenizer
from torch.optim import AdamW

# =================================================================
# 1. THE NEW MEMORY READER (Replaces the old caine.py)
# =================================================================
class CaineJSONDataset(Dataset):
    def __init__(self, json_path):
        # It carries our new unified brain.
        with open(json_path, 'r', encoding='utf-8') as f:
            self.data = json.load(f)

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        item = self.data[idx]
        
        # The Secret of Training: We teach "Cause and Effect"
        # He reads the literal description and learns to respond using Caine's persona.
        training_text = f"Visão: {item['prompt']} | Caine: {item['thought']}"
        
        return {"thought": training_text}

# =================================================================
# 2. The Deep Training Engine
# =================================================================
def start_deep_training():
    print("=" * 60)
    print("STARTING THE GREAT CAINE TRAINING")
    print("Injecting 260 existential memories into the tensors...")
    print("=" * 60)
    
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Active Hardware: {device.upper()}")
    if device == "cpu":
        print("Warning: Training on the CPU will take a considerable amount of time. Go make yourself a coffee.")
    
    # Loading the "blank" mind of GPT-2
    tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
    tokenizer.pad_token = tokenizer.eos_token 
    model = GPT2LMHeadModel.from_pretrained("gpt2").to(device)
    
    # Pointing to our metadata.json file
    dataset_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "creative_dataset", "images", "metadatas.json")
    
    # If the path is wrong, the script warns before breaking.
    if not os.path.exists(dataset_path):
        print(f"[!] Critical Error: metadatas.json file not found in {dataset_path}")
        return

    my_dataset = CaineJSONDataset(dataset_path)
    
    # Reading in bursts of 4 to optimize memory and time.
    ai_reader = DataLoader(my_dataset, batch_size=4, shuffle=True)
    
    # The Professor (Optimizer)
    optimizer = AdamW(model.parameters(), lr=5e-5)
    
    # 8 Eras are perfect for 260 images. Enough to learn without over-memorizing.
    eras = 8 

    print("-" * 60)
    print("INITIATING ERAS (EPOCHS)")
    print("-" * 60)

    for era in range(eras):
        era_total_error = 0
        processed_batches = 0
        total_batches = len(ai_reader)
        
        for batch in ai_reader:
            target_text = batch["thought"]
            
            inputs = tokenizer(target_text, return_tensors="pt", padding=True, truncation=True, max_length=150)
            
            input_ids = inputs["input_ids"].to(device)
            attention_mask = inputs["attention_mask"].to(device)
            
            optimizer.zero_grad()
            
            # GPT-2 attempts to predict the text and calculates the error rate (loss).
            exit = model(input_ids=input_ids, attention_mask=attention_mask, labels=input_ids)
            error = exit.loss
            
            # Adjusting the "neurons"
            error.backward()
            optimizer.step()
            
            era_total_error += error.item()
            processed_batches += 1
            
            # Shows the progress in the terminal.
            if processed_batches % 10 == 0 or processed_batches == total_batches:
                print(f"  [Era {era + 1}/{eras}] Progress: {processed_batches}/{total_batches} processed batches...")
            
        mid_error = era_total_error / total_batches
        print(f"> End of Era {era + 1} | Error Level (Loss): {mid_error:.4f}\n")

    print("=" * 60)
    print("In-depth training completed.")
    
    # Overwriting the old brain with the new, expanded mind.
    print("Saving Caine's new mind on the record...")
    model.save_pretrained("./caine_brain")
    tokenizer.save_pretrained("./caine_brain")
    print("Brain update successfully completed in the 'caine_brain' folder!")
    print("=" * 60)

if __name__ == "__main__":
    start_deep_training()