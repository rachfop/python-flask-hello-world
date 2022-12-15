import asyncio

from flask import Flask, render_template, request
from temporalio.client import Client

from run_worker import SayHello, WorkflowParameters


app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
async def main():
    if request.form.get("action") == "subscribe":
        user = request.form["email"]
        client = await Client.connect("localhost:7233")
        param = WorkflowParameters(email=user)
        # Execute a workflow
        result = await client.start_workflow(
            SayHello.run, param, id=user, task_queue="my-task-queue"
        )
        return render_template("welcome.html", result=result, user=user)

    return render_template("email.html")


# query the workflow
@app.route("/query", methods=["GET", "POST"])
async def query():

    result = await query(SayHello.query_email)
    return render_template("welcome.html", result=result)


if __name__ == "__main__":
    asyncio.run(main())


# temporal workflow terminate --workflow-id my-workflow-id --reason "Terminating workflow" --namespace default
