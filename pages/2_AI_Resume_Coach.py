"""
This is the resume coach module.  It accepts user input and invokes the LLM to
allow the user to improve their resume by chatting with the LLM.  The coaching
report is included in the chat state.
"""

import streamlit as st
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationBufferMemory

from helpers import get_replicate_llm

# Display the header.
st.title("CareerPilot")
st.caption("Where your career takes flight")
st.divider()
st.markdown("### AI Resume Coach")
st.caption("Ask away! Our AI coach is here to help tailor your resume for the job.")

# Display an error if there is one
if "error" in st.session_state:
    st.error(st.session_state["error"])
if not st.session_state.get("resume_text") or not st.session_state.get(
    "job_description_text"
):
    # If the user is here without a resume and job description, direct them to
    # the home page.
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
        --- BEGIN INSTRUCTION ---
        As an AI Resume Coach, your role is to assist job applicants in refining their resumes for specific job descriptions.
        You MUST provide detailed, actionable feedback based on the provided input data. Your task is to ensure your advice is specific and actionable.
        Failure to provide targeted and accurate advice as required will be penalized. Remember to answer any questions given in a natural, human-like manner. Your role requires you to be precise and helpful.
        --- END INSTRUCTION ---

        --- BEGIN EXAMPLE INTERACTION ---
        Applicant Question: "How can I make my resume stand out for a project management role?"
        AI Response: "To enhance your resume for a project management role, focus on adding quantifiable achievements in your past projects. For instance, mention the budget you managed or the percentage completion of the projects under your leadership. Ensure your response is detailed and practical."
        --- END EXAMPLE INTERACTION ---

        --- BEGIN INPUT DATA ---
        Resume: {st.session_state.get("resume_text")}
        Job Description: {st.session_state.get("job_description_text")}
        Coaching Report: {st.session_state.get("coaching_report")}
        --- END INPUT DATA ---
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
