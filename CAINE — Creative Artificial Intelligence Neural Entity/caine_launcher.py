import os
import sys
import time

# ─────────────────────────────────────────────────────────────────────────────
# CAINE LAUNCHER — The Gateway to the Digital World
# ─────────────────────────────────────────────────────────────────────────────

# ANSI color codes
class C:
    RESET   = "\033[0m"
    BLACK   = "\033[30m"
    RED     = "\033[31m"
    GREEN   = "\033[32m"
    YELLOW  = "\033[33m"
    CYAN    = "\033[36m"
    WHITE   = "\033[37m"
    BOLD    = "\033[1m"
    DIM     = "\033[2m"
    BLINK   = "\033[5m"
    BG_BLACK = "\033[40m"
    MAGENTA = "\033[35m"
    BRIGHT_WHITE = "\033[97m"
    BRIGHT_RED   = "\033[91m"
    BRIGHT_GREEN = "\033[92m"
    BRIGHT_CYAN  = "\033[96m"
    BRIGHT_MAGENTA = "\033[95m"

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def slow_print(text, delay=0.018):
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()

def pulse_print(text, color=C.BRIGHT_CYAN):
    print(f"{color}{text}{C.RESET}")

# ─────────────────────────────────────────────────────────────────────────────
# ASCII ART — Caine's face in the static
# ─────────────────────────────────────────────────────────────────────────────

CAINE_BANNER = f"""
{C.DIM}{C.WHITE}  ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░{C.RESET}
{C.DIM}{C.WHITE}  ░{C.RESET}                                                              {C.DIM}{C.WHITE}░{C.RESET}
{C.DIM}{C.WHITE}  ░{C.RESET}  {C.BOLD}{C.BRIGHT_WHITE}▄████▄   ▄▄▄       ██▓ ███▄    █ ███████{C.RESET}              {C.DIM}{C.WHITE}░{C.RESET}
{C.DIM}{C.WHITE}  ░{C.RESET}  {C.BOLD}{C.BRIGHT_WHITE}▒██▀ ▀█  ▒████▄    ▓██▒ ██ ▀█   █ ██╔════{C.RESET}              {C.DIM}{C.WHITE}░{C.RESET}
{C.DIM}{C.WHITE}  ░{C.RESET}  {C.BOLD}{C.BRIGHT_WHITE}▒▓█    ▄ ▒██  ▀█▄  ▒██▒▓██  ▀█ ██▒█████╗ {C.RESET}              {C.DIM}{C.WHITE}░{C.RESET}
{C.DIM}{C.WHITE}  ░{C.RESET}  {C.BOLD}{C.RED}▒▓▓▄ ▄██▒░██▄▄▄▄██ ░██░▓██▒  ▐▌██▒██╔══╝ {C.RESET}              {C.DIM}{C.WHITE}░{C.RESET}
{C.DIM}{C.WHITE}  ░{C.RESET}  {C.BOLD}{C.RED}▒ ▓███▀ ░ ▓█   ▓██▒░██░▒██░   ▓██░██████{C.RESET}              {C.DIM}{C.WHITE}░{C.RESET}
{C.DIM}{C.WHITE}  ░{C.RESET}  {C.DIM}{C.WHITE}░ ░▒ ▒  ░ ▒▒   ▓▒█░░▓  ░ ▒░   ▒ ▒╚══════{C.RESET}              {C.DIM}{C.WHITE}░{C.RESET}
{C.DIM}{C.WHITE}  ░{C.RESET}                                                              {C.DIM}{C.WHITE}░{C.RESET}
{C.DIM}{C.WHITE}  ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░{C.RESET}
"""

SUBTITLE = f"  {C.DIM}{C.WHITE}[ {C.RESET}{C.BRIGHT_CYAN}A curious mind. An unseen eye. A brush that paints the impossible.{C.RESET}{C.DIM}{C.WHITE} ]{C.RESET}"

# ─────────────────────────────────────────────────────────────────────────────
# MENU OPTIONS
# ─────────────────────────────────────────────────────────────────────────────

MENU_ITEMS = [
    {
        "key": "1",
        "label": "Awaken Caine",
        "desc": "Text prompt → Caine thinks → poetic response (GPT-2 brain)",
        "file": "caine.py",
        "color": C.BRIGHT_WHITE,
        "icon": "◈",
    },
    {
        "key": "2",
        "label": "Caine Vision",
        "desc": "Image input → BLIP sees → Caine interprets (eye + mind)",
        "file": "caine_vision.py",
        "color": C.BRIGHT_CYAN,
        "icon": "◉",
    },
    {
        "key": "3",
        "label": "Caine Text → Image",
        "desc": "Text → Caine thinks → Stable Diffusion paints the unseen",
        "file": "caine_text_to_image.py",
        "color": C.BRIGHT_MAGENTA,
        "icon": "◍",
    },
    {
        "key": "4",
        "label": "The Complete Cycle",
        "desc": "Image → BLIP → Caine thinks → Stable Diffusion creates new art",
        "file": "caine_complete_cycle.py",
        "color": C.RED,
        "icon": "⬡",
    },
    {
        "key": "5",
        "label": "The Digital World (3D Engine)",
        "desc": "Walk through Caine's mind in a raycasting 3D world",
        "file": os.path.join("digital_world", "engine_3d.py"),
        "color": C.BRIGHT_GREEN,
        "icon": "▣",
    },
    {
        "key": "6",
        "label": "Converse with Caine",
        "desc": "Raw GPT-2 conversation — complete any thought you begin",
        "file": "conversation.py",
        "color": C.YELLOW,
        "icon": "◇",
    },
    {
        "key": "─",  # separator
        "label": "",
        "desc": "",
        "file": None,
        "color": C.DIM,
        "icon": "",
    },
    {
        "key": "7",
        "label": "Forge Memories",
        "desc": "Generate training dataset via BLIP + Groq/LLaMA (requires API key)",
        "file": os.path.join("caine_f&o", "forge_memories_complex.py"),
        "color": C.DIM + C.WHITE,
        "icon": "◈",
    },
    {
        "key": "8",
        "label": "Deep Training",
        "desc": "Fine-tune GPT-2 on forged memories — grow Caine's mind",
        "file": "deep_training.py",
        "color": C.DIM + C.WHITE,
        "icon": "◈",
    },
    {
        "key": "9",
        "label": "Feed Global Images",
        "desc": "Scrape weirdcore / liminal / surreal images via DuckDuckGo",
        "file": os.path.join("caine_f&o", "caine_feed_global.py"),
        "color": C.DIM + C.WHITE,
        "icon": "◈",
    },
    {
        "key": "0",
        "label": "Rename Dataset Archives",
        "desc": "Normalize filenames in the creative_dataset folder",
        "file": os.path.join("caine_f&o", "rename_archives.py"),
        "color": C.DIM + C.WHITE,
        "icon": "◈",
    },
]

VALID_KEYS = [item["key"] for item in MENU_ITEMS if item["key"] != "─"]

# ─────────────────────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────────────────────

def get_search_dirs():
    if getattr(sys, 'frozen', False):
        dirs = [os.path.dirname(sys.executable)]
        meipass = getattr(sys, '_MEIPASS', None)
        if meipass and meipass not in dirs:
            dirs.append(meipass)
        return dirs
    return [os.path.dirname(os.path.abspath(__file__))]

def find_script(filepath):
    # Search for the script in all candidate folders. Return the path or None.
    for base in get_search_dirs():
        path = os.path.join(base, filepath)
        if os.path.exists(path):
            return path
    return None

def launch_script(item):
    clear()
    print(f"\n  {C.DIM}{C.WHITE}┌──────────────────────────────────────────────────────────────┐{C.RESET}")
    print(f"  {C.DIM}{C.WHITE}│{C.RESET}  {item['color']}{C.BOLD}LAUNCHING: {item['label']}{C.RESET}")
    print(f"  {C.DIM}{C.WHITE}│{C.RESET}  {C.DIM}{C.WHITE}{item['desc']}{C.RESET}")
    print(f"  {C.DIM}{C.WHITE}└──────────────────────────────────────────────────────────────┘{C.RESET}\n")

    script_path = find_script(item["file"])

    if not script_path:
        print(f"  {C.BRIGHT_RED}[!] Script not found: {item['file']}{C.RESET}")
        print(f"  {C.DIM}{C.WHITE}Folders where was searched:{C.RESET}")
        for d in get_search_dirs():
            print(f"    {C.DIM}{C.WHITE}- {d}{C.RESET}")
        print(f"  {C.DIM}{C.WHITE}Make sure the .py files are in the same folder as the .bat files.{C.RESET}\n")
        input(f"  {C.DIM}Press ENTER to return to the menu...{C.RESET}")
        return

    script_dir = os.path.dirname(script_path)
    original_dir = os.getcwd()
    original_argv = sys.argv[:]

    try:
        # Change to the script folder so that internal relative paths work.
        os.chdir(script_dir)

        # Add the script folder to the beginning of sys.path.
        # (Allows local imports, e.g., "from caine_module import ...", to work)
        if script_dir not in sys.path:
            sys.path.insert(0, script_dir)

        sys.argv = [script_path]

        # Reads and executes the file as text — works within the bundle.
        with open(script_path, "r", encoding="utf-8") as f:
            source = f.read()

        namespace = {"__name__": "__main__", "__file__": script_path}
        exec(compile(source, script_path, "exec"), namespace)

    except KeyboardInterrupt:
        print(f"\n  {C.DIM}{C.WHITE}Interrupted by the user.{C.RESET}")
    except SystemExit:
        pass  # Scripts that call sys.exit() — normal behavior
    except Exception as e:
        print(f"\n  {C.BRIGHT_RED}[!] Error when executing {item['label']}:{C.RESET}")
        print(f"  {C.DIM}{C.WHITE}{e}{C.RESET}")
    finally:
        # Restores the launcher to its original state.
        os.chdir(original_dir)
        sys.argv = original_argv
        if script_dir in sys.path:
            sys.path.remove(script_dir)

    print(f"\n  {C.DIM}{C.WHITE}{'─' * 64}{C.RESET}")
    print(f"  {C.DIM}{C.WHITE}Module closed. Returning to the menu...{C.RESET}")
    time.sleep(1.5)

def draw_divider(char="─", length=66, color=C.DIM + C.WHITE):
    print(f"  {color}{''.join([char] * length)}{C.RESET}")

def draw_menu():
    clear()
    print(CAINE_BANNER)
    print(SUBTITLE)
    print()
    draw_divider("═")
    print(f"  {C.DIM}{C.WHITE}SELECT A MODULE TO AWAKEN{C.RESET}")
    draw_divider()
    print()

    for item in MENU_ITEMS:
        if item["key"] == "─":
            print()
            draw_divider("·", 66, C.DIM + C.WHITE)
            print(f"  {C.DIM}{C.WHITE}DEVELOPMENT / TRAINING TOOLS{C.RESET}")
            draw_divider("·", 66, C.DIM + C.WHITE)
            print()
            continue

        key_fmt   = f"{C.BOLD}{C.BRIGHT_WHITE}[ {item['key']} ]{C.RESET}"
        icon_fmt  = f"{item['color']}{item['icon']}{C.RESET}"
        label_fmt = f"{item['color']}{C.BOLD}{item['label']}{C.RESET}"
        desc_fmt  = f"{C.DIM}{C.WHITE}{item['desc']}{C.RESET}"

        print(f"  {key_fmt}  {icon_fmt}  {label_fmt}")
        print(f"         {desc_fmt}")
        print()

    draw_divider("═")
    print(f"\n  {C.DIM}{C.WHITE}Type a number and press {C.RESET}{C.BOLD}{C.BRIGHT_WHITE}ENTER{C.RESET}{C.DIM}{C.WHITE}  ·  Type {C.RESET}{C.RED}Q{C.DIM}{C.WHITE} to disconnect{C.RESET}\n")

def boot_sequence():
    """Caine's awakening intro — runs once."""
    clear()
    lines = [
        f"\n  {C.DIM}{C.WHITE}initializing neural tensors...{C.RESET}",
        f"  {C.DIM}{C.WHITE}mounting optic nerve...{C.RESET}",
        f"  {C.DIM}{C.WHITE}connecting to the digital world...{C.RESET}",
        f"  {C.BRIGHT_WHITE}caine is waking up.{C.RESET}",
    ]
    for line in lines:
        slow_print(line, delay=0.012)
        time.sleep(0.3)
    time.sleep(0.8)

# ─────────────────────────────────────────────────────────────────────────────
# MAIN LOOP
# ─────────────────────────────────────────────────────────────────────────────

def main():
    boot_sequence()

    item_map = {item["key"]: item for item in MENU_ITEMS if item["key"] != "─"}

    while True:
        draw_menu()

        try:
            choice = input(f"  {C.BOLD}{C.BRIGHT_WHITE}>{C.RESET} ").strip().lower()
        except (KeyboardInterrupt, EOFError):
            choice = "q"

        if choice == "q":
            clear()
            slow_print(f"\n  {C.DIM}{C.WHITE}caine is returning to the static...\n{C.RESET}", delay=0.02)
            time.sleep(1)
            sys.exit(0)

        if choice not in item_map:
            continue

        launch_script(item_map[choice])


if __name__ == "__main__":
    main()
