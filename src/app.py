import streamlit as st
import yaml
from pathlib import Path
import logging
from utils.helpers import setup_logging
from components.sidebar import render_sidebar
from components.widgets import display_header
from utils.helpers import load_css
# Configure the app
def configure_app():
    """Configure the Streamlit app"""
    st.set_page_config(
        page_title="RSS Feed and downloader",
        page_icon="🚀",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Load configuration
    config_path = Path("config/config.yaml")
    with open(config_path) as cfg:
        config = yaml.safe_load(cfg)
    
    return config

# Initialize session state
def init_session_state():
    """Initialize session state variables"""
    if 'data' not in st.session_state:
        st.session_state.data = None
    if 'settings' not in st.session_state:
        st.session_state.settings = {}
    if 'auth_status' not in st.session_state:
        st.session_state.auth_status = False

def main():
    # Setup logging
    setup_logging()
    logger = logging.getLogger(__name__)
    load_css()
    try:
        # Configure app and load settings
        config = configure_app()
        
        # Initialize session state
        init_session_state()
        
        # Display header
        display_header()
        
        # Render sidebar
        render_sidebar()
        
        # Main app content
        st.write("## Welcome to  App")
        st.write("This is the main page of your application.")
        
        
        # ...

    except Exception as e:
        logger.error(f"Application error: {str(e)}")
        st.error("An error occurred. Please check the logs for details.")

if __name__ == "__main__":
    main()