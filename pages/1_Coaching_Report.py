"""
This is the coaching report module.  It invokes the LLM and displays the
coaching report based on the resume and job description.
"""

import streamlit as st

from helpers import get_replicate_llm

# Display the header.
st.title("CareerPilot")
st.caption("Where your career takes flight")
st.divider()
st.markdown("### Coaching Report")
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
    llm = get_replicate_llm()

    prompt = f"""
    --- BEGIN INSTRUCTION ---
    Your task as a Resume Analysis Expert is to analyze the resume and job description provided below and generate a comprehensive coaching report tailored for a job applicant aiming to enhance their resume for a specific job opening.
    You MUST follow these steps in your evaluation, and failure to adhere to these steps will be penalized:
    1. **Alignment Score**: Provide a matching score out of 10, indicating the resume's alignment with the job requirements. Ensure the alignment score reflects the applicant’s fit.
    2. **Key Strengths**: Identify strengths of the resume that directly relate to the job description. Highlight these strengths clearly.
    3. **Improvement Areas**: Point out missing elements or areas for improvement that are crucial for securing an interview. Focus on critical improvement areas.
    4. **Recommendations**: Give specific recommendations on how to adjust the resume to better match the job description. Detail these recommendations thoroughly.
    Your task is to ensure that each section of your report is clear and thorough.
    --- END INSTRUCTION ---

    --- BEGIN EXAMPLE ---
    - Matching Score: 7/10
    - Key Strengths: Well-structured experience section, strong leadership keywords.
    - Improvement Areas: Lack of quantifiable achievements, missing skills related to project management.
    - Recommendations: Add specific outcomes to your projects to showcase impact, include a 'Skills' section with relevant project management tools.
    --- END EXAMPLE ---

    --- BEGIN INPUT DATA ---
    Resume: {st.session_state.resume_text}
    Job Description: {st.session_state.job_description_text}
    --- END INPUT DATA ---
    --- BEGIN OUTPUT PRIMER ---
    Matching Score:
    --- END OUTPUT PRIMER ---
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

    # Show the resume coach page if the user has a coaching report and wants to chat.
    if st.session_state.get("coaching_report"):
        if st.button("Chat with AI Resume Coach", type="primary"):
            st.switch_page("pages/2_AI_Resume_Coach.py")
