import os
import argparse
import pyautogui
import time

parser = argparse.ArgumentParser()
parser.add_argument("-p", "--path", help="absolute path to store screenshot.", default="./images")
parser.add_argument("-t", "--type", help="h (hour), m (minute), or s (second)", default='h')
parser.add_argument("-f", "--frequency", help="screenshots per unit (e.g., 2 per hour)", default=1, type=int)
args = parser.parse_args()

if args.type == 'h':
    sec = 3600 / args.frequency
elif args.type == 'm':
    sec = 60 / args.frequency
elif args.type == 's':
    sec = 1 / args.frequency
else:
    sec = 1

if sec < 0.5:
    sec = 0.5

if not os.path.isdir(args.path):
    os.makedirs(args.path, exist_ok=True)

try:
    while True:
        t = time.localtime()
        current_time = time.strftime("%Y_%m_%d_%H_%M_%S", t)
        file = current_time + ".png"
        image = pyautogui.screenshot(os.path.join(args.path, file))
        print(f"{file} saved successfully.")
        time.sleep(sec)
except KeyboardInterrupt:
    print("Script stopped by user.")