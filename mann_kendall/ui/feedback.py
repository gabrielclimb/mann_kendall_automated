__author__ = "Gabriel Barbosa Soares"

import requests
import streamlit as st

FORMSPREE_ENDPOINT = "https://formspree.io/f/xeelvjdr"


def create_feedback_section() -> None:
    """
    Render feedback form in sidebar using Formspree integration.

    Allows users to send feedback directly to the project maintainer via email.
    The form includes optional name/email fields and a required message field.
    """
    with st.expander("💬 Send Feedback"):
        st.markdown("Help us improve! Share your thoughts, report bugs, or request features.")

        with st.form("feedback_form", clear_on_submit=True):
            name = st.text_input("Name (optional)", placeholder="Your name", help="Optional - helps us personalize our response")

            email = st.text_input(
                "Email (optional)",
                placeholder="your.email@example.com",
                help="Optional - we'll only use this to reply to your feedback",
            )

            category = st.selectbox(
                "Category",
                ["General Feedback", "Bug Report", "Feature Request", "Question"],
                help="Select the type of feedback you're providing",
            )

            message = st.text_area(
                "Your message *",
                height=150,
                placeholder="Tell us what you think...",
                help="Required - please provide details about your feedback",
            )

            submit = st.form_submit_button("📧 Send Feedback", use_container_width=True)

            if submit:
                if not message.strip():
                    st.error("❌ Please enter a message before submitting.")
                else:
                    payload = {
                        "name": name if name.strip() else "Anonymous",
                        "email": email if email.strip() else "Not provided",
                        "category": category,
                        "message": message,
                        "_subject": f"MKA Feedback: {category}",  # Custom email subject
                    }

                    try:
                        response = requests.post(
                            FORMSPREE_ENDPOINT, data=payload, headers={"Accept": "application/json"}, timeout=10
                        )

                        if response.status_code == 200:
                            st.success("✅ Thank you! Your feedback has been sent successfully.")
                            st.balloons()
                        else:
                            st.error("❌ Failed to send feedback. Please try again or contact us directly.")
                    except requests.exceptions.Timeout:
                        st.error("❌ Request timed out. Please check your connection and try again.")
                    except requests.exceptions.RequestException as e:
                        st.error(f"❌ Network error: {str(e)}")
                    except Exception as e:
                        st.error(f"❌ Unexpected error: {str(e)}")

        st.caption("🔒 Your feedback is sent securely via Formspree. We respect your privacy.")
