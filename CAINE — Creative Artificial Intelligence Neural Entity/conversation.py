import torch
import warnings
from transformers import GPT2LMHeadModel, GPT2Tokenizer

warnings.filterwarnings("ignore")

def start_conversation():
    print("Awakening Caine (Local Brain)...")
    
    brain_path = "./caine_brain"
    
    try:
        # Load YOUR model and YOUR vocabulary saved in the folder
        tokenizer = GPT2Tokenizer.from_pretrained(brain_path)
        model = GPT2LMHeadModel.from_pretrained(brain_path)
    except Exception as e:
        print(f"Error loading the brain. Are you sure you ran the training and saved the folder? Error: {e}")
        return

    # Default GPT-2 configuration
    tokenizer.pad_token = tokenizer.eos_token
    model.eval() # Set the model to 'Reading/Generation Mode' (turn off training)

    print("-" * 50)
    print("CAINE ONLINE. Type the beginning of a thought for her to complete.")
    print("Example: 'The silence of the asphalt'")
    print("Type 'exit' to shut down.")
    print("-" * 50)

    while True:
        entrance = input("\nYOU > ")
        
        if entrance.lower() == 'exit':
            print("Turning off...")
            break
            
        if not entrance.strip():
            continue

        # Transform your text into tensors
        inputs = tokenizer(entrance, return_tensors="pt")
        
        # Generate the continuation
        with torch.no_grad(): # Ensures that we won't train/use memory for nothing
            exit = model.generate(
                inputs["input_ids"],
                attention_mask=inputs["attention_mask"],
                max_new_tokens=40,       # How many new words can she invent
                temperature=0.7,         # Creativity (0.1 = literal, 1.0 = very chaotic)
                do_sample=True,
                pad_token_id=tokenizer.eos_token_id,
                no_repeat_ngram_size=2   # Prevents her from repeating the same word several times
            )
            
        # Decodifica de volta para texto legível
        answer = tokenizer.decode(exit[0], skip_special_tokens=True)
        print(f"Caine > {answer}")

if __name__ == "__main__":
    start_conversation()