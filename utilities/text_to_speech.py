from gtts import gTTS
import os
import sys

def text_to_speech(input_file, output_file="voice.mp3", lang='en'):
    if not os.path.exists(input_file):
        print(f"Error: {input_file} not found.")
        return False
    
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            text = f.read()
        
        if not text.strip():
            print("Error: File is empty.")
            return False
        
        speech = gTTS(text=text, lang=lang, slow=False)
        speech.save(output_file)
        print(f"Saved to {output_file}")
        
        # Try to play the file
        if sys.platform == "darwin":  # macOS
            os.system(f"afplay {output_file}")
        elif sys.platform == "win32":  # Windows
            os.system(f"start {output_file}")
        else:  # Linux
            os.system(f"mpg123 {output_file}")
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    file_name = input("Enter text file path: ")
    text_to_speech(file_name)