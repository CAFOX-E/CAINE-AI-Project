import os
import requests
import time
import random
from ddgs import DDGS

def download_stealth_ddg_dataset():
    print("=" * 60)
    print("CONNECTING CAINE TO DUCKDUCKGO (STEALTH MODE)")
    print("Searching for images with surgical patience to avoid blockages...")
    print("=" * 60)

    search_term = ["weirdcore"]
    quantity_per_term = 3
    
    folder_path = "../creative_dataset/global_images"
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    viewed_urls = set()
    total_downloaded = 0

    with DDGS() as ddgs:
        for term in search_term:
            print(f"\n[-] Starting stealth search for: '{term}'...")
            
            attempts = 0
            search_success = False
            results = []

            # 1. THE BYPASS TRICK: THE RESILIENCE LOOP
            # If we get a 403 block, the script does not die. It sleeps and tries again.
            while attempts < 3 and not search_success:
                try:
                    print(f"  [>] Scouring the web (Attempt {attempts + 1}/3)...")
                    results = list(ddgs.images(term, max_results=quantity_per_term))
                    search_success = True # If it went past the line above without error, it worked!
                except Exception as e:
                    # Calculation of "Exponential Backoff": wait 20s, then 40s, then 60s
                    waiting_time = 20 * (attempts + 1)
                    print(f"  [!] Radar detected the script! (Ratelimit)")
                    print(f"  [zZz] Sleeping for {waiting_time} seconds to confuse the server...")
                    time.sleep(waiting_time)
                    attempts += 1

            if not search_success or not results:
                print("  [!] Very hostile server now. Moving on to the next concept.")
                continue

            print(f"  [+] List obtained successfully. Starting slow download...")

            for idx, item in enumerate(results):
                image_link = item.get("image")
                
                if not image_link or image_link in viewed_urls:
                    continue

                try:
                    # 2. THE DISGUISE: Pretending to be the Chrome browser on a Windows
                    headers = {
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
                    }
                    
                    img_data = requests.get(image_link, headers=headers, timeout=5).content
                    
                    archive_name = f"ddg_{term.replace(' ', '_')}_{idx}.jpg"
                    archive_path = os.path.join(folder_path, archive_name)
                    
                    with open(archive_path, 'wb') as archive:
                        archive.write(img_data)
                    
                    viewed_urls.add(image_link)
                    total_downloaded += 1
                    print(f"    + Captured: {archive_name}")
                    
                except Exception:
                    # If an individual website fails, silently ignore it
                    pass
                
                # 3. THE HUMAN FACTOR: Random pause between each download (0.5 to 2 seconds)
                time.sleep(random.uniform(0.5, 2.0))

            # 4. COOLING THE ENGINES: Long pause before changing the search term
            print("  [-] Cooling down the engines before looking up the next word...")
            time.sleep(15)

    print("=" * 60)
    print(f"STEALTH OPERATION COMPLETED. {total_downloaded} images recovered.")
    print("=" * 60)

if __name__ == "__main__":
    download_stealth_ddg_dataset()
# , "dreamcore", "surrealism classic", "liminal space", "scary suburb", "Eastern Europe Aesthetic", "frutiger aero", "divine machinery aesthetic", "circus aesthetic", "liminal void core"