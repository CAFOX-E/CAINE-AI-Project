import os

def organize_dataset():
    # Path to the folder where Caine's images are saved
    images_folder = "../creative_dataset/images" # Change to "images" if your folder is in English
    
    if not os.path.exists(images_folder):
        print(f"Folder not found: {images_folder}")
        return
        
    print("-" * 50)
    print("STARTING THE STANDARDIZATION OF CAINE MEMORIES")
    print("-" * 50)

    # List all files in the folder
    archives = os.listdir(images_folder)
    
    # Filters to ensure we only touch images (ignores hidden Windows files)
    images = [f for f in archives if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    
    # Sort the list to maintain consistency
    images.sort() 

    counter = 1
    for old_name in images:
        # Separates the file name from the extension (ex: .jpg)
        extension = os.path.splitext(old_name)[1]
        
        # Creates the new name formatted with 3 leading zeros (ex: picture_001.jpg)
        new_name = f"picture_{counter:03d}{extension}"
        
        old_path = os.path.join(images_folder, old_name)
        new_path = os.path.join(images_folder, new_name)
        
        # If the file already has the right name, it ignores
        if old_name == new_name:
            counter += 1
            continue
            
        try:
            os.rename(old_path, new_path)
            print(f"[+] Renamed: {old_name[:15]}... -> {new_name}")
            counter += 1
        except Exception as e:
            print(f"[-] Error when renaming {old_name}: {e}")

    print("-" * 50)
    print(f"Operation completed! {counter - 1} files are organized.")

if __name__ == "__main__":
    organize_dataset()