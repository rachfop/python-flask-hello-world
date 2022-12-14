from flask import Flask, escape, render_template, request
import os
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
import asyncio
from temporalio.client import Client
from run_worker import GreetingWorkflow

app = Flask(__name__)


#@app.route("/", methods=["GET", "POST"])
async def process_email_form():
    client = await Client.connect("127.0.0.1:7233")
    if request.method == "POST" and request.form.get("email"):


        

            results = await client.start_workflow(
                GreetingWorkflow.run,
                "subscribe",
                id="hello-activity-workflow-id",
                task_queue="hello-activity-task-queue",
            )

    return results





if __name__ == "__main__":
    app.run()
