import streamlit as st
from helpers import pdf_to_text

# Main title
st.title("CareerPilot")
st.caption("Where your career takes flight")

# Create two containers for the text areas and file uploader
with st.container():
    st.markdown("<h3>1. Paste or Upload Resume</h3>", unsafe_allow_html=True)
    resume_text = st.text_area("Paste resume:", height=100)
    pdf_file = st.file_uploader("Upload resume as PDF:", type="pdf")  # No width specified

st.markdown("---")  # Adds a horizontal line for better separation

with st.container():
    st.markdown("<h3>2. Paste Job Description</h3>", unsafe_allow_html=True)
    job_description_text = st.text_area("Paste job description:", height=100)

# Button to generate the coaching report
if st.button("Generate Coaching Report"):
    # Set session state only when the button is clicked
    resume_text_provided = bool(resume_text.strip())
    st.session_state.resume_text = None if not resume_text_provided else resume_text

    if pdf_file is not None:
        st.session_state.resume_text = pdf_to_text(pdf_file)

    job_description_provided = bool(job_description_text.strip())
    st.session_state.job_description_text = None if not job_description_provided else job_description_text

    # Check if both resume and job description are provided
    if st.session_state.get("resume_text") and st.session_state.get("job_description_text"):
        # Here you would include the logic to process the resume and job description
        # and generate the coaching report.
        # For example, you could display the result like this:
        # report = generate_coaching_report(resume_text, job_description_text)
        # st.write(report)
        st.success("The coaching report has been generated! (Placeholder)")
    else:
        st.error("Please provide both a resume and job description to generate the coaching report.")
