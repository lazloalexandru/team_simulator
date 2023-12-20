import openai
import os
import sys
import tiktoken
import json


def token_count(some_text):
    encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
    return len(encoding.encode(some_text))


def gpt(prompt_json):
    api_key = os.environ.get('GPT_API_KEY')
    if api_key is None:
        print("API key not found. Please set the 'GPT_API_KEY' environment variable.")
        sys.exit()

    openai.api_key = api_key

    system_role = prompt_json["system"]
    user_content = prompt_json["user"]

    messages = [
        {"role": "system", "content": f"{system_role}"},
        {"role": "user", "content": f"{user_content}"}
    ]

    input_message = json.dumps(messages)
    print("Input token count:", token_count(input_message))
    print("Waiting for GPT ...")

    answer = openai.ChatCompletion.create(
        model="gpt-4-1106-preview",
        response_format={"type": "json_object"},
        temperature=0.5,
        messages=messages
    )

    output_message = answer.choices[0].message['content']
    print("Output token count:", token_count(output_message))

    return output_message


if __name__ == "__main__":
    import json

    text = '{"system": "You are an assistant", "user": "Give me result for 4+1 in JSON format"}'
    prompt = json.loads(text)
    response = gpt(prompt)
    print(response)
