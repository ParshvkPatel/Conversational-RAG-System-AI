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

{context}

Current Question:
{question}

Answer:
"""

    response = client.chat.completions.create(

        model=MODEL,

        temperature=0,

        max_tokens=700,

        messages=[

            {
                "role": "user",
                "content": prompt
            }

        ]

    )

    return response.choices[0].message.content.strip()