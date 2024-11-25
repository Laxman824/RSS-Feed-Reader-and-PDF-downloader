# helpers.py
import logging
from pathlib import Path
import pandas as pd
from datetime import datetime

def setup_logging():
    """Configure logging for the application"""
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_dir / "app.log"),
            logging.StreamHandler()
        ]
    )

# def load_css():
#     """Load custom CSS styles"""
#     css_file = Path("src/styles/main.css")
#     if css_file.exists():
#         with open(css_file) as f:
#             return f"<style>{f.read()}</style>"
#     return ""


import streamlit as st
from pathlib import Path

def load_css():
    """Load and apply custom CSS styles"""
    css_file = Path(__file__).parent.parent / "styles" / "main.css"
    if css_file.exists():
        with open(css_file) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    else:
        st.warning("CSS file not found!")