from groq import Groq
import streamlit as st
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GROQ_KEY")

if not api_key:
    st.error("GROQ_KEY not found in .env file")
    st.stop()

def groq_client(query):
  client = Groq(api_key=api_key)

  #st.title("What is Mergers and Acquisitions?")

  completion = client.chat.completions.create(
      model="openai/gpt-oss-120b",  # safer default model
      messages=[
          {"role": "user",
          "content": query}
      ],
      temperature=0.7,
  )

  #st.subheader("The Answer is:")
  return completion.choices[0].message.content

a=groq_client("Complete the sentence: The fox jumps over the...")
print(a)