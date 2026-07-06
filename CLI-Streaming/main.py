import os
from dotenv import load_dotenv
from anthropic import AsyncAnthropic
import asyncio
load_dotenv()
clinet = AsyncAnthropic()

async def message_send() -> None:
    async with clinet.messages.stream(
        max_tokens = 1024,
        messages=[
        {
            "role": "user",
            "content": "Hello, Claude",
        }
    ],
    model="claude-opus-4-8",
    )as stream:
        async for text in stream.text_stream:
            print(text, end= "", flush= True)
        print()

        
    

asyncio.run(message_send())
    

