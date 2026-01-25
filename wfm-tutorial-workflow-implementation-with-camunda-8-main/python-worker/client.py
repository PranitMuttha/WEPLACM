import asyncio

from pyzeebe import ZeebeClient, create_insecure_channel


# See https://github.com/camunda-community-hub/pyzeebe for details
async def start_work_process(client: ZeebeClient):
    print("Starting process instance demo 1 by process id")
    await client.run_process("Process_0yqlmow", variables={"work": 9})


async def send_message_work_process(client: ZeebeClient):  
    print("Starting process instance with a message")  
    await client.publish_message(name="StartWorkProcess",  
                                 correlation_key="Hello",  
                                 variables={"work": 2 })
                                 
async def main():
    channel = create_insecure_channel(grpc_address="141.26.15x.xx:26500")
    print("Channel created")
    client = ZeebeClient(channel)
    print("Client created")

    # await start_work_process(client)
    # await send_message_work_process(client)


if __name__ == "__main__":
    asyncio.run(main())