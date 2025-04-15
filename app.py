import streamlit as st
from openai import OpenAI
import os

st.title("Saffi's Assistant")

# Initialize OpenAI client
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("What would you like to know?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Generate AI response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        try:
            response = client.chat.completions.create(
                model="gpt-4.1-nano-2025-04-14",
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
                stream=True
            )
            
            # Stream the response
            for chunk in response:
                if chunk.choices[0].delta.content is not None:
                    full_response += chunk.choices[0].delta.content
                    message_placeholder.markdown(full_response + "▌")
            
            message_placeholder.markdown(full_response)
            
        except Exception as e:
            st.error(f"Error: {str(e)}")
            
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": full_response})

# Add a simplified sidebar with New Chat button
with st.sidebar:
    if st.button("New Chat", use_container_width=True, type="primary"):
        st.session_state.messages = []
        st.rerun()
    
    st.divider()
    st.write("Model: gpt-4.1-nano-2025-04-14")
