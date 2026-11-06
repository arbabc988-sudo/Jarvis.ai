import streamlit as st
from groq import Groq

# Page configuration
st.set_page_config(page_title="Jarvis AI", page_icon="🤖", layout="centered")

st.title("🤖 Jarvis - Cloud Accelerated")
st.write("Aapka personal AI assistant ab Cloud par 24/7 super-fast chal raha hai!")

# Groq API Client initialize karein (Streamlit Secrets se key uthayega)
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("Apna sawal yahan poochen..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate assistant response using Groq Cloud API
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""

        try:
            completion = client.chat.completions.create(
                model="qwen-2.5-32b",  # Fast and smart open-source model
                messages=st.session_state.messages,
                stream=True
            )

            for chunk in completion:
                content = chunk.choices[0].delta.content or ""
                full_response += content
                message_placeholder.markdown(full_response + "▌")

            message_placeholder.markdown(full_response)
        except Exception as e:
            full_response = f"Error: {e}"
            message_placeholder.markdown(full_response)

    st.session_state.messages.append({"role": "assistant", "content": full_response})
