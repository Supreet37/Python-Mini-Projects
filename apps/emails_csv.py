import csv
import smtplib
from email.message import EmailMessage

# HOW TO USE:
# 1. Create credentials.txt:
#      Line 1: your Gmail address
#      Line 2: your Gmail App Password (NOT your real password)
#      Go to myaccount.google.com > Security > App Passwords to generate one
# 2. Create emails.csv with one recipient email per line
# 3. Run: python emails_csv.py

def get_credentials():
    with open("credentials.txt", "r") as f:
        lines = f.read().splitlines()
    return lines[0].strip(), lines[1].strip()

def send_mail():
    email_address, email_pass = get_credentials()

    subject = "Welcome to Python"
    body = (
        "Python is an interpreted, high-level, general-purpose programming language.\n"
        "Created by Guido van Rossum and first released in 1991.\n"
        "Python's design philosophy emphasizes code readability."
    )

    with smtplib.SMTP("smtp.gmail.com", 587) as s:
        s.ehlo()
        s.starttls()
        s.login(email_address, email_pass)
        print("Logged in successfully.")

        with open("emails.csv", newline="") as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if not row:
                    continue
                recipient = row[0].strip()
                msg = EmailMessage()
                msg.set_content(body)
                msg["Subject"] = subject
                msg["From"] = email_address
                msg["To"] = recipient
                s.send_message(msg)
                print(f"Sent to: {recipient}")

    print("All emails sent!")

if __name__ == "__main__":
    send_mail()
