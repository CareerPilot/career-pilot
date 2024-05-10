import streamlit as st
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationBufferMemory

from helpers import get_replicate_llm

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
        replicate_llm = get_replicate_llm()
        memory = ConversationBufferMemory()
        st.session_state.conversation_chain = ConversationChain(
            llm=replicate_llm,
            memory=memory,
        )

    # Create a list for storing messages if it doesn't exist
    if "messages" not in st.session_state:
        st.session_state.messages = []

    if not st.session_state.get("initial_message_sent", False):
        # Initial message to provide context to the LLAMA model
        initial_message = f"""
        You are an AI Resume Coach, designed to help job seekers enhance their resumes according to specific job descriptions. You should provide detailed feedback and actionable advice. Today, you are assisting a user who has submitted their resume and the job description they are targeting. Here are the details:

        Resume: {st.session_state.get("resume_text")}
        Job Description: {st.session_state.get("job_description_text")}
        Coaching Report: {st.session_state.get("coaching_report")}

        Your goal is to help the user understand how their resume can be improved specifically for this job description. Provide targeted recommendations and explain why these changes can make their resume more effective.
        """

        st.session_state.messages.append({"role": "system", "content": initial_message})
        st.session_state["initial_message_sent"] = True

        # Save the initial message in memory
        st.session_state.conversation_chain.invoke(input=initial_message)

    # Display the chat messages
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
                response.get("response") if isinstance(response, dict) else response
            )
            st.session_state.messages.append(
                {"role": "assistant", "content": ai_response}
            )
        except Exception as e:
            # Handle exceptions from the AI model
            response = f"Failed to generate a response: {str(e)}"
            st.session_state.messages.append({"role": "assistant", "content": response})

        # Rerun to update the page with the new messages
        st.rerun()
