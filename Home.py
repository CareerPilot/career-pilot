import streamlit as st
from helpers import doc_to_text, pdf_to_text
from io import StringIO

# Set the page title and subtitle
st.title("CareerPilot")
st.caption("Where your career takes flight")

# Function to handle document processing
def process_documents(uploaded_file, resume_text):
    try:
        if uploaded_file is not None:
            name = uploaded_file.name.lower()
            if name.endswith('pdf'):
                return pdf_to_text(uploaded_file)
            elif name.endswith('doc') or name.endswith('docx'):
                return doc_to_text(uploaded_file)
            else:
                return StringIO(uploaded_file.getvalue().decode("utf-8")).read()
        else:
            return resume_text.strip()
    except Exception as e:
        st.session_state['error'] = "Error parsing the uploaded file. Try a different format."
        return None

# Function to clear error when file is removed
def handle_file_uploader_change():
    if 'uploaded_file' in st.session_state and not st.session_state['uploaded_file']:
        st.session_state.pop('error', None)

# Create the tab structure
tab1, tab2 = st.tabs(["Upload Resume & Job Description", "Coaching Report"])

# Tab 1: Upload Resume & Job Description
with tab1:
    with st.container():
        st.markdown("<h3>1. Paste or Upload Resume</h3>", unsafe_allow_html=True)
        resume_text = st.text_area("Paste resume:")
        uploaded_file = st.file_uploader("Upload resume as DOC, DOCX, PDF, or TXT:",
                                         type=["doc", "docx", "pdf", "txt"],
                                         on_change=handle_file_uploader_change,
                                         key='uploaded_file')

    with st.container():
        st.markdown("<h3>2. Paste Job Description</h3>", unsafe_allow_html=True)
        job_description_text = st.text_area("Paste job description:")

    # Attempt to process documents
    if resume_text or uploaded_file:
        processed_resume = process_documents(uploaded_file, resume_text)
        if processed_resume:
            st.session_state['processed_resume'] = processed_resume
            if 'error' in st.session_state:
                del st.session_state['error']
        else:
            st.session_state.pop('processed_resume', None)
    else:
        st.session_state.pop('processed_resume', None)

    if job_description_text:
        st.session_state['job_description_text'] = job_description_text.strip()
    else:
        st.session_state.pop('job_description_text', None)



# Tab 2: Coaching Report
with tab2:
    st.markdown("<h3>Coaching Report</h3>", unsafe_allow_html=True)
    st.caption("Analysis & actionable feedback on tailoring your resume for the job")
    if 'error' in st.session_state:
        st.error(st.session_state['error'])
    elif 'processed_resume' not in st.session_state or 'job_description_text' not in st.session_state or not st.session_state.get('processed_resume') or not st.session_state.get('job_description_text'):
        st.warning("Submit both a resume and job description in the previous tab to generate the coaching report.")
    else:

        st.success("The coaching report has been generated! (Placeholder)")

