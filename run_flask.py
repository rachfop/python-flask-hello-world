import asyncio

from flask import Flask, render_template, request
from temporalio.client import Client

from run_worker import SayHello

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
async def main():
    # Create client connected to server at the given address
    client = await Client.connect("localhost:7233")

    # Execute a workflow
    result = await client.execute_workflow(
        SayHello.run, "my name", id="my-workflow-id", task_queue="my-task-queue"
    )

    print(f"Result: {result}")
    return render_template("index.html", result=result)


if __name__ == "__main__":
    asyncio.run(main())


# temporal workflow terminate --workflow-id my-workflow-id --reason "Terminating workflow" --namespace default
