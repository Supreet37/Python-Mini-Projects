import json
import csv

if __name__ == '__main__':
    try:
        with open('input.json', 'r') as f:
            data = json.load(f)

        if not data:
            print("No data found.")
            exit()

        # Get all unique keys from all objects
        fieldnames = set()
        for obj in data:
            fieldnames.update(obj.keys())
        fieldnames = sorted(fieldnames)

        with open('output.csv', 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)

        print("CSV created successfully.")
    except FileNotFoundError:
        print("Error: input.json not found.")
    except json.JSONDecodeError:
        print("Error: Invalid JSON format.")
    except Exception as ex:
        print(f'Error: {str(ex)}')