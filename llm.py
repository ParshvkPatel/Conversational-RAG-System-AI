import os
from urllib import response
from dotenv import load_dotenv
from groq import Groq
from prompts import SYSTEM_PROMPT

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("❌ GROQ_API_KEY not found in .env file")

client = Groq(api_key=api_key)

MODEL = "llama-3.3-70b-versatile"


def generate_answer(question, context):

    prompt = f"""
{SYSTEM_PROMPT}

Context:
{context}

Question:
{question}

Answer:
"""

    try:

        response = client.chat.completions.create(
            model=MODEL,
            temperature=0,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )
        answer = response.choices[0].message.content

        return answer.strip()

    except Exception as e:

        print("\n❌ GROQ ERROR:")
        print(e)

        return "Error while generating answer."