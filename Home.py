import streamlit as st
from helpers import doc_to_text, pdf_to_text
from io import StringIO
from langchain_community.llms import Replicate
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationBufferMemory

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
tab1, tab2, tab3 = st.tabs(["Upload Resume & Job Description", "Coaching Report", "AI Resume Coach"])

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
    if 'error' in st.session_state:
        st.error(st.session_state['error'])
    elif 'processed_resume' not in st.session_state or 'job_description_text' not in st.session_state or not st.session_state.get('processed_resume') or not st.session_state.get('job_description_text'):
        st.warning("Submit both a resume and job description in the previous tab to generate the coaching report.")
    else:
        st.markdown("<h3>Coaching Report</h3>", unsafe_allow_html=True)
        st.caption("Analysis & actionable feedback on tailoring your resume for the job")
        st.success("The coaching report has been generated! (Placeholder)")

# Tab 3: AI Resume Coach Chatbot
with tab3:
    st.markdown("<h3>AI Resume Coach</h3>", unsafe_allow_html=True)
    st.caption("Have a conversation to get more advice about your resume")

    # Display an error if there is one
    if 'error' in st.session_state:
        st.error(st.session_state['error'])
    elif 'processed_resume' not in st.session_state or 'job_description_text' not in st.session_state or not st.session_state.get('processed_resume') or not st.session_state.get('job_description_text'):
        st.warning("Submit both a resume and job description in the first tab to access the AI Resume Coach.")
    else:
        # Initialize the conversation chain and memory if not already done
        if 'conversation_chain' not in st.session_state:
            replicate_llm = Replicate(
                model="meta/meta-llama-3-8b-instruct",
                model_kwargs={"temperature": 0.75, "max_length": 500, "top_p": 1}
            )
            memory = ConversationBufferMemory()
            st.session_state.conversation_chain = ConversationChain(
                llm=replicate_llm,
                memory=memory,
            )

        # Create a list for storing messages if it doesn't exist
        if 'messages' not in st.session_state:
            st.session_state.messages = []

        # Display the chat messages
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # Input field for user's prompt
        prompt = st.chat_input("How can I better tailor my resume for the job?")
        if prompt:
            st.session_state.messages.append({"role": "user", "content": prompt})
            try:
                # Generate a response from the AI
                response = st.session_state.conversation_chain.invoke(input=prompt)
                # Parse the response to display only the AI's response part
                ai_response = response.get('response') if isinstance(response, dict) else response
                st.session_state.messages.append({"role": "assistant", "content": ai_response})
            except Exception as e:
                # Handle exceptions from the AI model
                response = f"Failed to generate a response: {str(e)}"
                st.session_state.messages.append({"role": "assistant", "content": response})

            # Rerun to update the page with the new messages
            st.rerun()
