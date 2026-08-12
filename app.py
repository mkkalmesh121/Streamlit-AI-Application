import os
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

# Load API key from .env
load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)

# Page settings
st.set_page_config(page_title="AI Text Generator", page_icon="🤖", layout="centered")

st.title("🤖 MY CHATBOT FOR PROJECT")
st.write("Enter any prompt and get an AI-generated response.")

# User input
prompt = st.text_area("Enter your prompt:", height=150)

temperature = st.slider("Creativity", 0.0, 1.0, 0.7)
max_tokens = st.slider("Maximum Tokens", 50, 1000, 300)

if st.button("Generate Response"):

    if not prompt.strip():
        st.warning("Please enter a prompt.")
    else:
        with st.spinner("Generating response..."):

            try:
                response = client.chat.completions.create(
                    model="openai/gpt-4o-mini",
                    messages=[
                        {
                            "role": "system",
                            "content": (
                                "You are a knowledgeable AI assistant. "
                                "Answer every question accurately, clearly, "
                                "and in a well-formatted way. "
                                "If the user asks for code, provide complete working code. "
                                "If the user asks for an explanation, explain in simple language."
                            )
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    temperature=temperature,
                    max_tokens=max_tokens
                )

                answer = response.choices[0].message.content

                st.success("Response Generated Successfully!")
                st.subheader("AI Response")
                st.write(answer)

                st.download_button(
                    label="📥 Download Response",
                    data=answer,
                    file_name="AI_Response.txt",
                    mime="text/plain"
                )

            except Exception as e:
                st.error(f"Error: {e}")