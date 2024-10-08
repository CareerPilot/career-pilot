"""
This is the primary module for the CareerPilot application.  Streamlit runs
this to display the Website.
"""

from io import StringIO

import streamlit as st

from helpers import doc_to_text, pdf_to_text

# Main title
st.title("CareerPilot")
st.caption("Where your career takes flight")
st.divider()

# Container for resume input
with st.container():
    # Allow the user to either paste the text of their resume or upload it in
    # an acceptable format.
    st.markdown("### 1. Paste or Upload Resume")
    resume_text = st.text_area(
        "Resume:", value=str(st.session_state.get("resume_text", ""))
    )
    uploaded_file = st.file_uploader(
        "Upload DOCX, PDF, or TXT", type=["docx", "pdf", "txt"]
    )

    # Display a message if both resume text and uploaded file are provided
    resume_info_placeholder = st.empty()
    if resume_text.strip() and uploaded_file:
        resume_info_placeholder.info("Using the uploaded file.")

st.divider()

# Container for job description input
with st.container():
    st.markdown("### 2. Paste Job Description")
    job_description_text = st.text_area(
        "Job Description:", value=str(st.session_state.get("job_description_text", ""))
    )

# Check if both resume and job description are provided
if (resume_text.strip() or uploaded_file) and job_description_text.strip():
    if st.button("View Coaching Report", type="primary"):
        # Put the resume text into session state when the button is clicked
        if uploaded_file is not None:
            try:
                name = uploaded_file.name.lower()
                if name.endswith("pdf"):
                    st.session_state.resume_text = pdf_to_text(uploaded_file)
                elif name.endswith("docx"):
                    st.session_state.resume_text = doc_to_text(uploaded_file)
                else:
                    st.session_state.resume_text = StringIO(
                        uploaded_file.getvalue().decode("utf-8")
                    ).read()
            except Exception as e:
                st.error("Error parsing the uploaded file. Try a different format.")
                st.stop()
        elif resume_text.strip():
            st.session_state.resume_text = resume_text.strip()

        # Reset the coaching report and display the coaching report page to
        # generate a new one.
        st.session_state.job_description_text = job_description_text.strip()
        if st.session_state.get("coaching_report"):
            st.session_state.coaching_report = ""
        st.switch_page("pages/1_Coaching_Report.py")
else:
    # Tell the user to provide the required text.
    if not (resume_text.strip() or uploaded_file) and not job_description_text.strip():
        st.warning("Input resume and job description.")
    elif not (resume_text.strip() or uploaded_file):
        st.warning("Input resume.")
    elif not job_description_text.strip():
        st.warning("Input job description.")

# Show a button to clear session state and start over.
if st.session_state.get("resume_text") or st.session_state.get("job_description"):
    if st.button("Clear All"):
        st.session_state.clear()
        st.rerun()
