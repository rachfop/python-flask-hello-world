import asyncio
from datetime import datetime, timedelta
from temporalio import workflow, activity
from temporalio.client import Client
from temporalio.worker import Worker

from dataclasses import dataclass


@dataclass
class WorkflowParameters:
    email: str


@activity.defn
async def say_hello(name: str) -> str:
    return f"Hello, {name}!"


@workflow.defn
class SayHello:
    def __init__(self, param: WorkflowParameters):
        self._param = param

    @workflow.run
    async def run(self, param: WorkflowParameters) -> str:
        # Wait for the name to be set
        self._param = param
        return await workflow.execute_activity(
            say_hello, param.email, schedule_to_close_timeout=timedelta(seconds=5)
        )

    @workflow.query
    async def query_email(self) -> str:
        return self._param.email


async def main():
    # Create client connected to server at the given address
    client = await Client.connect("localhost:7233")

    # Run the worker
    worker = Worker(
        client, task_queue="my-task-queue", workflows=[SayHello], activities=[say_hello]
    )
    await worker.run()


if __name__ == "__main__":
    asyncio.run(main())
