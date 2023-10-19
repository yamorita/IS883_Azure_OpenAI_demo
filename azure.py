# azure.py
# Import necessary libraries
import streamlit as st
import openai
import os
# A comment
# Set up your OpenAI API key
openai.api_key = os.environ.get('OPENAI_API_KEY')
# Initialize Streamlit
# st.title("Awesome Chatbot")
# temperature = st.slider('Select the temperature', 0.0, 0.7, 1.5)
# st.write("Temperature is ", temperature)
# # Create a text input field for user queries
# user_input = st.text_input("Ask a question:")
# # Send the user's query to OpenAI GPT-3
# if user_input:
#     response = openai.Completion.create(
#     engine="text-davinci-003",
#     prompt=user_input,
#     max_tokens=50,
#     temperature=temperature
#     )
#     st.write(response['choices'][0]['text'].strip())

st.title("Negotiation Mastery")
# Set a default model
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

col1, col2, col3 = st.columns(3)
col1.metric("Cuurent baseline", "$100,000", "$10,000")
col2.metric("Minimum baseline", "$120,000")
col3.metric("Mood", "😀")

instruction = """
You are the professional negotiation coach providing a role-play for salary negotiation. 
First, set the stage by asking what type of job the client wants. Then start roll-play for salary negotiation."""

# Accept user input
if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "system", "content": instruction})
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        for response in openai.ChatCompletion.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        ):
            full_response += response.choices[0].delta.get("content", "")
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
    st.session_state.messages.append({"role": "assistant", "content": full_response})