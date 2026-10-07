import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

MODEL = "qwen/qwen3.8-27b"  # check console.groq.com/docs/models for current models

# The messages list is the chatbot's memory
messages = [
    {"role": "system", "content": "You are a helpful and friendly assistant."}
]

print("Chatbot ready! Type 'quit' to exit.\n")

while True:
    user_input = input("You: ").strip()
    if user_input.lower() in ("quit", "exit"):
        print("Goodbye!")
        break
    if not user_input:
        continue

    messages.append({"role": "user", "content": user_input})

    try:
        stream = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            temperature=0.7,
            max_tokens=1024,
            stream=True,  # shows the answer word by word
        )

        print("Bot: ", end="", flush=True)
        reply = ""
        for chunk in stream:
            text = chunk.choices[0].delta.content or ""
            print(text, end="", flush=True)
            reply += text
        print("\n")

        # Save the bot's reply so it remembers the conversation
        messages.append({"role": "assistant", "content": reply})

    except Exception as e:
        print(f"\nError: {e}\n")
        messages.pop()  # remove the failed user message