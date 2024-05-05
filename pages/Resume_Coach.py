import streamlit as st
from langchain_community.llms import Replicate
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationBufferMemory

st.title("CareerPilot")
st.caption("Where your career takes flight")
st.divider()
st.markdown("<h3>AI Resume Coach</h3>", unsafe_allow_html=True)
st.caption("Have a conversation to get more advice about your resume")

# Display an error if there is one
if 'error' in st.session_state:
    st.error(st.session_state['error'])
if not st.session_state.get('resume_text') or not st.session_state.get('job_description_text'):
    st.warning("Input resume and job description on the home page access the AI Resume Coach.")
    if st.button("Go Home", type="primary"):
      st.switch_page("Home.py")
else:
    # Initialize the conversation chain and memory if not already done
    if 'conversation_chain' not in st.session_state:
        replicate_llm = Replicate(
            model="meta/meta-llama-3-8b-instruct",
            model_kwargs={"temperature": 0.75, "max_length": 500, "top_p": 1}
        )
        memory = ConversationBufferMemory()
        st.session_state.conversation_chain = ConversationChain(
            llm=replicate_llm,
            memory=memory,
        )

    # Create a list for storing messages if it doesn't exist
    if 'messages' not in st.session_state:
        st.session_state.messages = []

    # Display the chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Input field for user's prompt
    prompt = st.chat_input("How can I better tailor my resume for the job?")
    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        try:
            # Generate a response from the AI
            response = st.session_state.conversation_chain.invoke(input=prompt)
            # Parse the response to display only the AI's response part
            ai_response = response.get('response') if isinstance(response, dict) else response
            st.session_state.messages.append({"role": "assistant", "content": ai_response})
        except Exception as e:
            # Handle exceptions from the AI model
            response = f"Failed to generate a response: {str(e)}"
            st.session_state.messages.append({"role": "assistant", "content": response})

        # Rerun to update the page with the new messages
        st.rerun()
