import streamlit as st
import urllib.request
import json

# Page configuration
st.set_page_config(page_title="Jarvis AI", page_icon="🤖", layout="centered")

st.title("🤖 Jarvis - Cloud Accelerated")
st.write("Aapka personal AI assistant ab Cloud par 24/7 super-fast chal raha hai!")

# Groq API Key from Streamlit Secrets
api_key = st.secrets["GROQ_API_KEY"]

# Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("Apna sawal yahan poochen..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate response using Groq API via standard Python (No extra package needed!)
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        try:
            url = "https://api.groq.com/openai/v1/chat/completions"
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": "qwen-2.5-32b",
                "messages": [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
                "stream": False
            }
            
            req = urllib.request.Request(
                url, 
                data=json.dumps(payload).encode('utf-8'), 
                headers=headers, 
                method='POST'
            )
            
            with urllib.request.urlopen(req) as response:
                res_data = json.loads(response.read().decode('utf-8'))
                full_response = res_data['choices'][0]['message']['content']
                message_placeholder.markdown(full_response)
                
        except Exception as e:
            full_response = f"Error: {e}"
            message_placeholder.markdown(full_response)

    st.session_state.messages.append({"role": "assistant", "content": full_response})
