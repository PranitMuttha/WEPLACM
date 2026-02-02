import asyncio
from datetime import datetime
from pyzeebe import ZeebeWorker, create_insecure_channel, Job, JobController
from psycopg2.extras import execute_values
from db import get_db_connection   # if you move DB logic to db.py


def register_publish_job_posting_online(worker: ZeebeWorker) -> None:
    @worker.task(task_type="publish_job_posting_online")
    async def publish_job_posting_online(hiringRequest: Job):

        variables = hiringRequest.variables

        job_request = variables.get("hiringRequest", {})
        conn = get_db_connection()


async def main():
    channel = create_insecure_channel("141.26.156.184:26500")
    worker = ZeebeWorker(channel)

    register_publish_job_posting_online(worker)

    print("Worker running...")
    await worker.work()


if __name__ == "__main__":
    asyncio.run(main())
