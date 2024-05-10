import streamlit as st

from helpers import get_llama_llm, get_replicate_llm, is_local

st.title("CareerPilot")
st.caption("Where your career takes flight")
st.divider()
st.markdown("<h3>Coaching Report</h3>", unsafe_allow_html=True)
st.caption("Get insights on how well your resume matches the job description.")

# Display an error if there is one
if "error" in st.session_state:
    st.error(st.session_state["error"])
elif not st.session_state.get("resume_text") or not st.session_state.get(
    "job_description_text"
):
    st.warning(
        "Submit resume and job description on home page to access Coaching Report."
    )
    if st.button("Go Home", type="primary"):
        st.switch_page("Home.py")
else:
    # Initialize the LLM
    llm = get_replicate_llm() if is_local() else get_llama_llm()

    prompt = f"""
        Please analyze the following resume and job description to generate a comprehensive coaching report. Assess how well the resume aligns with the job requirements specified in the job description. Provide a detailed analysis including:
        1. A matching score out of 10, indicating overall alignment.
        2. Key strengths of the resume in relation to the job description.
        3. Areas for improvement or elements that are missing in the resume.
        4. Specific recommendations on how to tailor the resume to better match the job description.

        Resume: {st.session_state.resume_text}
        Job Description: {st.session_state.job_description_text}
        """

    if st.session_state.get("coaching_report", ""):
        st.write(st.session_state.coaching_report)
    else:
        placeholder = st.empty()  # Create a placeholder for the report
        placeholder.text(
            "Generating your coaching report... Please wait."
        )  # Display temporary text
        try:
            response = llm.invoke(prompt)  # Directly call the model with the prompt
            st.session_state.coaching_report = (
                response  # Save the response in session state
            )
            placeholder.empty()  # Clear the placeholder
            st.write(response)  # Display the report
        except Exception as e:
            st.error(f"Failed to generate a coaching report: {str(e)}")

    if st.session_state.get("coaching_report"):
        if st.button("Chat with AI Resume Coach", type="primary"):
            st.switch_page("pages/2_AI_Resume_Coach.py")
