def decimal_to_binary():
    while True:
        try:
            dec = input("Enter decimal number (or 'q' to quit): ")
            if dec.lower() == 'q':
                return
            # Allow only integers
            if '.' in dec:
                print("Please enter an integer (no decimal points)")
                continue
            dec = int(dec)
            print(f"Binary: {bin(dec)[2:]}\n")
            return
        except ValueError:
            print("Please enter a valid integer.\n")

def binary_to_decimal():
    while True:
        binary = input("Enter binary number (0s and 1s only, or 'q' to quit): ")
        if binary.lower() == 'q':
            return
        if not all(c in '01' for c in binary):
            print("Invalid binary number. Use only 0 and 1.\n")
            continue
        try:
            print(f"Decimal: {int(binary, 2)}\n")
            return
        except ValueError:
            print("Invalid binary number.\n")

def main():
    while True:
        print("\n" + "="*30)
        print("BINARY/DECIMAL CONVERTER")
        print("="*30)
        print("1. Decimal to Binary")
        print("2. Binary to Decimal")
        print("3. Exit")
        
        choice = input("Choose option (1-3): ").strip()
        
        if choice == '1':
            decimal_to_binary()
        elif choice == '2':
            binary_to_decimal()
        elif choice == '3':
            print("Goodbye!")
            break
        else:
            print("Invalid option. Please choose 1, 2, or 3.\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nGoodbye!")