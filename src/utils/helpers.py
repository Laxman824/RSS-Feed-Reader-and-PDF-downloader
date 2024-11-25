import logging
from pathlib import Path
import streamlit as st

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

def create_directories():
    """Create necessary directories if they don't exist"""
    directories = [
        Path("data/downloaded_pdfs"),
        Path("logs")
    ]
    
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)

def format_date(date_str: str) -> str:
    """Format date string for display"""
    try:
        from dateutil import parser
        date_obj = parser.parse(date_str)
        return date_obj.strftime("%B %d, %Y")
    except:
        return date_str

def clean_text(text: str) -> str:
    """Clean text for display"""
    import re
    text = re.sub(r'<[^>]+>', '', text)  # Remove HTML tags
    text = ' '.join(text.split())  # Normalize whitespace
    return text