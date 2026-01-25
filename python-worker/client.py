import asyncio
from pyzeebe import ZeebeClient, create_insecure_channel

async def send_hiring_request(client: ZeebeClient):
    print("Starting process instance with a Hiring request message")
    await client.publish_message(
        name="Hiring Request",  # MUST match BPMN
        correlation_key="hiringRequest",  # job_opening.job_id
        variables={
            "hiringRequest": {
                "company": {
                    "company_Id": "WBIG-001",
                    "name": "WBIG GmbH"
                },
                "job_opening": {
                    "job_id": "JOB-123",
                    "job_title": "Data Analyst",
                    "number_of_openings": 2,
                    "department": "Analytics",
                    "location": ["Berlin","Koblenz","Essen"],
                    "work_mode": "Hybrid",
                    "job_description": "Analyze KPIs and create dashboards.",
                    "requirements": {
                        "education": "BSc in Computer Science or similar",
                        "technical_skills": ["SQL", "Python", "Power BI"],
                        "soft_skills": ["Communication", "Teamwork"],
                        "experience": "2+ years",
                        "languages": {
                            "required": ["English"],
                            "preferred": ["German"]
                        },
                        "work_authorization": "EU"
                    },
                    "employment_details": {
                        "job_type": "Full-time",
                        "contract_type": "Permanent",
                        "working_hours": "40h/week",
                        "salary_range": {
                            "min": "45000",
                            "max": "65000",
                            "currency": "EUR"
                        },
                        "benefits": ["Home office budget", "Public transport ticket"]
                    },
                    "required_documents": ["CV", "Cover Letter"],
                    "contact": {
                        "recruiter_name": "Anna Schmidt",
                        "email": "anna.schmidt@wbig.example",
                        "phone": "+49 30 123456"
                    },
                    "posting_date": "2026-01-25",
                    "closing_date": "2026-02-28",
                    "starting_date": "2026-03-15",
                    "duratuion": "Permanent"
                }
            }
        }
    )


async def main():
    channel = create_insecure_channel(grpc_address="141.26.156.184:26500")
    print("Channel created")
    client = ZeebeClient(channel)
    print("Client created")

    await send_hiring_request(client)


if __name__ == "__main__":
    asyncio.run(main())
