import streamlit as st
import feedparser
import requests
import os
from datetime import datetime
import time
from bs4 import BeautifulSoup
import pandas as pd
import logging
import re
from typing import List, Dict, Optional

class RSSFeedManager:
    def __init__(self):
        """Initialize the RSS Feed Manager"""
        self.download_dir = "downloaded_pdfs"
        self.setup_logging()
        self.ensure_download_directory()
        
        # Initialize session state for RSS feeds if not exists
        if 'rss_feeds' not in st.session_state:
            st.session_state.rss_feeds = []
        if 'processed_links' not in st.session_state:
            st.session_state.processed_links = set()

    def setup_logging(self):
        """Set up logging configuration"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('rss_manager.log'),
                logging.StreamHandler()
            ]
        )

    def ensure_download_directory(self):
        """Create download directory if it doesn't exist"""
        if not os.path.exists(self.download_dir):
            os.makedirs(self.download_dir)
            logging.info(f"Created download directory: {self.download_dir}")

    def validate_rss_url(self, url: str) -> bool:
        """Validate if the given URL is a valid RSS feed"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(url, headers=headers, timeout=10)
            feed = feedparser.parse(response.content)
            return len(feed.entries) > 0
        except Exception as e:
            logging.error(f"Error validating RSS feed {url}: {str(e)}")
            return False

    def get_pdf_from_webpage(self, url: str) -> Optional[str]:
        """Extract PDF link from webpage"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(url, headers=headers, timeout=30)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                for link in soup.find_all('a'):
                    href = link.get('href', '')
                    if href.lower().endswith('.pdf'):
                        return href if href.startswith('http') else f"https://{href}" if href.startswith('//') else url + href
            return None
        except Exception as e:
            logging.error(f"Error extracting PDF from webpage {url}: {str(e)}")
            return None

    def download_pdf(self, url: str, filename: str) -> bool:
        """Download PDF from given URL"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(url, headers=headers, stream=True, timeout=30)
            
            if response.status_code == 200:
                filepath = os.path.join(self.download_dir, filename)
                with open(filepath, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                return True
            return False
        except Exception as e:
            logging.error(f"Error downloading PDF {url}: {str(e)}")
            return False

    def clean_filename(self, title: str) -> str:
        """Clean the filename to remove invalid characters"""
        filename = "".join([c for c in title if c.isalnum() or c in (' ', '-', '_')]).rstrip()
        return filename.replace(' ', '_') + '.pdf'

    def fetch_feed_entries(self, url: str) -> List[Dict]:
        """Fetch entries from a single RSS feed"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(url, headers=headers)
            feed = feedparser.parse(response.content)
            
            entries = []
            for entry in feed.entries:
                entry_data = {
                    'title': entry.get('title', 'No Title'),
                    'link': entry.get('link', ''),
                    'published': entry.get('published', 'No Date'),
                    'summary': entry.get('summary', 'No Summary'),
                }
                entries.append(entry_data)
            return entries
        except Exception as e:
            logging.error(f"Error fetching feed {url}: {str(e)}")
            return []

def main():
    st.set_page_config(page_title="RSS Feed PDF Downloader", layout="wide")
    st.title("RSS Feed PDF Downloader")

    # Initialize RSS Feed Manager
    manager = RSSFeedManager()

    # Sidebar for adding RSS feeds
    with st.sidebar:
        st.header("Add RSS Feed")
        new_feed = st.text_input("Enter RSS Feed URL")
        if st.button("Add Feed"):
            if new_feed:
                if manager.validate_rss_url(new_feed):
                    if new_feed not in st.session_state.rss_feeds:
                        st.session_state.rss_feeds.append(new_feed)
                        st.success("RSS Feed added successfully!")
                    else:
                        st.warning("This feed is already added.")
                else:
                    st.error("Invalid RSS feed URL")

        st.header("Manage Feeds")
        for i, feed in enumerate(st.session_state.rss_feeds):
            col1, col2 = st.columns([3, 1])
            with col1:
                st.text(feed)
            with col2:
                if st.button("Remove", key=f"remove_{i}"):
                    st.session_state.rss_feeds.remove(feed)
                    st.rerun()

    # Main content area
    if not st.session_state.rss_feeds:
        st.info("Add RSS feeds using the sidebar to get started!")
    else:
        # Tabs for different views
        tab1, tab2 = st.tabs(["Feed Viewer", "PDF Downloader"])

        with tab1:
            st.header("Feed Content")
            selected_feed = st.selectbox("Select Feed to View", st.session_state.rss_feeds)
            if selected_feed:
                with st.spinner("Fetching feed content..."):
                    entries = manager.fetch_feed_entries(selected_feed)
                    if entries:
                        for entry in entries:
                            with st.expander(entry['title']):
                                st.write(f"Published: {entry['published']}")
                                st.write(entry['summary'])
                                st.markdown(f"[Read More]({entry['link']})")

        with tab2:
            st.header("Download PDFs")
            selected_feed_download = st.selectbox(
                "Select Feed for PDF Download", 
                st.session_state.rss_feeds,
                key="download_feed"
            )
            
            if st.button("Scan for PDFs"):
                with st.spinner("Scanning for PDFs..."):
                    entries = manager.fetch_feed_entries(selected_feed_download)
                    pdf_links = []
                    
                    for entry in entries:
                        if entry['link'].lower().endswith('.pdf'):
                            pdf_links.append((entry['title'], entry['link']))
                        else:
                            pdf_url = manager.get_pdf_from_webpage(entry['link'])
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
                                    if st.button("Download", key=f"download_{url}"):
                                        filename = manager.clean_filename(title)
                                        if manager.download_pdf(url, filename):
                                            st.session_state.processed_links.add(url)
                                            st.success(f"Downloaded: {filename}")
                                        else:
                                            st.error("Download failed")
                    else:
                        st.warning("No PDFs found in this feed")

    # Footer
    st.markdown("---")
    st.markdown("Made with ❤️ by Laxman")

if __name__ == "__main__":
    main()