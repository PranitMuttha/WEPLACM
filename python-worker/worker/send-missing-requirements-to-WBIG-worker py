import asyncio
from pyzeebe import ZeebeWorker, create_insecure_channel, Job, JobController

def register_prepare_missing_requirements(worker: ZeebeWorker) -> None:
    @worker.task(task_type="prepare-missing-requirements")
    async def prepare_missing_requirements(job: Job):
        print("Worker: prepare-missing-requirements")
        variables = job.variables

        hiring_request = variables.get("hiringRequest", {})
        job_opening = hiring_request.get("job_opening", {})
        requirements = job_opening.get("requirements", {})
        employment = job_opening.get("employment_details", {})

        missing = []

        if not job_opening.get("job_title"):
            missing.append("Job title")

        if not job_opening.get("job_description"):
            missing.append("Job description")

        if not requirements.get("education"):
            missing.append("Education")

        if not requirements.get("technical_skills"):
            missing.append("Technical skills")

        if not employment.get("salary_range", {}).get("min"):
            missing.append("Minimum salary")

        if not employment.get("salary_range", {}).get("max"):
            missing.append("Maximum salary")

        email_body = (
            "Hello WBIG Team,\n\n"
            "The following required information is missing in your hiring request:\n\n"
            + "\n".join(f"- {field}" for field in missing) +
            "\n\nPlease update and resubmit the request.\n\n"
            "Best regards,\nRecruitment Team"
        )

        return {
            "missingRequirements": {"count": len(missing), "fields": missing},
            "notification": {"subject": "Missing information in hiring request", "body": email_body},
        }


async def main():
    channel = create_insecure_channel(grpc_address="141.26.156.184:26500")
    print("Channel created")
    worker = ZeebeWorker(channel)
    print("Worker created")
    
    register_prepare_missing_requirements(worker)

    await worker.work()

if __name__ == "__main__":
    asyncio.run(main())
