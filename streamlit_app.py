import os
import streamlit as st
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationBufferMemory
from langchain_community.llms import Replicate
from langchain.globals import set_verbose

set_verbose(True)

# Initialize API token and model
REPLICATE_API_TOKEN = st.secrets["REPLICATE_API_TOKEN"]
os.environ["REPLICATE_API_TOKEN"] = REPLICATE_API_TOKEN

# Setup model and conversation chain
replicate_llm = Replicate(
    model="meta/meta-llama-3-8b-instruct",
    model_kwargs={"temperature": 0.75, "max_length": 500, "top_p": 1},
)

# Initialize memory only once and store in Streamlit's session state
if 'memory' not in st.session_state:
    st.session_state.memory = ConversationBufferMemory()

conversation_chain = ConversationChain(
    llm=replicate_llm,
    memory=st.session_state.memory,  # Use the memory from session state
)

st.title("Llama Model Conversation")

prompt = st.text_area("Enter your prompt:")
if st.button("Generate"):
    if prompt:
        try:
            response = conversation_chain.invoke(input=prompt)
            st.write(response)
        except Exception as e:
            st.error(f"Failed to generate a response: {str(e)}")
    else:
        st.error("Please enter a prompt to continue the conversation.")
