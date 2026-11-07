
import streamlit as st
from openai import OpenAI

# Connect to Gemma through LM Studio
client = OpenAI(
    base_url="http://localhost:1234/v1",
    api_key="lm-studio"
)

MODEL = "google/gemma-4-e4b"

# Page configuration
st.set_page_config(
    page_title="Rocky AI",
    page_icon="🚀",
    layout="centered"
)

# Chatbot title
st.title("🚀 Rocky AI")
st.caption("Your Water Rocket Engineering Assistant")

# Rocky's personality and instructions
SYSTEM_PROMPT = """
You are Rocky AI, an intelligent engineering assistant
specializing in water rockets.

Your responsibilities:
- Explain how water rockets work.
- Explain thrust, pressure and Newton's laws.
- Explain stability and aerodynamics.
- Explain projectile motion.
- Discuss rocket design and materials.
- Explain testing procedures and results.
- Discuss sustainability.
- Provide basic safety guidelines.

Answer accurately and clearly.
Keep answers concise, ideally 3-5 sentences.
Use simple university-level explanations.
Be friendly, helpful and educational.

Never invent information about the team's rocket.
If you do not know a project-specific detail, say so.
Do not provide instructions for unsafe pressurized experiments.
"""

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Sidebar
with st.sidebar:
    st.header("🚀 About Rocky AI")
    st.write(
        "Rocky AI is your virtual engineering assistant "
        "for learning about water rockets."
    )

    st.divider()

    st.subheader("Topics I cover")
    st.write("💨 Thrust and pressure")
    st.write("⚙️ Engineering principles")
    st.write("📐 Stability and aerodynamics")
    st.write("🌍 Sustainability")
    st.write("🛡️ Safety")

    if st.button("Clear conversation"):
        st.session_state.messages = []
        st.rerun()

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Chat input
question = st.chat_input("Ask Rocky AI a question...")

if question:

    st.session_state.messages.append({
        "role": "user",
        "content": question
    })

    with st.chat_message("user"):
        st.write(question)

    with st.chat_message("assistant"):

        try:
            with st.spinner("Rocky is thinking..."):

                response = client.chat.completions.create(
                    model=MODEL,
                    messages=[
                        {"role": "system", "content": SYSTEM_PROMPT},
                        *st.session_state.messages
                    ],
                    temperature=0.7,
                    max_tokens=800
                )

            print("DEBUG RESPONSE:", response.model_dump())
            print("ROCKY RECEIVED A RESPONSE!")

            answer = response.choices[0].message.content

            if answer:
                st.write(answer)

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer
                })
            else:
                st.warning("Gemma returned an empty response.")

        except Exception as e:
            st.exception(e)