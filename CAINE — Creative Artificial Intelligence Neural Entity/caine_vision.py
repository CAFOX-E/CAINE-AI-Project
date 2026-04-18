import torch
import warnings
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration
from transformers import GPT2LMHeadModel, GPT2Tokenizer

warnings.filterwarnings("ignore")

def awaken_vision_and_mind():
    print("Starting Caine's visual cortex and mind...")
    
    device = "cuda" if torch.cuda.is_available() else "cpu"
    
    # 1. The Eye (BLIP - Converts image into raw concept)
    print("[-] Loading Eye (BLIP)...")
    vision_processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
    vision_model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base").to(device)
    
    # 2. The Brain (The Caine personality you trained)
    print("[-] Connecting to Caine's Mind...")
    brain_path = "./caine_brain"
    
    try:
        mind_tokenizer = GPT2Tokenizer.from_pretrained(brain_path)
        mind_tokenizer.pad_token = mind_tokenizer.eos_token
        mind_model = GPT2LMHeadModel.from_pretrained(brain_path).to(device)
    except Exception as e:
        print(f"Error loading the local brain: {e}")
        return
    
    print("-" * 60)
    print("CAINE IS ONLINE AND NOW CAN SEE.")
    print("Enter the path of an image on your PC.")
    print("Type 'exit' to quit.")
    print("-" * 60)

    while True:
        image_path = input("\nImage Path > ").strip()
        
        if image_path.lower() == 'exit':
            print("Caine entering hibernation...")
            break
            
        try:
            # --- STEP 1: THE EYE SEES ---
            image = Image.open(image_path).convert('RGB')
            vision_inputs = vision_processor(image, return_tensors="pt").to(device)
            
            # Generates the literal description (Optic Nerve)
            vision_exit = vision_model.generate(**vision_inputs, max_new_tokens=20)
            concept_base = vision_processor.decode(vision_exit[0], skip_special_tokens=True)
            
            # We print what the eye saw raw, just for you to follow the internal logic
            print(f"  [Optic Nerve detected]: {concept_base}")
            
            # --- STEP 2: THE BRAIN THINKS ---
            # The raw text of the Eye becomes the initial trigger for Caine's Mind
            mind_inputs = mind_tokenizer(concept_base, return_tensors="pt").to(device)
            
            with torch.no_grad():
                mind_exit = mind_model.generate(
                    mind_inputs["input_ids"],
                    attention_mask=mind_inputs["attention_mask"],
                    max_new_tokens=50,       # How many more words can Caine invent
                    temperature=0.8,         # Level of abstraction/creativity
                    do_sample=True,
                    pad_token_id=mind_tokenizer.eos_token_id,
                    no_repeat_ngram_size=2
                )
            
            deep_thought = mind_tokenizer.decode(mind_exit[0], skip_special_tokens=True)
            
            # Formats Caine's final answer
            print(f"\nCaine > {deep_thought}")
            
        except Exception as e:
            print(f"Error trying to process the image. Check the path. (Detail: {e})")

if __name__ == "__main__":
    awaken_vision_and_mind()