# 01_home.py
import streamlit as st
from components.widgets import custom_metric_card

def show():
    st.title("Home")
    
    # Display key metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        custom_metric_card("Metric 1", "1,234", 5.2)
    with col2:
        custom_metric_card("Metric 2", "5,678", -2.1)
    with col3:
        custom_metric_card("Metric 3", "9,012", 0.8)
    
    # Add more content
    st.write("## Recent Activity")
    st.write("Your recent activity will appear here")
