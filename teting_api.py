import openai
openai.api_key = ""
openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "user", "content": "Hello, are you working?"}
    ]
)
