"""
Main application entry point for Mann Kendall Automated.
This script launches the Streamlit web application.
"""

__author__ = "Gabriel Barbosa Soares"


from mann_kendall.ui.streamlit_app import main

if __name__ == "__main__":
    # Launch the Streamlit app
    main()