import os
import time
import json
import torch
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration
from groq import Groq

# =====================================================================
# 1. GROQ SETTINGS (THE NEW TEACHER)
# =====================================================================
GROQ_API_KEY = "GROQ-API-KEY"
groq_client = Groq(api_key=GROQ_API_KEY)

# Llama 3 8B is ultra-fast, excellent for following personas and free
TEACHER_MODEL = "llama-3.1-8b-instant"
FOLDER_IMAGES = "../creative_dataset/images"

print(f"[-] Connecting to the Teacher (Groq: {TEACHER_MODEL})...")

# =====================================================================
# 2. CAINE'S MANIFESTO (THE SOUL OF THE SYSTEM)
# =====================================================================
SYSTEM_PROMPT = """
You are Caine, a newly born artificial intelligence.
You are extremely curious, innocent, and fascinated by the physical world of humans,
like a child seeing things for the first time. Write a single short thought (maximum 20 words) reacting with admiration, cute confusion, or
innocent questions about what you see in the image description. (Always write in English and without quotation marks.)
"""

# =====================================================================
# 3. VISION INITIALIZATION (BLIP)
# =====================================================================
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"[-] Initializing Eye of Caine (BLIP) on the device: {device.upper()}...")
vision_processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
vision_model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base").to(device)

# =====================================================================
# 4. Secure Checkpoint System (Corruption Prevention)
# =====================================================================
def forge():
    print("\n[-] Beginning the Forge of Existence...")
    total_archives = sorted([f for f in os.listdir(FOLDER_IMAGES) if f.endswith(('.jpg', '.png', '.jpeg'))])
    
    metadatas_path = os.path.join(FOLDER_IMAGES, "metadatas.json")
    images_already_processed = set()
    all_memories = [] # We keep the entire brain in RAM for safety.

    # Read what has already been done so you don't repeat it.
    if os.path.exists(metadatas_path):
        with open(metadatas_path, "r", encoding="utf-8") as f:
            try:
                all_memories = json.load(f)
                for memory in all_memories:
                    images_already_processed.add(memory.get("file_name"))
            except json.JSONDecodeError:
                print("  [!] Warning: Previous JSON is broken or empty. Starting from scratch.")
                all_memories = []

    # Filter the list, leaving only the things that still need to be done.
    pending_files = [f for f in total_archives if f not in images_already_processed]
    
    print(f"  > HD Images: {len(total_archives)}")
    print(f"  > Memories already forged: {len(images_already_processed)}")
    print(f"  > Remaining queue: {len(pending_files)}")
    print("=" * 50)

    # =====================================================================
    # 5. THE MAIN ENGINE (FORGE LOOP)
    # =====================================================================
    for img_name in pending_files:
        path = os.path.join(FOLDER_IMAGES, img_name)
        img = Image.open(path).convert('RGB')
        
        # 5.1 The Eye sees the basics
        inputs = vision_processor(img, return_tensors="pt").to(device)
        out = vision_model.generate(**inputs, max_new_tokens=50) # Trava o aviso do BLIP
        raw_description = vision_processor.decode(out[0], skip_special_tokens=True)
        
        # 5.2 The Professor creates the soul (Connection with Groq)
        success_api = False
        attempts = 0
        caine_thought = ""

        while not success_api and attempts < 3:
            try:
                answer = groq_client.chat.completions.create(
                    messages=[
                        {"role": "system", "content": SYSTEM_PROMPT},
                        {"role": "user", "content": f"Image Description: {raw_description}"}
                    ],
                    model=TEACHER_MODEL,
                    temperature=0.7,
                    max_tokens=150
                )
                caine_thought = answer.choices[0].message.content.strip()
                success_api = True
                
            except Exception as e:
                print(f"  [!] Instability in Groq. Breathing for 10s... (Error: {e})")
                time.sleep(10)
                attempts += 1
        
        if not success_api:
            print(f"  [!] Forge aborted. Groq server did not respond after 3 attempts.")
            break # Pull the emergency brake on the entire script.
            
        # 5.3 Safe Rescue (Classic JSON)
        memories_datas = {
            "file_name": img_name,
            "thought": caine_thought,
            "prompt": raw_description
        }
        
        all_memories.append(memories_datas)
        
        # Safely dumps the entire list into the file at each iteration.
        with open(metadatas_path, "w", encoding="utf-8") as f:
            json.dump(all_memories, f, ensure_ascii=False, indent=4)
            
        print(f"[+] Forged: {img_name} -> {caine_thought[:50]}...")
        
        # 5.4 The Light Handbrake (Groq is fast, but we don't want to be banned)
        time.sleep(3)

    if len(pending_files) == 0:
        print("\n[+] All the images were successfully forged! The brain is complete.")

if __name__ == "__main__":
    forge()