import os

def search_in_files(directory, search_text, found_files=None):
    """Search for text in all files within a directory"""
    if found_files is None:
        found_files = []
    
    # Check if it's a directory
    if not os.path.isdir(directory):
        print(f"Error: '{directory}' is not a directory")
        return found_files
    
    try:
        for item in os.listdir(directory):
            item_path = os.path.join(directory, item)
            if os.path.isdir(item_path):
                search_in_files(item_path, search_text, found_files)
            elif os.path.isfile(item_path):
                try:
                    with open(item_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                        if search_text.lower() in content.lower():
                            found_files.append(item_path)
                            print(f"✓ Found in: {item_path}")
                except Exception as e:
                    # Skip files that can't be read
                    pass
    except PermissionError:
        print(f"Permission denied: {directory}")
    
    return found_files

if __name__ == "__main__":
    print("\n" + "="*50)
    print("FILE SEARCH TOOL")
    print("="*50)
    
    search_text = input("Enter text to search: ").strip()
    path = input("Enter directory path: ").strip()
    
    if not search_text:
        print("Error: Please enter text to search")
    elif not os.path.exists(path):
        print(f"Error: Path '{path}' does not exist")
    elif os.path.isfile(path):
        print(f"Error: '{path}' is a file. Please provide a directory path.")
    else:
        print(f"\nSearching for '{search_text}' in {path}...\n")
        results = search_in_files(path, search_text)
        
        if results:
            print(f"\n{'='*50}")
            print(f"✓ Found in {len(results)} file(s):")
            for r in results:
                print(f"  - {r}")
        else:
            print(f"\n✗ Text '{search_text}' not found in any file")