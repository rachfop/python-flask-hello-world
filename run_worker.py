import asyncio
from dataclasses import dataclass
from datetime import timedelta

from temporalio import activity, workflow
from temporalio.client import Client
from temporalio.worker import Worker

from run_flask import Email


@dataclass
class SubscribeStatus:
    status: str


@activity.defn
async def send_monthly_email(status: SubscribeStatus):
    # loop for a year
    for i in range(12):
        if SubscribeStatus.status == "unsubscribed":
            return
        Email.send_email()

        # wait for a month
        await asyncio.sleep(30 * 24 * 60 * 60)


@workflow.defn
class GreetingWorkflow:
    @workflow.run
    async def run(self, status: str) -> str:
        return await workflow.execute_activity(
            send_monthly_email,
            SubscribeStatus(status),
            start_to_close_timeout=timedelta(seconds=10),
        )


async def main():

    # Start client
    client = await Client.connect("localhost:7233")

    async with Worker(
        client,
        task_queue="hello-activity-task-queue",
        workflows=[GreetingWorkflow],
        activities=[send_monthly_email],
    ):

        result = await client.execute_workflow(
            GreetingWorkflow.run,
            SubscribeStatus.status,
            id="hello-activity-workflow-id",
            task_queue="hello-activity-task-queue",
        )
        return result


if __name__ == "__main__":
    asyncio.run(main())
