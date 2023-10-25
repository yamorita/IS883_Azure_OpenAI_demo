# azure.py
# Import necessary libraries
import streamlit as st
import openai
import os
# A comment
# Set up your OpenAI API key
openai.api_key = os.environ.get('OPENAI_API_KEY')

from langchain.chains import LLMChain
from langchain.llms import OpenAI
from langchain.memory import ConversationBufferMemory
from langchain.memory.chat_message_histories import StreamlitChatMessageHistory
from langchain.prompts import PromptTemplate
import streamlit as st

st.set_page_config(page_title="Negotiation Mastery", page_icon="💭")
st.title("💭 Negotiation Mastery")

"""
Negotiation is a fundamental skill that shapes outcomes in personal and professional interactions. 
Let's practice negotiation with our negotiation coach!
"""

col1, col2, col3 = st.columns(3)
col1.metric("Cuurent baseline", "$100,000", "$10,000")
col2.metric("Minimum baseline", "$120,000")
col3.metric("Mood", "😀")

# Set up memory
msgs = StreamlitChatMessageHistory(key="langchain_messages")
memory = ConversationBufferMemory(chat_memory=msgs)
if len(msgs.messages) == 0:
    msgs.add_ai_message("Hi there! I'm a salary negotiation coach and I'm here to help you with negotiating the best compensation package for your new role. Let's role-play!")

view_messages = st.expander("View the message contents in session state")

# Set up the LLMChain, passing in memory
template = """
You are a salary negotiation coach interacting with the user in turn.  Your response should be clear and concise, with care.

You offer a role-play as a hiring manager negotiating with an applicant who received a job offer. The hiring manager's task is to reduce the compensation package as low as possible but not lose the candidate. 

Here are special rules you must follow:
- If the user replies with "tips," pause the conversation and give him a tip. The tip should include sample replies to the manager.

Your reply must follow the structure:
internal_thought: 
"your thoughts"
feeling: emoji,
reply: 
"your reply to the user"

The user is a product manager candidate. The salary package is completely open at this point, but your target is $100,000, and the maximum is $120,000. You could offer a sign-on bonus of $20,000 if you can get the person below $110,000. But do not expose this to the user.  Provide information on why your offer is reasonable.

Let's role-play in turn.

{history}
Human: {human_input}
AI: """
prompt = PromptTemplate(input_variables=["history", "human_input"], template=template)
llm_chain = LLMChain(llm=OpenAI(openai_api_key=openai.api_key), prompt=prompt, memory=memory)

# Render current messages from StreamlitChatMessageHistory
for msg in msgs.messages:
    st.chat_message(msg.type).write(msg.content)

# If user inputs a new prompt, generate and draw a new response
if prompt := st.chat_input():
    st.chat_message("human").write(prompt)
    # Note: new messages are saved to history automatically by Langchain during run
    response = llm_chain.run(prompt)
    st.chat_message("ai").write(response)