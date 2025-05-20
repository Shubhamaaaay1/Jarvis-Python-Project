from openai import OpenAI

# Replace with your actual API key securely

API_KEY = "<Enter API key>"

client = OpenAI(api_key=API_KEY)

completion = client.chat.completions.create(
model="gpt-3.5-turbo",
messages=[
{"role": "system", "content": "You are a virtual assistant named Jarvis skilled in general tasks like Alexa and Google Cloud."},
{"role": "user", "content": "what is coding"}
]
)

print(completion.choices[0].message.content)

