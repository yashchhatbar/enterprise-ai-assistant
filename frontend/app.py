
import streamlit as st
import requests
import os

# Configuration
API_URL = os.getenv("API_URL", "http://localhost:8000")

st.set_page_config(page_title="Enterprise AI Assistant", page_icon="🤖", layout="wide")

st.title("🤖 Enterprise AI Knowledge Assistant")
st.markdown("---")

# Sidebar for Upload
with st.sidebar:
    st.header("📂 Document Upload")
    uploaded_file = st.file_uploader("Upload Company Documents", type=["pdf", "txt", "docx", "csv"])
    
    if st.button("Process Document"):
        if uploaded_file:
            with st.spinner("Processing document..."):
                try:
                    files = {"file": (uploaded_file.name, uploaded_file, uploaded_file.type)}
                    response = requests.post(f"{API_URL}/upload", files=files)
                    
                    if response.status_code == 200:
                        st.success(f"✅ {response.json()['message']}")
                    else:
                        st.error(f"❌ Upload failed: {response.text}")
                except Exception as e:
                    st.error(f"⚠️ Connection Error: {e}")
        else:
            st.warning("Please select a file first.")

# Main Chat Interface
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input
if prompt := st.chat_input("Ask a question about your documents..."):
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get Bot Response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        try:
            with st.spinner("Thinking..."):
                response = requests.post(f"{API_URL}/query", json={"question": prompt})
                
                if response.status_code == 200:
                    data = response.json()
                    answer = data.get("answer", "No answer found.")
                    sources = data.get("sources", [])
                    
                    full_response = answer
                    
                    if sources:
                        full_response += "\n\n**Sources:**\n" + "\n".join([f"- {s}" for s in sources])
                    
                    message_placeholder.markdown(full_response)
                else:
                    full_response = "❌ Error: Could not retrieve answer."
                    message_placeholder.markdown(full_response)
        except Exception as e:
            full_response = f"⚠️ Connection Error: {e}"
            message_placeholder.markdown(full_response)
            
    # Add assistant message to history
    st.session_state.messages.append({"role": "assistant", "content": full_response})
