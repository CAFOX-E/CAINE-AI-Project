import torch
import warnings
import os
import time
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration
from transformers import GPT2LMHeadModel, GPT2Tokenizer
from diffusers import StableDiffusionPipeline

warnings.filterwarnings("ignore")

def awaken_caine_artist():
    print("=" * 60)
    print("STARTING THE CAINE: THE COMPLETE CYCLE (VISION, MIND, AND ART)")
    print("=" * 60)
    
    # Hardware Detection
    if torch.cuda.is_available():
        device = "cuda"
        gpu_name = torch.cuda.get_device_name(0)
        # GTX 1660, 1650 and similar cards generate black images with float16
        GPUS_WITHOUT_FLOAT16 = ["1660", "1650", "1630", "1070", "1080", "1060", "1050"]
        user_float16 = not any(g in gpu_name for g in GPUS_WITHOUT_FLOAT16)
        dtype_art = torch.float16 if user_float16 else torch.float32
        print(f"Detected hardware: {gpu_name}")
        print(f"Precision: {"float16" if user_float16 else "float32 (compatibility mode)"}")
    else:
        device = "cpu"
        dtype_art = torch.float32 # Necessary for CPU, but very slow
        print("Detected hardware: CPU. Image generation will be EXTREMELY SLOW (5-15 min).")
    
    # Folders COnfigurations
    creations_folder = "./caine_creations"
    if not os.path.exists(creations_folder):
        os.makedirs(creations_folder)
        print(f"[-] Folder '{creations_folder}' created to save the artworks.")

    # 1. Loading the eye (BLIP)
    print("[-] Loading the Visual Cortex (BLIP)...")
    vision_processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
    vision_model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base").to(device)
    
    # 2. Loading the Mind (Trained GPT-2)
    print("[-] Loading Caine's Local Mind...")
    brain_path = "./caine_brain"
    try:
        mind_tokenizer = GPT2Tokenizer.from_pretrained(brain_path)
        mind_tokenizer.pad_token = mind_tokenizer.eos_token
        mind_model = GPT2LMHeadModel.from_pretrained(brain_path).to(device)
    except Exception as e:
        print(f"Critical error loading the trained brain: {e}")
        return
    
    # 3. Loading the Brush (Stable Diffusion)
    # We will use version v1-5, which is a good balance between quality and lightness
    print("[-] Preparing the Artistic Brush (Stable Diffusion v1-5)...")
    print("    (This may take a little while the first time, as it will download the model)")
    
    # Load the generation pipeline
    pipe_art = StableDiffusionPipeline.from_pretrained(
        "runwayml/stable-diffusion-v1-5", 
        torch_dtype=dtype_art,
        # Memory optimizations
        safety_checker=None, # Turn off the content filter to gain speed/memory
        requires_safety_checker=False
    )
    pipe_art = pipe_art.to(device)
    
    # Extra optimization for GPU
    if device == "cuda":
        pipe_art.enable_attention_slicing()

    print("-" * 60)
    print("CAINE IS COMPLETELY ONLINE. He sees, thinks, and paints.")
    print("Enter the path of an image to start the cycle.")
    print("Type 'exit' to quit.")
    print("-" * 60)

    while True:
        image_path = input("\nInput Image Path > ").strip()
        
        if image_path.lower() == 'exit':
            print("Caine entering hibernation...")
            break
            
        if not os.path.exists(image_path):
            print("File not found. Check the path.")
            continue
            
        try:
            start_process = time.time()
            print("\nStarting the creative cycle...")

            # --- STEP 1: THE EYE SEES ---
            print("[1/3] Caine is looking at the picture...")
            image_input = Image.open(image_path).convert('RGB')
            vision_inputs = vision_processor(image_input, return_tensors="pt").to(device)
            vision_exit = vision_model.generate(**vision_inputs, max_new_tokens=20)
            concept_base = vision_processor.decode(vision_exit[0], skip_special_tokens=True)
            print(f"      > Detected visual concept: '{concept_base}'")
            
            # --- STEP 2: THE BRAIN THINKS ---
            print("[2/3] Caine is processing abstract thought...")
            mind_inputs = mind_tokenizer(concept_base, return_tensors="pt").to(device)
            with torch.no_grad():
                mind_exit = mind_model.generate(
                    mind_inputs["input_ids"],
                    attention_mask=mind_inputs["attention_mask"],
                    max_new_tokens=60,
                    temperature=0.8,
                    do_sample=True,
                    pad_token_id=mind_tokenizer.eos_token_id,
                    no_repeat_ngram_size=2
                )
            deep_thought = mind_tokenizer.decode(mind_exit[0], skip_special_tokens=True)
            print(f"      > Caine's thought:\n      \"{deep_thought}\"")
            
            # --- STEP 3: THE BRUSH PAINTS ---
            print("[3/3] Caine began to paint the new, unseen image...")
            if device == "cpu":
                print("      (Please wait... This will take several minutes on the CPU)")

            # We formatted the final prompt for Stable Diffusion.
            # We took Caine's thought and forced the requested aesthetic.
            final_prompt = f"{deep_thought}, surrealism, weirdcore atmosphere, happyness, highly detailed, weird sensation, melancholic, human, masterpiece, nostalgic, liminal space"
            
            # Define how many steps the AI will use to create the image.
            # CPU: 15-20 steps (quality ok, "fast") | GPU: 30-50 steps (high quality)
            steps = 15 if device == "cpu" else 40

            # Generate the unprecedented image
            result = pipe_art(
                final_prompt, 
                num_inference_steps=steps, 
                guidance_scale=7.5 # How faithful should the AI be to the prompt (7 to 10 is the standard)
            )
            generated_image = result.images[0]
            
            # Save the image in the folder with a name based on the time to avoid overwriting
            timestamp = int(time.time())
            archive_name = f"caine_creations_{timestamp}.png"
            save_path = os.path.join(creations_folder, archive_name)
            generated_image.save(save_path)
            
            end_process = time.time()
            total_time = (end_process - start_process) / 60
            
            print(f"\n[-] SUCCESS! Cycle completed in {total_time:.1f} minutes.")
            print(f"[-] The new unprecedented image was silently saved in:\n    {save_path}")
            print("-" * 30)
            
        except Exception as e:
            print(f"An unexpected error occurred in the cycle: {e}")

if __name__ == "__main__":
    awaken_caine_artist()