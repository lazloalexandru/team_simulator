import openai
import os

api_key = os.environ.get('GPT_API_KEY')

if api_key is None:
    print("API key not found. Please set the 'MY_API_KEY' environment variable.")
else:
    print("API key:", api_key)

    openai.api_key = api_key

    system_role = "You are a pyton assistant!"
    user_content = "What is print(4+1) function print out? Give me JSON answer"

    response = openai.ChatCompletion.create(
        model="gpt-4-1106-preview",
        response_format={"type": "json_object"},
        temperature=0.5,
        messages=[
            {"role": "system", "content": f"{system_role}"},
            {"role": "user", "content": f"{user_content}"}
        ]
    )

    print(response.choices[0].message['content'])
