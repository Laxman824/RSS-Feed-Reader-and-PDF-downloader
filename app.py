import streamlit as st
import feedparser
import requests
from bs4 import BeautifulSoup
import os
import tempfile
from datetime import datetime
import logging
from pathlib import Path
import pandas as pd
import time
import yaml
from typing import List, Dict, Optional

# Initialize session state variables
def init_session_state():
    """Initialize session state variables"""
    if 'feeds' not in st.session_state:
        st.session_state.feeds = []
    if 'processed_links' not in st.session_state:
        st.session_state.processed_links = set()
    if 'downloaded_pdfs' not in st.session_state:
        st.session_state.downloaded_pdfs = []

class RSSFeedManager:
    def __init__(self):
        """Initialize the RSS Feed Manager"""
        self.setup_session_state()
        
    def setup_session_state(self):
        """Initialize session state variables"""
        if 'feeds' not in st.session_state:
            st.session_state.feeds = []
        if 'processed_links' not in st.session_state:
            st.session_state.processed_links = set()
        if 'downloaded_pdfs' not in st.session_state:
            st.session_state.downloaded_pdfs = []

    def validate_feed(self, url: str) -> bool:
        """Validate if the URL is a valid RSS feed"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(url, headers=headers, timeout=10)
            feed = feedparser.parse(response.content)
            return len(feed.entries) > 0
        except Exception as e:
            logging.error(f"Feed validation error: {str(e)}")
            return False

def render_sidebar():
    """Render sidebar with feed management options"""
    with st.sidebar:
        st.header("Add RSS Feed")
        new_feed = st.text_input("Enter RSS Feed URL")
        if st.button("Add Feed"):
            if new_feed:
                feed_manager = RSSFeedManager()
                if feed_manager.validate_feed(new_feed):
                    if new_feed not in st.session_state.feeds:
                        st.session_state.feeds.append(new_feed)
                        st.success("Feed added successfully!")
                    else:
                        st.warning("This feed is already added.")
                else:
                    st.error("Invalid RSS feed URL")

        st.header("Manage Feeds")
        if st.session_state.feeds:  # Check if feeds exist
            for i, feed in enumerate(st.session_state.feeds):
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.text(feed)
                with col2:
                    if st.button("Remove", key=f"remove_{i}"):
                        st.session_state.feeds.remove(feed)
                        st.rerun()
        else:
            st.info("No feeds added yet. Add an RSS feed above to get started!")

def render_feed_viewer():
    """Render the feed content viewer"""
    st.header("Feed Content")
    if not st.session_state.feeds:
        st.info("Add some RSS feeds to get started!")
        return

    selected_feed = st.selectbox("Select Feed", st.session_state.feeds)
    if selected_feed:
        feed_manager = RSSFeedManager()
        with st.spinner("Loading feed content..."):
            entries = feed_manager.fetch_feed_content(selected_feed)
            if entries:
                for entry in entries:
                    with st.expander(entry['title']):
                        st.write(f"Published: {entry['published']}")
                        st.write(entry['summary'])
                        st.markdown(f"[Read More]({entry['link']})")
            else:
                st.warning("No entries found in this feed.")

def render_pdf_downloader():
    """Render the PDF downloader interface"""
    st.header("PDF Downloader")
    if not st.session_state.feeds:
        st.info("Add some RSS feeds to get started!")
        return

    selected_feed = st.selectbox(
        "Select Feed", 
        st.session_state.feeds,
        key="pdf_feed_selector"
    )

    if st.button("Scan for PDFs"):
        feed_manager = RSSFeedManager()
        with st.spinner("Scanning for PDFs..."):
            entries = feed_manager.fetch_feed_content(selected_feed)
            pdf_links = []

            for entry in entries:
                if entry['link'].lower().endswith('.pdf'):
                    pdf_links.append((entry['title'], entry['link']))
                else:
                    pdf_url = feed_manager.extract_pdf_link(entry['link'])
                    if pdf_url:
                        pdf_links.append((entry['title'], pdf_url))

            if pdf_links:
                st.success(f"Found {len(pdf_links)} PDFs!")
                for title, url in pdf_links:
                    if url not in st.session_state.processed_links:
                        col1, col2 = st.columns([3, 1])
                        with col1:
                            st.write(title)
                        with col2:
                            try:
                                response = requests.get(url)
                                if response.status_code == 200:
                                    st.download_button(
                                        label="Download",
                                        data=response.content,
                                        file_name=f"{title}.pdf",
                                        mime="application/pdf",
                                        key=f"download_{url}"
                                    )
                            except Exception as e:
                                st.error(f"Error preparing download: {str(e)}")
            else:
                st.warning("No PDFs found in this feed.")

def main():
    # Page config
    st.set_page_config(
        page_title="RSS Feed PDF Downloader",
        page_icon="📚",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # Initialize session state
    init_session_state()

    # App title
    st.title("RSS Feed PDF Downloader")

    # Render sidebar
    render_sidebar()

    # Main content tabs
    tab1, tab2 = st.tabs(["Feed Viewer", "PDF Downloader"])

    with tab1:
        render_feed_viewer()

    with tab2:
        render_pdf_downloader()

    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center'>
            <p>Made with ❤️ using Streamlit</p>
        </div>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()