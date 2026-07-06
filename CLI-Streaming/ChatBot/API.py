import anthropic
from anthropic.types import ToolParam
from anthropic import beta_tool
from dotenv import load_dotenv
from pathlib import Path
dotenv_path = Path(__file__).resolve().parent.parent / '.env'
load_dotenv(dotenv_path=dotenv_path)

client = anthropic.AsyncAnthropic()
get_employee_salary_schema = ToolParam(
        {
  "name": "get_employee_salary",
  "description": "Returns the salary of an employee given their name.",
  "input_schema": {
    "type": "object",
    "properties": {
      "name": {
        "type": "string",
        "description": "The employee's full first name, e.g. 'Meghan'"
      }
    },
    "required": ["name"]
  }
}
    )

web_search_schema = ToolParam({
    "type": "web_search_20250305",
    "name": "web_search"
})

class ChatBot_API :

    async def chatbot_msg(self, messages) -> str:
        try:
            async with client.messages.stream(
                max_tokens = 1024,
                messages=messages,
                tools= [get_employee_salary_schema, web_search_schema],
            model="claude-opus-4-8",
            )as stream:
                async for text in stream.text_stream:
                    print(text, end= "", flush= True)
                print()
                
                final_message = await stream.get_final_message()
                full_text = final_message.content[0].text
                for content in final_message.content:
                    if content.type == "tool_use":
                        if content.name == 'get_employee_salary':
                            tool_result = self.get_employee_salary(content.input['name'])
                            print(f"salary is {tool_result}")

                return full_text

        except anthropic.APIConnectionError as e:
            print(e.cause)
        except anthropic.RateLimitError as e:
            print("Reach reate Limit")
            print(e.cause)
        except anthropic.APIStatusError as e:
            print(e.status_code)
            print(e.response)

    def add_user_message(self, message, text):
        user_message = {
                    "role": "user",
                    "content": text,
                }
        message.append(user_message)
    def add_assistant_message(self, message, text):
        user_message = {
                    "role": "assistant",
                    "content": text,
                }
        message.append(user_message)  
    @beta_tool
    def get_employee_salary(name: str)  -> str:
        salary = {
            "Meghan" : "$20k",
            "George" : "$30K" 
        }
        return salary.get(name)


   