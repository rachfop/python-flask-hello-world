from flask import Flask, escape, render_template, request
import os
import os
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
import asyncio

from run_worker import *

app = Flask(__name__)


@app.route("/")
async def get_data():
    result = await main()
    index = render_template("index.html")
    return result, index


@app.route("/", methods=["GET", "POST"])
def process_email_form():
    if request.method == "POST" and request.form.get("email"):
        email = request.form.get("email")
        action = request.form.get("action")

        if action == "subscribe":
            # Add the email address to a list of subscribers

            Email().send_email(email, "You've subscribed", "Thank you for subscribing")
            print(f"Subscribed: {email}")
            status = "subscribed"
            return render_template("welcome.html"), status
        elif action == "unsubscribe":
            # Remove the email address from the list of subscribers

            # Send an email to the user confirming their unsubscription
            Email().send_email(
                email, "You've unsubscribed", "Thank you for unsubscribing"
            )
            print(f"Unsubscribed: {email}")
            status = "unsubscribed"
            return render_template("goodbye.html"), status

    return render_template("email.html")


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


if __name__ == "__main__":
    app.run()
