import random
import string
import argparse

def generate_password(length=16, use_digits=True, use_punctuation=True):
    chars = string.ascii_letters
    if use_digits:
        chars += string.digits
    if use_punctuation:
        chars += string.punctuation
    
    password = ''.join(random.choice(chars) for _ in range(length))
    return password

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate a random password")
    parser.add_argument("-l", "--length", type=int, default=16, help="Password length")
    parser.add_argument("--no-digits", action="store_true", help="Exclude digits")
    parser.add_argument("--no-punctuation", action="store_true", help="Exclude punctuation")
    args = parser.parse_args()
    
    password = generate_password(
        length=args.length,
        use_digits=not args.no_digits,
        use_punctuation=not args.no_punctuation
    )
    print(password)