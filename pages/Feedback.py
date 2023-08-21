import streamlit as st

# Streamlit app configuration
st.set_page_config(
    page_title="CAPM Project with Feedback",
    page_icon="chart_with_upwards_trend",
    layout="wide"
)


# Feedback Form
st.title("Feedback Form")

with st.form("feedback_form"):
    st.write("Please provide your feedback:")
    feedback_text = st.text_area("Feedback", "")
    submitted = st.form_submit_button("Submit Feedback")

if submitted:
    # Save the feedback in a file, database, or send via email
    with open("feedback.txt", "a") as f:
        f.write(feedback_text + "\n")
    st.success("Thank you for your feedback!")


