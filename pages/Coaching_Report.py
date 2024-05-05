import streamlit as st
st.title("CareerPilot")
st.caption("Where your career takes flight")
st.divider()
st.markdown("<h3>Coaching Report</h3>", unsafe_allow_html=True)
st.caption("Have a conversation to get more advice about your resume")

# Display an error if there is one
if 'error' in st.session_state:
    st.error(st.session_state['error'])
elif not st.session_state.get('resume_text') or not st.session_state.get('job_description_text'):
    st.warning("Input resume and job description on the home page access coaching report.")
    if st.button("Go Home", type="primary"):
      st.switch_page("Home.py")
else:
    # Here you would include the logic to process the resume and job description
    # and generate the coaching report.
    # For example, you could display the result like this:
    # report = generate_coaching_report(st.session_state.resume_text, st.session_state.job_description_text)
    # st.write(report)
    st.write(f"Here is a placeholder report: {st.session_state.resume_text} {st.session_state.job_description_text} ")
    if st.button("Talk to Resume Coach", type="primary"):
      st.switch_page("pages/Replicate_Chatbot.py")