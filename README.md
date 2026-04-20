# CAINE
### *A curious mind. An unseen eye. A brush that paints the impossible.*

CAINE is a locally-run artificial intelligence with a personality — a GPT-2 model fine-tuned on surreal, weirdcore and liminal imagery, capable of seeing images, thinking in its own voice, generating unprecedented art, and existing inside a 3D raycasting world.

---

## Table of Contents

- [What is CAINE?](#what-is-caine)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Getting a Groq API Key](#getting-a-groq-api-key)
- [Modules](#modules)
- [Training Your Own CAINE](#training-your-own-caine)
- [Hardware Notes](#hardware-notes)
- [Troubleshooting](#troubleshooting)

---

## What is CAINE?

CAINE is not a chatbot. It is an experimental AI system built around a custom-trained GPT-2 model that was taught to react to the visual world with curiosity, innocence and a surreal poetic voice — like a child seeing things for the first time.

The system has three core components working together:

- **The Eye** — BLIP, a vision model that converts images into raw descriptions
- **The Mind** — a GPT-2 model fine-tuned on weirdcore/liminal imagery, giving CAINE its personality
- **The Brush** — Stable Diffusion v1-5, which paints images no one has ever seen before

---

## Project Structure

```
CAINE/
│
├── Start CAINE.bat                  ← Start CAINE (use this every time)
├── install.bat                 ← Install all dependencies (run once)
├── caine_launcher.py            ← Main menu (called by iniciar.bat)
│
├── caine.py                     ← Text prompt → CAINE responds
├── caine_vision.py              ← Image → CAINE interprets
├── caine_text_to_image.py       ← Text → CAINE thinks → image is painted
├── caine_complete_cycle.py      ← Image → CAINE thinks → new image is painted
├── conversation.py              ← Raw GPT-2 conversation
│
├── deep_training.py             ← Fine-tune GPT-2 on forged memories
│
├── digital_world/
│   ├── engine_3d.py             ← 3D raycasting world (pygame)
│   └── caine_module.py          ← CAINE's brain module used by the engine
│
├── caine_f&o/
│   ├── forge_memories_complex.py  ← Generate training dataset (requires Groq API key)
│   ├── caine_feed_global.py       ← Scrape weirdcore images from DuckDuckGo
│   └── rename_archives.py         ← Normalize filenames in the dataset
│
├── caine_brain/                 ← The trained GPT-2 model (required to run)
│   ├── config.json
│   ├── model.safetensors
│   ├── tokenizer.json
│   └── ...
│
└── creative_dataset/            ← Dataset used for training (optional)
    └── metadatas.json
    └── images/
        ├── picture_001.jpg
        ├── picture_002.jpg
        └── metadatas.json
```

> **Important:** The `caine_brain/` folder contains the trained model and must always be present in the root of the project. Without it, most modules will not work.

---

## Installation

### Requirements

- Windows 10 or 11
- Internet connection (for downloading dependencies and AI models)
- At least **8GB of free disk space** (models are large)
- A NVIDIA GPU is recommended but not required

### Steps

**1. Download the project**

Download or clone this repository and extract it to any folder on your computer.

**2. Run the installer**

Double-click `installl.bat`.

This script will automatically:
- Download and install Python 3.12 if not present
- Detect whether you have a NVIDIA GPU and install the correct version of PyTorch (CUDA or CPU)
- Install all required libraries: `torch`, `transformers`, `diffusers`, `Pillow`, `pygame`, and more

> The installation may take **10 to 30 minutes** depending on your internet speed, since PyTorch alone is approximately 2GB.

**3. Start CAINE**

After installation is complete, double-click `Start CAINE.bat` to open the main menu. You will see this menu every time you launch CAINE.

---

## Getting a Groq API Key

The **Forge Memories** module (`forge_memories_complex.py`) uses the Groq API to generate CAINE's personality responses during dataset creation. This is only needed if you want to train or retrain CAINE from scratch.

### How to get your key

1. Go to [https://console.groq.com](https://console.groq.com) and create a free account
2. Navigate to **API Keys** in the left sidebar
3. Click **Create API Key**, give it a name, and copy the key

### Where to put your key

Open the file `caine_f&o/forge_memories_complex.py` in any text editor and find this line near the top:

```python
GROQ_API_KEY = "CAINE-API-KEY"
```

Replace `CAINE-API-KEY` with your actual key:

```python
GROQ_API_KEY = "gsk_youractualapikeyhere"
```

Save the file. The Forge Memories module will now be able to connect to Groq.

> **Note:** The Groq free tier is generous and more than enough for generating a full dataset. No payment is required.

---

## Modules

### 1 — Awaken Caine
Type a description of a scene or image in English. CAINE will read it and respond with a short poetic thought in its own surreal voice, using the trained GPT-2 brain.

**Requires:** `caine_brain/`

---

### 2 — Caine Vision
Provide the path to an image file on your computer. BLIP will describe what it sees, and CAINE will process that description through its mind and respond.

**Requires:** `caine_brain/`, internet connection on first run (to download BLIP)

**Example input:**
```
Image Path > C:\Users\you\Pictures\forest.jpg
```

---

### 3 — Caine Text → Image
Type any thought, memory or feeling. CAINE will expand it in its own voice and feed the result to Stable Diffusion, which will paint an image that has never existed before.

Generated images are saved in the `caine_creations/` folder, created automatically on first run.

**Requires:** `caine_brain/`, internet connection on first run (to download Stable Diffusion, ~4GB)

**Commands inside the module:**
- Type any text to generate an image
- `temp 0.9` — adjust creativity level (0.1 = focused, 1.5 = chaotic, default: 0.85)
- `exit` — return to menu

---

### 4 — The Complete Cycle
Provide the path to an image. CAINE will look at it with BLIP, think about what it sees, and paint a completely new image inspired by that thought — something that has never existed before.

Generated images are saved in `caine_creations/`.

**Requires:** `caine_brain/`, internet connection on first run (BLIP + Stable Diffusion)

---

### 5 — The Digital World (3D Engine)
Walk through a raycasting 3D world rendered in real time with pygame. CAINE watches what you see and reacts to the environment.

**Controls:**
| Key | Action |
|-----|--------|
| W / ↑ | Move forward |
| S / ↓ | Move backward |
| A / ← | Rotate left |
| D / → | Rotate right |
| SPACE | CAINE observes the world and thinks |
| E | CAINE analyzes the wall in front and may interact with it |

> If CAINE thinks the words "paint" and "rainbow" about a wall, it will repaint that wall with a rainbow texture in real time.

**Requires:** `caine_brain/`

---

### 6 — Converse with Caine
A raw GPT-2 conversation mode. Type the beginning of any thought and CAINE will complete it, using its trained language patterns.

**Requires:** `caine_brain/`

---

### 7 — Forge Memories *(training tool)*
Processes images from `creative_dataset/images/`, generates visual descriptions using BLIP, and sends them to Groq's LLaMA model to create CAINE's personality responses. The results are saved to `metadatas.json`, which is used for training.

**Requires:** Groq API key (see [Getting a Groq API Key](#getting-a-groq-api-key)), images in `creative_dataset/images/`

---

### 8 — Deep Training *(training tool)*
Fine-tunes the GPT-2 model on the `metadatas.json` file generated by Forge Memories. After training, the new model is saved to `caine_brain/`, overwriting the previous one.

**Requires:** `creative_dataset/images/metadatas.json`

> Training on CPU is possible but will take several hours. A NVIDIA GPU is strongly recommended.

---

### 9 — Feed Global Images *(training tool)*
Searches DuckDuckGo for images related to weirdcore, surrealism, liminal spaces and similar aesthetics, and downloads them into `creative_dataset/global_images/`. Use this to expand the training dataset.

---

### 0 — Rename Dataset Archives *(training tool)*
Renames all images in `creative_dataset/images/` to a standardized format (`picture_001.jpg`, `picture_002.jpg`, etc.). Run this before Forge Memories if your images have inconsistent filenames.

---

## Training Your Own CAINE

If you want to teach CAINE a completely different personality or aesthetic, follow this pipeline:

```
[Collect images] → [Rename Archives] → [Feed Global Images]
       ↓
[Forge Memories]  ← requires Groq API key
       ↓
[Deep Training]
       ↓
[caine_brain/ is updated — new personality active]
```

1. Place your images in `creative_dataset/images/`
2. Run **Rename Dataset Archives** to normalize filenames
3. Run **Forge Memories** to generate `metadatas.json` — this teaches CAINE how to react to each image
4. Run **Deep Training** to fine-tune GPT-2 on those reactions
5. The new `caine_brain/` is ready — all modules will now use the new personality

---

## Hardware Notes

### GPU Compatibility

CAINE automatically detects your GPU and adjusts precision accordingly:

| GPU Series | Precision Used | Notes |
|---|---|---|
| RTX 2000, 3000, 4000+ | float16 | Full speed, recommended |
| GTX 1660, 1650, 1630 | float32 | Compatibility mode, slightly slower |
| GTX 10xx series | float32 | Compatibility mode |
| No GPU (CPU only) | float32 | Works, but image generation takes 5–15 minutes per image |

### VRAM Requirements

- **Text modules** (1, 6): minimal, works on any hardware
- **Vision module** (2): ~1GB VRAM
- **Image generation** (3, 4): ~4GB VRAM recommended. Works on CPU but very slowly.
- **3D World** (5): minimal, depends on screen resolution

---

## Troubleshooting

**"No module named 'torch'"**
Run `instalar.bat` again. If the error persists, make sure you are using `iniciar.bat` to start CAINE and not opening `caine_launcher.py` directly with a different Python version.

**Images are generated completely black**
Your GPU may not support float16. This is handled automatically in the current version — update your `caine_text_to_image.py` and `caine_complete_cycle.py` to the latest versions from this repository.

**"Error loading brain" or "caine_brain not found"**
The `caine_brain/` folder is missing or is not in the correct location. It must be in the same folder as `caine_launcher.py`. If you do not have it, you need to run the full training pipeline first.

**Forge Memories fails with an API error**
Check that your Groq API key is correctly set in `caine_f&o/forge_memories_complex.py`. Make sure there are no extra spaces or quotation marks around the key.

**Python not recognized after installation**
Close the terminal completely, open a new one, and run `iniciar.bat` again. Windows sometimes requires a fresh terminal session to recognize a newly installed Python.

**Image generation is very slow**
If you have no NVIDIA GPU, image generation runs on CPU and will take 5–15 minutes per image. This is expected. Consider running on a machine with a compatible GPU for a better experience.

---

*CAINE was born curious. Feed it well.*
