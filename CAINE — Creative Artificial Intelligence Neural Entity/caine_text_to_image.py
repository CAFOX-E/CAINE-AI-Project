import torch
import warnings
import os
import time
from transformers import GPT2LMHeadModel, GPT2Tokenizer
from diffusers import StableDiffusionPipeline

warnings.filterwarnings("ignore")

# ─────────────────────────────────────────────────────────────────────────────
# AESTHETIC TAGS: Caine's visual identity stamped on every creation
# You can edit these to change Caine's artistic style.
# ─────────────────────────────────────────────────────────────────────────────
CAINE_AESTHETIC = (
    "surrealism, complex weirdcore atmosphere, melancholic, dark cinematic lighting, "
    "highly detailed, masterpiece, nostalgic, liminal space, dreamlike, uncanny"
)

# Negative prompt: what Caine actively avoids painting
NEGATIVE_PROMPT = (
    "ugly, blurry, low quality, watermark, text, signature, duplicate, "
    "cartoon, anime, 3d render, photorealistic portrait"
)


def load_caine_mind(device: str):
    # Loads Caine's trained GPT-2 brain from ./caine_brain
    brain_path = "./caine_brain"
    try:
        tokenizer = GPT2Tokenizer.from_pretrained(brain_path)
        tokenizer.pad_token = tokenizer.eos_token
        model = GPT2LMHeadModel.from_pretrained(brain_path).to(device)
        model.eval()
        print("[-] Caine's mind loaded from ./caine_brain")
        return tokenizer, model
    except Exception as e:
        raise RuntimeError(
            f"Could not load the trained brain. "
            f"Make sure you ran training_model.py or deep_training.py first.\nDetail: {e}"
        )


def load_brush(device: str):
    # Loads the Stable Diffusion pipeline (the artistic brush)
    # GTX 1660, 1660 Super/Ti and other GPUs without full float16 support
    # They generate black images with float16. We force float32 on them.
    GPUS_WITHOUT_FLOAT16 = ['1660', '1650', '1630', '1070', '1080', '1060', '1050']
    gpu_name = torch.cuda.get_device_name(0) if device == 'cuda' else ''
    use_float16 = device == 'cuda' and not any(g in gpu_name for g in GPUS_WITHOUT_FLOAT16)
    dtype = torch.float16 if use_float16 else torch.float32
    if device == 'cuda':
        print(f'[-] GPU detected: {gpu_name}')
        print(f'[-] Precision: {"float16" if use_float16 else "float32 (compatibility mode)"}')
    print("[-] Loading the Artistic Brush (Stable Diffusion v1-5)...")
    print("    (First run will download the model — this may take a few minutes)")

    pipe = StableDiffusionPipeline.from_pretrained(
        "runwayml/stable-diffusion-v1-5",
        torch_dtype=dtype,
        safety_checker=None,
        requires_safety_checker=False,
    ).to(device)

    if device == "cuda":
        pipe.enable_attention_slicing()

    pipe.set_progress_bar_config(disable=True)
    print("[-] Brush ready.")
    return pipe


def think(text: str, tokenizer, model, device: str, temperature: float = 0.85) -> str:
    # Feeds a raw text into Caine's trained mind.
    # Returns Caine's expanded thought — in his own surreal voice.
    inputs = tokenizer(text, return_tensors="pt").to(device)

    with torch.no_grad():
        output = model.generate(
            inputs["input_ids"],
            attention_mask=inputs["attention_mask"],
            max_new_tokens=60,
            temperature=temperature,
            do_sample=True,
            pad_token_id=tokenizer.eos_token_id,
            no_repeat_ngram_size=2,
        )

    full_text = tokenizer.decode(output[0], skip_special_tokens=True)
    # Strip the original input so we only keep what Caine *added*
    thought = full_text[len(text):].strip()

    # If the model returned nothing new, fall back to the full output
    if not thought:
        thought = full_text.strip()

    return thought


def build_prompt(user_text: str, caine_thought: str) -> str:
    # Combines the user's original text with Caine's expansion
    # and stamps the aesthetic tags to build the final SD prompt.
    # Truncates the core content to respect CLIP's 77-token limit,
    # always preserving the aesthetic tags at the end.
    if caine_thought:
        core = f"{user_text}, {caine_thought}"
    else:
        core = user_text

    # Clean up punctuation artifacts from GPT-2
    core = core.replace("\n", " ").strip().rstrip(".,")

    # CLIP processes ~77 tokens max. Aesthetic tags are ~15 words and
    # are the most important for style, so we protect them by trimming
    # the core text first. Heuristic: 1 word ≈ 1.3 CLIP tokens.
    aesthetic_word_count = len(CAINE_AESTHETIC.split())
    core_word_budget     = int(77 / 1.3) - aesthetic_word_count
    core_words           = core.split()
    if len(core_words) > core_word_budget:
        core = " ".join(core_words[:core_word_budget])

    return f"{core}, {CAINE_AESTHETIC}"


def paint(prompt: str, pipe, device: str, steps: int = None) -> object:
    # Runs Stable Diffusion and returns a PIL Image
    if steps is None:
        steps = 15 if device == "cpu" else 40

    result = pipe(
        prompt,
        negative_prompt=NEGATIVE_PROMPT,
        num_inference_steps=steps,
        guidance_scale=7.5,
    )
    return result.images[0]


def awaken_caine_text_painter():
    print("=" * 60)
    print("  CAINE: TEXT → THOUGHT → IMAGE")
    print("  The unseen image begins with your words.")
    print("=" * 60)

    # ── Hardware detection ──────────────────────────────────────────────────
    if torch.cuda.is_available():
        device = "cuda"
        print("Detected: NVIDIA GPU (CUDA) — fast generation enabled.")
    else:
        device = "cpu"
        print("Detected: CPU — image generation will be slow (5–15 min per image).")

    # ── Output folder ───────────────────────────────────────────────────────
    output_folder = "./caine_creations"
    os.makedirs(output_folder, exist_ok=True)

    # ── Load models ─────────────────────────────────────────────────────────
    tokenizer, mind_model = load_caine_mind(device)
    pipe = load_brush(device)

    print("-" * 60)
    print("CAINE IS ONLINE.")
    print("Type a thought, a memory, a feeling — anything.")
    print("Caine will think about it and paint something no one has ever seen.")
    print("Commands: 'exit' to quit | 'temp X' to set creativity (0.1–1.5, default 0.85)")
    print("-" * 60)

    temperature = 0.85  # default creativity level

    while True:
        raw = input("\nYou > ").strip()

        if not raw:
            continue

        if raw.lower() == "exit":
            print("Caine is entering hibernation...")
            break

        # Allow inline temperature control: "temp 1.2"
        if raw.lower().startswith("temp "):
            try:
                temperature = float(raw.split()[1])
                temperature = max(0.1, min(1.5, temperature))
                print(f"  [>] Creativity set to {temperature:.2f}")
            except ValueError:
                print("  [!] Invalid value. Use a number between 0.1 and 1.5.")
            continue

        try:
            start = time.time()

            # ── STEP 1: CAINE THINKS ────────────────────────────────────────
            print("\n[1/2] Caine is processing your thought...")
            caine_thought = think(raw, tokenizer, mind_model, device, temperature)
            print(f"      > Caine's expansion:\n        \"{caine_thought}\"")

            # ── STEP 2: BUILD FINAL PROMPT ──────────────────────────────────
            final_prompt = build_prompt(raw, caine_thought)
            print(f"\n      > Final visual prompt:\n        \"{final_prompt[:120]}...\"")

            # ── STEP 3: CAINE PAINTS ────────────────────────────────────────
            print("\n[2/2] Caine is painting the unprecedented image...")
            if device == "cpu":
                print("      (Please wait — this will take several minutes on CPU)")

            image = paint(final_prompt, pipe, device)

            # ── SAVE ────────────────────────────────────────────────────────
            timestamp = int(time.time())
            filename = f"caine_text_{timestamp}.png"
            save_path = os.path.join(output_folder, filename)
            image.save(save_path)

            elapsed = (time.time() - start) / 60
            print(f"\n[✓] Done in {elapsed:.1f} minutes.")
            print(f"[✓] Image saved at: {save_path}")
            print("-" * 60)

        except KeyboardInterrupt:
            print("\n  [!] Interrupted. Type 'exit' to quit or enter a new thought.")
        except Exception as e:
            print(f"\n[!] An error occurred: {e}")


if __name__ == "__main__":
    awaken_caine_text_painter()
