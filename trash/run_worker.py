import asyncio
from dataclasses import dataclass
from datetime import timedelta

from temporalio import activity, workflow
from temporalio.client import Client
from temporalio.worker import Worker

from flask import Flask, escape, render_template, request
import os
import os
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
import asyncio
from temporalio.client import Client


@dataclass
class SubscribeStatus:
    status: str
    email: str

@activity.defn
async def send_monthly_email(input: SubscribeStatus):
    email = request.form.get("email")
    
    action = request.form.get("action")
    if action == "subscribe":
        print("Sending email to " + input.email)
    # Email().send_email(input.email, "You've subscribed", "Thank you for subscribing")
    return render_template("welcome.html")




@workflow.defn
class GreetingWorkflow:
    @workflow.run
    async def run(self, status: str) -> str:
        return await workflow.start_activity(
            send_monthly_email,
            SubscribeStatus(status),
            start_to_close_timeout=timedelta(seconds=10),
        )

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


async def start_worker():
    # Start worker
    client = await Client.connect("localhost:7233")

    async with Worker(
        client,
        task_queue="hello-activity-task-queue",
        workflows=[GreetingWorkflow],
        activities=[send_monthly_email],
    ) as worker:
        await worker.run()

async def start_workflow():
    client = await Client.connect("localhost:7233")
    results = await client.start_workflow(
        GreetingWorkflow.run,
        "subscribe",
        id="hello-activity-workflow-id",
        task_queue="hello-activity-task-queue",
    )
    print("Started workflow:", results)

async def main():
    await asyncio.gather(
        start_worker(),
        start_workflow(),
    )

if __name__ == "__main__":
    load_dotenv()
    asyncio.run(main())