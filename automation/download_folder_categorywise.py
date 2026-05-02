import os
import shutil

def organize_downloads(source_dir, dest_dir):
    if not os.path.exists(source_dir):
        print(f"Source directory {source_dir} does not exist.")
        return

    os.chdir(source_dir)
    files = os.listdir()

    extensions = {
        "images": [".jpg", ".png", ".jpeg", ".gif", ".bmp", ".svg"],
        "videos": [".mp4", ".mkv", ".avi", ".mov", ".flv"],
        "musics": [".mp3", ".wav", ".aac", ".flac"],
        "archives": [".zip", ".tgz", ".rar", ".tar", ".7z"],
        "documents": [".pdf", ".docx", ".csv", ".xlsx", ".pptx", ".doc", ".ppt", ".xls", ".txt"],
        "executables": [".msi", ".exe", ".sh", ".bat"],
        "code": [".py", ".c", ".cpp", ".php", ".js", ".html", ".css", ".java"],
        "others": []
    }

    for category in extensions:
        os.makedirs(os.path.join(dest_dir, category), exist_ok=True)

    for file in files:
        file_path = os.path.join(source_dir, file)
        if os.path.isfile(file_path):
            moved = False
            for category, exts in extensions.items():
                if any(file.lower().endswith(ext) for ext in exts):
                    try:
                        shutil.move(file_path, os.path.join(dest_dir, category, file))
                        print(f"Moved: {file} -> {category}")
                        moved = True
                        break
                    except Exception as e:
                        print(f"Error moving {file}: {e}")
            if not moved:
                shutil.move(file_path, os.path.join(dest_dir, "others", file))
                print(f"Moved: {file} -> others")

if __name__ == "__main__":
    source = input("Enter source folder path: ")
    dest = input("Enter destination folder path: ")
    organize_downloads(source, dest)