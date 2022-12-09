from flask import Flask, escape, render_template, request
import os
import os
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
import asyncio
from temporalio.client import Client
from run_worker import GreetingWorkflow

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
async def process_email_form():
    client = await Client.connect("127.0.0.1:7233")

    if request.method == "POST" and request.form.get("email"):
        email = request.form.get("email")
        action = request.form.get("action")

        if action == "subscribe":

            Email().send_email(email, "You've subscribed", "Thank you for subscribing")
            status = "subscribe"
            results = await client.execute_workflow(
                GreetingWorkflow.run,
                status,
                id="hello-activity-workflow-id",
                task_queue="hello-activity-task-queue",
            )

            return render_template("welcome.html"), results, status
        elif action == "unsubscribe":
            Email().send_email(
                email, "You've unsubscribed", "Thank you for unsubscribing"
            )
            status = "unsubscribe"
            results = await client.execute_workflow(
                GreetingWorkflow.run,
                status,
                id="hello-activity-workflow-id",
                task_queue="hello-activity-task-queue",
            )
            return render_template("goodbye.html"), results, status

    return render_template("email.html")


class Email:
    def __init__(self):
        self.email_address = os.environ.get("EMAIL_ADDRESS")
        self.email_password = os.environ.get("EMAIL_PASSWORD")

    def send_email(self, to, subject, message):
        try:
            if self.email_address is None or self.email_password is None:
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
