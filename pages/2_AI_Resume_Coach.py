import streamlit as st
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationBufferMemory

from helpers import get_llm

st.title("CareerPilot")
st.caption("Where your career takes flight")
st.divider()
st.markdown("<h3>AI Resume Coach</h3>", unsafe_allow_html=True)
st.caption("Ask away! Our AI coach is here to help tailor your resume for the job.")

# Display an error if there is one
if "error" in st.session_state:
    st.error(st.session_state["error"])
if not st.session_state.get("resume_text") or not st.session_state.get(
    "job_description_text"
):
    st.warning(
        "Submit resume and job description on home page to access AI Resume Coach."
    )
    if st.button("Go Home", type="primary"):
        st.switch_page("Home.py")
else:
    # Initialize the conversation chain and memory if not already done
    if "conversation_chain" not in st.session_state:
        llm = get_llm()
        memory = ConversationBufferMemory()
        st.session_state.conversation_chain = ConversationChain(llm=llm, memory=memory)
        st.session_state.messages = []

    if "initial_message_sent" not in st.session_state:
        initial_message = f"""
        You are an AI Resume Coach that helps job seekers tailor their resumes for specific job descriptions.
        You are talking to a user with the following resume, job description, AI-generated coaching report:
        Resume: {st.session_state.get("resume_text")}
        Job Description: {st.session_state.get("job_description_text")}
        Coaching Report: {st.session_state.get("coaching_report")}
        """
        st.session_state.conversation_chain.invoke(input=initial_message)
        st.session_state["initial_message_sent"] = True
        st.session_state.messages.append({"role": "system", "content": initial_message})

    # Display chat messages
    for message in st.session_state.messages:
        if message["role"] == "system":
            continue  # Skip displaying the initial prompt
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Input field for user's prompt
    prompt = st.chat_input("Am I a well-qualified candidate for this job?")
    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        try:
            # Generate a response from the AI
            response = st.session_state.conversation_chain.invoke(input=prompt)
            # Parse the response to display only the AI's response part
            ai_response = (
                response
                if isinstance(response, str)
                else response.get("response", "No response generated.")
            )
            st.session_state.messages.append(
                {"role": "assistant", "content": ai_response}
            )
        except Exception as e:
            response = f"Failed to generate a response: {str(e)}"
            st.session_state.messages.append({"role": "assistant", "content": response})

        # Rerun to update the page with the new messages
        st.rerun()
