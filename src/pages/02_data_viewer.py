
# 02_data_viewer.py
import streamlit as st
import pandas as pd
from utils.data_loader import load_data, preprocess_data
from components.widgets import data_table

def show():
    st.title("Data Viewer")
    
    # File uploader
    uploaded_file = st.file_uploader("Upload Data", type=['csv', 'xlsx', 'json'])
    
    if uploaded_file is not None:
        try:
            # Load and preprocess data
            df = load_data(uploaded_file)
            df = preprocess_data(df)
            
            # Display data summary
            st.write("## Data Summary")
            st.write(f"Total Records: {len(df)}")
            
            # Display data
            st.write("## Data Preview")
            data_table(df)
            
            # Add visualization options
            st.write("## Visualizations")
            chart_type = st.selectbox(
                "Select Chart Type",
                ["Line Chart", "Bar Chart", "Scatter Plot"]
            )
            
            if chart_type == "Line Chart":
                st.line_chart(df)
            elif chart_type == "Bar Chart":
                st.bar_chart(df)
            elif chart_type == "Scatter Plot":
                st.scatter_chart(df)
                
        except Exception as e:
            st.error(f"Error loading data: {str(e)}")
