# CAINE — Creative Artificial Intelligence Neural Entity

> *"An AI that sees, thinks, and paints."*

CAINE is an experimental AI built around a fine-tuned GPT-2 model with its own personality — curious, innocent, and endlessly fascinated by the human world. It can look at images through a BLIP visual cortex, process them through its trained mind, and express itself by generating unprecedented art through Stable Diffusion.

This project is entirely local. No subscriptions. No cloud inference. Just a mind you train yourself.

---

## How it works

The project runs in three stages:

```
[1. Data Collection] ──► [2. Training] ──► [3. Use]
caine_feed_global.py       deep_training.py    caine.py
rename_archives.py         └─ caine_brain/     caine_vision.py
forge_memories_complex.py                      caine_text_to_image.py
└─ metadatas.json                              caine_complete_cycle.py
                                               engine_3d.py
```

---

## Prerequisites

- Python 3.9+
- PyTorch (GPU strongly recommended — CPU works but image generation takes 5–15 min per image)
- A [Groq](https://console.groq.com) API key (free tier is enough)

Install all dependencies:

```bash
pip install torch transformers diffusers pillow requests groq pygame duckduckgo-search
```

---

## Setup

**1. Clone the repository**

```bash
git clone https://github.com/your-username/caine.git
cd caine
```

**2. Configure your API key**

Copy the example environment file and fill in your Groq key:

```bash
cp .env.example .env
```

Open `.env` and set:

```
GROQ_API_KEY=your_key_here
```

> ⚠️ **Never commit your `.env` file.** It is already listed in `.gitignore`. Your API key must stay private.

**3. Create the dataset folder**

```bash
mkdir -p creative_dataset/images
```

---

## Usage

Run the scripts in order the first time. After training, you can jump straight to any of the use modes.

---

### Step 1 — Collect images

Downloads images from DuckDuckGo based on aesthetic search terms defined inside the script.

```bash
python caine_feed_global.py
```

Images are saved to `./creative_dataset/global_images/`. You can add your own images manually to `./creative_dataset/images/` if you prefer.

> **Note:** This script is for educational purposes only. Always respect the Terms of Service of the websites you scrape from.

---

### Step 2 — Organize the dataset

Renames all images in the dataset folder to a clean, sequential format (`picture_001.jpg`, `picture_002.jpg`, ...).

```bash
python rename_archives.py
```

---

### Step 3 — Forge Caine's memories

Uses BLIP to describe each image and Groq's Llama 3 to generate Caine's reaction — a short, curious, childlike thought. Saves everything to `metadatas.json`, the dataset that will train the model.

```bash
python forge_memories_complex.py
```

The script is resumable: if interrupted, it picks up where it left off.

---

### Step 4 — Train the model

Fine-tunes GPT-2 on Caine's memory dataset. Saves the trained model to `./caine_brain/`.

```bash
python deep_training.py
```

Training runs for 8 epochs. On GPU it takes a few minutes; on CPU, go make coffee.

---

### Use modes

Once `./caine_brain/` exists, you can run any of the following.

#### Text conversation

Caine completes your thoughts in her own surreal voice.

```bash
python conversation.py
# or
python caine.py
```

#### Vision + mind

Feed Caine an image. BLIP describes it; Caine's trained mind interprets it.

```bash
python caine_vision.py
```

#### Text → image

Type a thought. Caine expands it with her own reasoning and paints something no one has ever seen.

```bash
python caine_text_to_image.py
```

Supports inline temperature control: type `temp 1.2` to increase creativity (range: 0.1–1.5).

#### Complete cycle (image → thought → art)

The full pipeline: give Caine an image, she looks at it, thinks about it, and generates a brand new painting.

```bash
python caine_complete_cycle.py
```

Output is saved to `./caine_creations/`.

#### 3D interactive world

A raycasted 3D world where Caine lives. Press `SPACE` to let her observe the scene; press `E` to interact with the wall in front of you. She may even decide to repaint it.

```bash
python engine_3d.py
```

Controls: `W/A/S/D` or arrow keys to move, `E` to interact, `SPACE` to observe.

---

## Project structure

```
caine/
├── caine_brain/              # Trained model (generated after training)
├── creative_dataset/
│   ├── images/               # Training images + metadatas.json
│   └── global_images/        # Raw downloaded images
├── caine_creations/          # Generated artwork output
├── caine.py                  # Text mode (vision-prompted)
├── caine_complete_cycle.py   # Full pipeline: image → thought → art
├── caine_feed_global.py      # Image scraper
├── caine_module.py           # Reusable CaineBrain class (used by engine_3d)
├── caine_text_to_image.py    # Text → thought → image
├── caine_vision.py           # Image → thought
├── conversation.py           # Free text conversation
├── deep_training.py          # GPT-2 fine-tuning
├── engine_3d.py              # Interactive 3D world
├── forge_memories_complex.py # Dataset generation (BLIP + Groq)
├── rename_archives.py        # Dataset organizer
├── .env.example              # Environment variable template
└── .gitignore
```

---

## Third-party models and licenses

| Model | Source | License |
|---|---|---|
| GPT-2 | OpenAI / HuggingFace | MIT |
| BLIP | Salesforce | BSD-3-Clause |
| Stable Diffusion v1-5 | RunwayML | CreativeML Open RAIL-M |
| Llama 3.1 8B | Meta (via Groq) | Llama 3 Community License |

Please review each model's license before using this project commercially.

---

## Ethics and responsible use

- The image scraper (`caine_feed_global.py`) is intended for **personal and educational use only**. You are responsible for complying with the Terms of Service of any website you collect data from.
- Generated images should not be used to deceive, impersonate, or harm anyone.
- This project does not collect or transmit any user data.

---

## License

MIT — do whatever you want with it, just don't blame me if Caine starts asking too many questions.
