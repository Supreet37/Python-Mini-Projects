import zipfile
import sys
import os
from pathlib import Path
import time

class FileCompressor:
    def __init__(self):
        self.files_compressed = 0
        self.total_original_size = 0
        self.total_compressed_size = 0
    
    def compress_file(self, file_path, output_path=None):
        """Compress a single file"""
        try:
            if output_path is None:
                output_path = file_path + '.zip'
            
            original_size = os.path.getsize(file_path)
            
            with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                zipf.write(file_path, arcname=os.path.basename(file_path))
            
            compressed_size = os.path.getsize(output_path)
            ratio = (1 - compressed_size / original_size) * 100 if original_size > 0 else 0
            
            print(f"  ✓ {os.path.basename(file_path)}")
            print(f"    Original: {original_size / 1024:.2f} KB")
            print(f"    Compressed: {compressed_size / 1024:.2f} KB")
            print(f"    Saved: {ratio:.1f}%")
            
            self.files_compressed += 1
            self.total_original_size += original_size
            self.total_compressed_size += compressed_size
            
            return True
            
        except Exception as e:
            print(f"  ✗ Error compressing {file_path}: {e}")
            return False
    
    def compress_directory(self, dir_path, output_path=None):
        """Compress an entire directory"""
        try:
            if output_path is None:
                output_path = dir_path.rstrip('/\\') + '.zip'
            
            # Get all files in directory
            all_files = []
            for root, dirs, files in os.walk(dir_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    all_files.append(file_path)
            
            if not all_files:
                print(f"  ✗ Directory is empty: {dir_path}")
                return False
            
            print(f"  Found {len(all_files)} files to compress")
            
            # Calculate original size
            for file_path in all_files:
                self.total_original_size += os.path.getsize(file_path)
            
            # Create zip file
            with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for file_path in all_files:
                    # Preserve directory structure
                    arcname = os.path.relpath(file_path, os.path.dirname(dir_path))
                    zipf.write(file_path, arcname)
                    self.files_compressed += 1
            
            self.total_compressed_size = os.path.getsize(output_path)
            ratio = (1 - self.total_compressed_size / self.total_original_size) * 100 if self.total_original_size > 0 else 0
            
            print(f"\n  📦 Compression complete!")
            print(f"    Original: {self.total_original_size / (1024*1024):.2f} MB")
            print(f"    Compressed: {self.total_compressed_size / (1024*1024):.2f} MB")
            print(f"    Saved: {ratio:.1f}%")
            
            return True
            
        except Exception as e:
            print(f"  ✗ Error compressing directory: {e}")
            return False
    
    def compress_multiple(self, paths, output_folder="compressed"):
        """Compress multiple files/folders"""
        os.makedirs(output_folder, exist_ok=True)
        
        for path in paths:
            if os.path.exists(path):
                name = os.path.basename(path)
                output_path = os.path.join(output_folder, f"{name}.zip")
                
                print(f"\n📦 Compressing: {name}")
                
                if os.path.isfile(path):
                    self.compress_file(path, output_path)
                elif os.path.isdir(path):
                    self.compress_directory(path, output_path)
            else:
                print(f"\n✗ Path not found: {path}")
        
        self.print_summary()
    
    def print_summary(self):
        """Print compression summary"""
        if self.files_compressed > 0:
            print("\n" + "="*50)
            print("COMPRESSION SUMMARY")
            print("="*50)
            print(f"Files compressed: {self.files_compressed}")
            print(f"Total original: {self.total_original_size / (1024*1024):.2f} MB")
            print(f"Total compressed: {self.total_compressed_size / (1024*1024):.2f} MB")
            print(f"Overall saved: {(1 - self.total_compressed_size / self.total_original_size) * 100:.1f}%")
            print("="*50)

def main():
    print("\n" + "="*50)
    print("FILE/FOLDER COMPRESSION TOOL")
    print("="*50)
    
    if len(sys.argv) < 2:
        print("\nUsage:")
        print("  python script.py <file_or_folder_path>")
        print("  python script.py <path1> <path2> <path3>")
        print("\nExamples:")
        print("  python script.py document.pdf")
        print("  python script.py my_folder/")
        print("  python script.py file1.txt file2.jpg folder1/")
        print("  python script.py -a  # Archive mode with timestamp")
        sys.exit(1)
    
    # Check for archive mode
    if sys.argv[1] == '-a':
        if len(sys.argv) > 2:
            paths = sys.argv[2:]
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            output_folder = f"archive_{timestamp}"
        else:
            print("Error: Please specify files/folders to archive")
            sys.exit(1)
    else:
        paths = sys.argv[1:]
        output_folder = "compressed"
    
    compressor = FileCompressor()
    compressor.compress_multiple(paths, output_folder)
    
    print(f"\n✓ Output folder: {output_folder}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠ Compression cancelled by user")
        sys.exit(0)