import streamlit as st

# Main title
st.title("CareerPilot")
st.caption("Where your career takes flight")

# Create two columns for the text areas
col1, col2 = st.columns(2)

with col1:
    st.header("Paste Your Resume")
    resume_text = st.text_area("Copy and paste your resume here", height=400)

with col2:
    st.header("Paste Job Description")
    job_description_text = st.text_area("Copy and paste the job description here", height=400)

# Button to generate the coaching report
if st.button("Generate Coaching Report"):
    # Here you would include the logic to process the resume and job description
    # and generate the coaching report.
    # For example, you could display the result like this:
    # report = generate_coaching_report(resume_text, job_description_text)
    # st.write(report)
    if resume_text and job_description_text:
        st.success("The coaching report has been generated! (Placeholder)")
        st.session_state.resume_text = resume_text
        st.session_state.job_description_text = job_description_text
    else:
        st.error("Please paste both your resume and the job description to generate the coaching report.")
