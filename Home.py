import streamlit as st
from helpers import doc_to_text, pdf_to_text
from io import StringIO

# Main title
st.title("CareerPilot")
st.caption("Where your career takes flight")

# Create two containers for the text areas and file uploader
with st.container():
    st.markdown("<h3>1. Paste or Upload Resume</h3>", unsafe_allow_html=True)
    resume_text = st.text_area("Paste resume:")
    uploaded_file = st.file_uploader("Upload resume as DOC, DOCX, PDF, or TXT:", type=["doc", "docx", "pdf", "txt"])  # No width specified

    # Placeholder for info message
    resume_info_placeholder = st.empty()

    # Determine the source of the resume
    resume_source = None
    if resume_text.strip():
        resume_source = "pasted"
    if uploaded_file:
        resume_source = "uploaded"

    # Display the source of the resume
    if resume_source:
        resume_info_placeholder.info(f"Using {resume_source} resume.")

st.markdown("---")  # Adds a horizontal line for better separation

with st.container():
    st.markdown("<h3>2. Paste Job Description</h3>", unsafe_allow_html=True)
    job_description_text = st.text_area("Paste job description:")

st.markdown("---")  # Adds a horizontal line for better separation

# Button to generate the coaching report
st.markdown("<h3>3. Get Coaching Report</h3>", unsafe_allow_html=True)

if (resume_text.strip() or uploaded_file) and job_description_text.strip():
    if st.button("Generate Coaching Report"):
        # Set session state only when the button is clicked
        if uploaded_file is not None:
            try:
                name = uploaded_file.name.lower()
                if name.endswith('pdf'):
                    st.session_state.resume_text = pdf_to_text(uploaded_file)
                elif name.endswith('doc') or name.endswith('docx'):
                    st.session_state.resume_text = doc_to_text(uploaded_file)
                else:
                    st.session_state.resume_text = StringIO(uploaded_file.getvalue().decode("utf-8")).read()
            except Exception as e:
                st.error("Error parsing the uploaded file. Try a different format.")
                st.stop()
        elif resume_text.strip():
            st.session_state.resume_text = resume_text.strip()

        st.session_state.job_description_text = job_description_text.strip()

        # Here you would include the logic to process the resume and job description
        # and generate the coaching report.
        # For example, you could display the result like this:
        # report = generate_coaching_report(st.session_state.resume_text, st.session_state.job_description_text)
        # st.write(report)
        st.success("The coaching report has been generated! (Placeholder)")
else:
    if not (resume_text.strip() or uploaded_file) and not job_description_text.strip():
        st.warning("Submit resume and job description to generate the coaching report.")
    elif not (resume_text.strip() or uploaded_file):
        st.warning("Submit resume to generate the coaching report.")
    elif not job_description_text.strip():
        st.warning("Submit job description to generate the coaching report.")
