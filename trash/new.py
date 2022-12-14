import os
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv

_ = load_dotenv()

# https://mljar.com/blog/python-send-email/


def subscribe():
    email = input("Enter your email: ")
    with open("email.txt", "a") as f:
        # strip the newline character
        f.write(email.strip() + "\n")
        count = 0
        while count < 3:
            Email().send_email(
                email, "You have subscribed", f"Thank you for subscribing {count}"
            )
            count += 1
        print(f"Subscribed: {email}")


def unsubscribe():
    email = input("Enter your email: ")
    with open("email.txt", "r") as f:
        lines = f.readlines()
    with open("email.txt", "w") as f:
        for line in lines:
            if line.strip("\n") != email:
                f.write(line)

        Email().send_email(email, "You've subscribed", "Thank you for subscribing")
        print(f"Unsubscribed: {email}")


class Email:
    def __init__(self):
        self.email_address = os.environ.get("EMAIL_ADDRESS")
        self.email_password = os.environ.get("EMAIL_PASSWORD")

    def send_email(self, to, subject, message):
        try:
            if self.email_address is None or self.email_password is None:
                # no email address or password
                # something is not configured properly
                print("Did you set email address and password correctly?")
                return False

            # create email
            msg = EmailMessage()
            msg["Subject"] = subject
            msg["From"] = self.email_address
            msg["To"] = to
            msg.set_content(message)

            # send email
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
                smtp.login(self.email_address, self.email_password)
                smtp.send_message(msg)
            return True
        except Exception as e:
            print("Problem during send email")
            print(str(e))
        return False


def main():
    print("1. Subscribe")
    print("2. Unsubscribe")
    choice = input("Enter your choice: ")
    if choice == "1":
        subscribe()

    elif choice == "2":
        unsubscribe()
    else:
        print("Invalid choice")


if __name__ == "__main__":
    main()
