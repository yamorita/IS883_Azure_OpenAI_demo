# azure.py
# Import necessary libraries
import streamlit as st
import openai
import os
# A comment
# Set up your OpenAI API key
openai.api_key = os.environ.get('OPENAI_API_KEY')
# Initialize Streamlit
st.title("Awesome Chatbot")
temperature = st.slider('Select the temperature', 0.0, 0.7, 1.5)
st.write("Temperature is ", temperature)
# Create a text input field for user queries
user_input = st.text_input("Ask a question:")
# Send the user's query to OpenAI GPT-3
if user_input:
    response = openai.Completion.create(
    engine="text-davinci-003",
    prompt=user_input,
    max_tokens=50,
    temperature=temperature
    )
    st.write(response['choices'][0]['text'].strip())
