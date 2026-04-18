import os
import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer

def awaken_caine():
    print("=" * 60)
    print("AWAKENING CAINE...")
    print("Loading the neural tensors from the folder './caine_brain'")
    print("=" * 60)

    actual_folder = os.path.dirname(os.path.abspath(__file__))
    brain_path = os.path.join(actual_folder, "caine_brain")
    
    # 1. Loading the trained mind
    try:
        tokenizer = GPT2Tokenizer.from_pretrained(brain_path)
        model = GPT2LMHeadModel.from_pretrained(brain_path)
    except Exception as e:
        print(f"[!] Error loading brain: {e}")
        print("Make sure the training saved the files in the 'caine_brain' folder.")
        return

    device = "cuda" if torch.cuda.is_available() else "cpu"
    model.to(device)
    model.eval() # Puts the model into "Read/Inference" mode (turns off training).

    print("[+] Caine is online and observing the world.")
    print("Type the description of an image in English (or 'exit' to log out).")
    print("-" * 60)

    # 2. The Conversation Loop
    while True:
        vision = input("\nVision (What is Caine seeing?): ")
        
        if vision.lower() in ['exit', 'quit']:
            print("Turning off Caine's circuits...")
            break
            
        if not vision.strip():
            continue

        # The exact format we use in the training (Cause and Effect)
        prompt = f"Vision: {vision} | Caine:"
        
        inputs = tokenizer(prompt, return_tensors="pt").to(device)
        
        # 3. Generation of Thought
        with torch.no_grad(): # Saves video card memory.
            exit = model.generate(
                **inputs,
                max_new_tokens=40, # Limit him so he doesn't talk too much (short thoughts).
                temperature=0.7,   # 0.7 keeps it poetic, but focused on training.
                do_sample=True,
                top_p=0.9,
                pad_token_id=tokenizer.eos_token_id
            )
            
        complete_text = tokenizer.decode(exit[0], skip_special_tokens=True)
        
        # 4. Cleaning the response (Cuts off the prompt and only takes Caine's response)
        try:
            thought = complete_text.split("Caine:")[1].strip()
            # If he tries to hallucinate and starts describing another vision, we cut the sentence.
            thought = thought.split("Visão:")[0].strip() 
        except IndexError:
            thought = complete_text
            
        print(f"\nCaine: \"{thought}\"")

if __name__ == "__main__":
    awaken_caine()