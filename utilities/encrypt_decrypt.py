import sys
import os

try:
    from Crypto.Cipher import AES
    from Crypto import Random
    from binascii import b2a_hex, a2b_hex
except ImportError:
    print("Error: pycryptodome library required. Install with: pip install pycryptodome")
    sys.exit(1)

def generate_key():
    """Generate a random 16-byte key"""
    return Random.new().read(16)

def encrypt_text(plain_text, key=None):
    if key is None:
        key = generate_key()
    
    if isinstance(key, str):
        key = key.encode()
    
    # Ensure key length is valid (16, 24, or 32 bytes)
    if len(key) < 16:
        key = key.ljust(16, b'0')
    elif len(key) > 32:
        key = key[:32]
    
    iv = Random.new().read(AES.block_size)
    cipher = AES.new(key, AES.MODE_CFB, iv)
    
    if isinstance(plain_text, str):
        plain_text = plain_text.encode()
    
    ciphertext = iv + cipher.encrypt(plain_text)
    return ciphertext, key

def decrypt_text(ciphertext, key):
    if isinstance(key, str):
        key = key.encode()
    
    iv = ciphertext[:16]
    cipher = AES.new(key, AES.MODE_CFB, iv)
    decrypted = cipher.decrypt(ciphertext[16:])
    return decrypted

def main():
    print("\n" + "="*40)
    print("AES ENCRYPTION/DECRYPTION TOOL")
    print("="*40)
    
    while True:
        print("\n1. Encrypt text")
        print("2. Decrypt file")
        print("3. Exit")
        choice = input("Choose: ").strip()
        
        if choice == '1':
            text = input("Enter text to encrypt: ")
            if text:
                ciphertext, key = encrypt_text(text)
                print(f"\n✓ Encrypted successfully!")
                print(f"Key (save this): {b2a_hex(key).decode()}")
                print(f"Encrypted data: {b2a_hex(ciphertext).decode()[:50]}...")
                
                # Save to file
                with open("encrypted.bin", "wb") as f:
                    f.write(ciphertext)
                with open("secret.key", "wb") as f:
                    f.write(key)
                print("\nSaved to: encrypted.bin and secret.key")
        
        elif choice == '2':
            key_hex = input("Enter key (hex): ").strip()
            try:
                key = a2b_hex(key_hex)
                if os.path.exists("encrypted.bin"):
                    with open("encrypted.bin", "rb") as f:
                        ciphertext = f.read()
                    decrypted = decrypt_text(ciphertext, key)
                    print(f"\n✓ Decrypted text: {decrypted.decode()}")
                else:
                    print("Error: encrypted.bin not found")
            except Exception as e:
                print(f"Error: {e}")
        
        elif choice == '3':
            print("Goodbye!")
            break

if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Command line mode
        text = sys.argv[1]
        ciphertext, key = encrypt_text(text)
        print(f"Key: {b2a_hex(key).decode()}")
        print(f"Encrypted: {b2a_hex(ciphertext).decode()}")
    else:
        main()