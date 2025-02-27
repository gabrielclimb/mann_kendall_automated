#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Main application entry point for Mann Kendall Automated.
This script launches the Streamlit web application.
"""

__author__ = "Gabriel Barbosa Soares"

import streamlit as st

# Import from our refactored package
from mann_kendall.ui.app import main

if __name__ == "__main__":
    # Launch the Streamlit app
    main()