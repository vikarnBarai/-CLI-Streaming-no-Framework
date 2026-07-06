import os
from dotenv import load_dotenv
from ChatBot.API import ChatBot_API
import asyncio
load_dotenv()
messages = []
api = ChatBot_API()
  
    
def main():
    while True:
        user_input = input(">") 
        api.add_user_message(message = messages, text = user_input)
        final_msg = asyncio.run(api.chatbot_msg(messages))
        api.add_assistant_message(messages,final_msg)

main()
