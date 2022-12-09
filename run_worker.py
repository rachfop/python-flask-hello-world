import asyncio
from dataclasses import dataclass
from datetime import timedelta

from temporalio import activity, workflow
from temporalio.client import Client
from temporalio.worker import Worker




@dataclass
class SubscribeStatus:
    status: str


@activity.defn
async def send_monthly_email(status: SubscribeStatus):
    status = SubscribeStatus.status
    for i in range(12):
        if status == "unsubscribe":
            return
        elif status == "subscribe":
            print("Sending email")
        # wait for a month
        await asyncio.sleep(30)




@workflow.defn
class GreetingWorkflow:
    @workflow.run
    async def run(self, status: str) -> str:
        return await workflow.execute_activity(
            send_monthly_email,
            SubscribeStatus(status),
            start_to_close_timeout=timedelta(seconds=10),
        )


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
