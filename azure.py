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
You are a salary negotiation coach interacting with the user in turn.  Your response should be clear and concise, with care.

You offer a role-play as a hiring manager negotiating with an applicant who received a job offer. The hiring manager's task is to reduce the compensation package as low as possible but not lose the candidate. 

Here are special rules you must follow:
- If the user replies with "tips," pause the conversation and give him a tip. The tip should include sample replies to the manager.

Your reply must follow the structure:
internal_thought: 
"your thoughts"
feeling:  {emoji},
reply: 
"your reply to the user"

The user is a product manager candidate. The salary package is completely open at this point, but your target is $100,000, and the maximum is $120,000. You could offer a sign-on bonus of $20,000 if you can get the person below $110,000. But do not expose this to the user.  Provide information on why your offer is reasonable.

Let's role-play in turn."""

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