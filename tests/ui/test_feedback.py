"""Tests for feedback.py module."""

import logging
from unittest.mock import MagicMock, patch

from mann_kendall.ui.feedback import EMAIL_PLACEHOLDER, create_feedback_section


@patch("mann_kendall.ui.feedback.requests.post")
@patch("mann_kendall.ui.feedback.st")
def test_empty_email_uses_placeholder(mock_st, mock_post):
    """Ensure placeholder email is sent when user leaves email blank."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_post.return_value = mock_response

    # Set up streamlit mocks for form context
    mock_st.expander.return_value.__enter__ = MagicMock()
    mock_st.expander.return_value.__exit__ = MagicMock(return_value=False)
    mock_form = MagicMock()
    mock_st.form.return_value.__enter__ = MagicMock(return_value=mock_form)
    mock_st.form.return_value.__exit__ = MagicMock(return_value=False)

    mock_st.text_input.side_effect = ["", ""]
    mock_st.selectbox.return_value = "General Feedback"
    mock_st.text_area.return_value = "Test feedback message"
    mock_st.form_submit_button.return_value = True

    create_feedback_section()

    assert mock_post.called, "Form submission should trigger Formspree request"
    _, kwargs = mock_post.call_args
    assert kwargs["data"]["email"] == EMAIL_PLACEHOLDER


@patch("mann_kendall.ui.feedback.requests.post")
@patch("mann_kendall.ui.feedback.st")
def test_non_200_response_logs_error(mock_st, mock_post, caplog):
    """Test that non-200 Formspree response logs status code and body."""
    # Set up mock response with non-200 status
    mock_response = MagicMock()
    mock_response.status_code = 422
    mock_response.text = '{"error": "invalid email"}'
    mock_post.return_value = mock_response

    # Set up streamlit mocks for form context
    mock_st.expander.return_value.__enter__ = MagicMock()
    mock_st.expander.return_value.__exit__ = MagicMock(return_value=False)
    mock_form = MagicMock()
    mock_st.form.return_value.__enter__ = MagicMock(return_value=mock_form)
    mock_st.form.return_value.__exit__ = MagicMock(return_value=False)

    mock_st.text_input.side_effect = ["Test User", "test@example.com"]
    mock_st.selectbox.return_value = "General Feedback"
    mock_st.text_area.return_value = "Test feedback message"
    mock_st.form_submit_button.return_value = True

    with caplog.at_level(logging.ERROR, logger="mann_kendall"):
        create_feedback_section()

    # Verify that error details were logged
    assert any("422" in record.message for record in caplog.records), (
        "Expected status code 422 to be logged"
    )
    assert any("invalid email" in record.message for record in caplog.records), (
        "Expected response body to be logged"
    )

    # Verify user-facing error does NOT expose status code or technical details
    error_calls = [str(call) for call in mock_st.error.call_args_list]
    assert any("Failed to send feedback" in call for call in error_calls), (
        "Expected generic error message shown to user"
    )
    assert all("422" not in call for call in error_calls), (
        "Status code should NOT appear in user-facing error message"
    )
