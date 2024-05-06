import streamlit as st
from langchain_community.llms import Replicate

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
    replicate_llm = Replicate(
        model="meta/meta-llama-3-8b-instruct",
        model_kwargs={"temperature": 0.75, "max_length": 500, "top_p": 1},
    )

    prompt = f"""Please analyze the following resume and job description and generate a comprehensive coaching report on how well the resume matches the job description.
    Start by giving a matching score out of 10.
    Here is the resume: {st.session_state.resume_text}.
    And here is the job description: {st.session_state.job_description_text}"""

    st.write(prompt)  # TODO: Remove this after testing
    # Generate the coaching report
    try:
        response = replicate_llm.invoke(
            prompt
        )  # Directly call the model with the prompt
        st.session_state.coaching_report = (
            response  # Save the response in session state
        )
        st.write(response)  # Display it
    except Exception as e:
        st.error(f"Failed to generate a coaching report: {str(e)}")
