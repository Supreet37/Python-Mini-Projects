import sys
import os
import math

def split_file_by_lines(filename, lines_per_file=1000):
    """
    Split a text file into multiple chunks by number of lines
    """
    try:
        # Create output directory
        output_dir = "split_files"
        os.makedirs(output_dir, exist_ok=True)
        
        # Get base name without extension
        base_name = os.path.splitext(os.path.basename(filename))[0]
        
        # Read and split file
        with open(filename, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
        
        total_lines = len(lines)
        num_files = math.ceil(total_lines / lines_per_file)
        
        print(f"Total lines: {total_lines}")
        print(f"Splitting into {num_files} files ({lines_per_file} lines each)")
        
        for i in range(num_files):
            start = i * lines_per_file
            end = start + lines_per_file
            chunk = lines[start:end]
            
            output_file = os.path.join(output_dir, f"{base_name}_part_{i+1:03d}.txt")
            with open(output_file, 'w', encoding='utf-8') as f:
                f.writelines(chunk)
            
            print(f"Created: {output_file} ({len(chunk)} lines)")
        
        print(f"\n✓ Successfully split file into {num_files} chunks")
        return True
        
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found")
        return False
    except Exception as e:
        print(f"Error: {e}")
        return False

def split_file_by_size(filename, chunk_size_mb=1):
    """
    Split a file into chunks of specific size (in MB)
    """
    try:
        output_dir = "split_files_by_size"
        os.makedirs(output_dir, exist_ok=True)
        
        base_name = os.path.splitext(os.path.basename(filename))[0]
        chunk_size = chunk_size_mb * 1024 * 1024  # Convert to bytes
        
        with open(filename, 'rb') as f:
            chunk_num = 1
            while True:
                chunk = f.read(chunk_size)
                if not chunk:
                    break
                
                output_file = os.path.join(output_dir, f"{base_name}_chunk_{chunk_num:03d}.bin")
                with open(output_file, 'wb') as out_f:
                    out_f.write(chunk)
                
                print(f"Created: {output_file} ({len(chunk)} bytes)")
                chunk_num += 1
        
        print(f"\n✓ Successfully split file into {chunk_num-1} chunks")
        return True
        
    except Exception as e:
        print(f"Error: {e}")
        return False

def main():
    print("\n" + "="*50)
    print("FILE SPLITTER TOOL")
    print("="*50)
    
    if len(sys.argv) < 2:
        filename = input("Enter file path to split: ").strip()
    else:
        filename = sys.argv[1]
    
    if not os.path.exists(filename):
        print(f"Error: File '{filename}' not found")
        return
    
    print("\nSplit by:")
    print("1. Number of lines (text files)")
    print("2. File size (any file)")
    
    choice = input("\nChoose option (1 or 2): ").strip()
    
    if choice == '1':
        lines = input("Lines per file (default 1000): ").strip()
        lines = int(lines) if lines else 1000
        split_file_by_lines(filename, lines)
    
    elif choice == '2':
        size = input("Size per file in MB (default 1): ").strip()
        size = float(size) if size else 1.0
        split_file_by_size(filename, size)
    
    else:
        print("Invalid choice")

if __name__ == "__main__":
    main()