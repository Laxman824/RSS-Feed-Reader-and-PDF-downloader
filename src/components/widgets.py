
# widgets.py
import streamlit as st

def display_header():
    """Display the app header with title and description"""
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.title("RSS FEED")
        st.markdown("Your app description goes here")
    
    with col2:
        if st.button("Help"):
            st.info("Help information goes here")

def custom_metric_card(title, value, delta=None):
    """Display a metric in a custom card format"""
    st.markdown(
        f"""
        <div style="
            padding: 20px;
            background-color: #f0f2f6;
            border-radius: 10px;
            margin: 10px 0;
        ">
            <h3>{title}</h3>
            <h2>{value}</h2>
            {f'<p style="color: {"green" if delta >= 0 else "red"}">({delta:+.1f}%)</p>' if delta is not None else ''}
        </div>
        """,
        unsafe_allow_html=True
    )

def data_table(data, height=400):
    """Display a scrollable data table with formatting"""
    st.markdown(
        f"""
        <style>
        .dataframe {{
            font-size: 12px;
            max-height: {height}px;
            overflow-y: auto;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )
    st.dataframe(data)