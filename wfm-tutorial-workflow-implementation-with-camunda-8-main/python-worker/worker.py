import asyncio
import random
from pyzeebe import ZeebeWorker, create_insecure_channel, Job, JobController


async def main():
    channel = create_insecure_channel(grpc_address="141.26.15x.xxx:26500")
    print("Channel created")
    worker = ZeebeWorker(channel)
    print("Worker created")

    async def overload_exception_handler(
        exception: Exception, job: Job, job_controller: JobController
    ) -> None:
        print("Too much work, can not handle this overload :(")
        await job_controller.set_error_status(message="Too much work!!!")

    @worker.task(
        task_type="MoodCalculator", exception_handler=overload_exception_handler
    )
    async def my_mood_calculator(job: Job, work: int):
        print("myServiceTask")
        print(
            f"Received job from process {job.bpmn_process_id} with instance id = {job.process_instance_key}"
        )
        print(f"Current variables: {job.variables}")
        if work >= 12:
            raise Exception

        print("Start clculation of mood")
        my_mood = random.choice(["Happy", "Good", "Bad", "Angry"])
        print(f"My mood is {my_mood}")
        return {"mood": my_mood}

    await worker.work()


if __name__ == "__main__":
    asyncio.run(main())
