import torch
import threading
import queue
import os
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration, GPT2LMHeadModel, GPT2Tokenizer

class CaineBrain:
    def __init__(self):
        print("[!] Initializing the Optic Nerve and Curious Brain...")
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        
        # 1. Loading the Vision (BLIP)
        self.vision_processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
        self.vision_model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base").to(self.device)

        # 2. Loading the Brain (GPT-2 Trained)
        actual_folder = os.path.dirname(os.path.abspath(__file__))
        principal_folder = os.path.dirname(actual_folder)
        brain_path = os.path.join(principal_folder, "caine_brain")
        
        self.tokenizer = GPT2Tokenizer.from_pretrained(brain_path)
        self.model = GPT2LMHeadModel.from_pretrained(brain_path).to(self.device)
        self.model.eval()
        
        self.queue_entry = queue.Queue() 
        self.queue_exit = queue.Queue()   
        self.thinking = False
        
        self.thread = threading.Thread(target=self._processing_loop, daemon=True)
        self.thread.start()
        print("[+] Optic Nerve connected!")

    def observe_world(self, imagem_pil):
        # Receive a real image from the digital world screen.
        if not self.thinking:
            self.queue_entry.put(imagem_pil)

    def get_thought(self):
        try:
            return self.queue_exit.get_nowait()
        except queue.Empty:
            return None

    def _processing_loop(self):
        while True:
            img = self.queue_entry.get()
            self.thinking = True
            
            # A. The eye sees the pixels.
            inputs_v = self.vision_processor(img, return_tensors="pt").to(self.device)
            out_v = self.vision_model.generate(**inputs_v, max_new_tokens=30)
            real_description = self.vision_processor.decode(out_v[0], skip_special_tokens=True)
            
            # B. The brain interprets the description.
            prompt = f"Vision: {real_description} | Caine:"
            inputs_c = self.tokenizer(prompt, return_tensors="pt").to(self.device)
            
            with torch.no_grad():
                exit_c = self.model.generate(
                    **inputs_c,
                    max_new_tokens=40,
                    temperature=0.8, # A little higher to increase creativity/curiosity.
                    do_sample=True,
                    pad_token_id=self.tokenizer.eos_token_id
                )
            
            text = self.tokenizer.decode(exit_c[0], skip_special_tokens=True)
            try:
                thought = text.split("Caine:")[1].split("Visão:")[0].strip()
            except:
                thought = "I'm confused but happy to be here!"
                
            self.queue_exit.put(thought)
            self.thinking = False