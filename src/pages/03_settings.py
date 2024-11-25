
# 03_settings.py
import streamlit as st
import yaml
from pathlib import Path

def show():
    st.title("Settings")
    
    # Load current settings
    config_path = Path("config/config.yaml")
    with open(config_path) as cfg:
        settings = yaml.safe_load(cfg)
    
    # Display settings form
    st.write("## Application Settings")
    
    # Theme settings
    st.write("### Theme Settings")
    theme = st.selectbox(
        "Select Theme",
        ["Light", "Dark"],
        index=0 if settings.get('theme') == 'light' else 1
    )
    
    # Data settings
    st.write("### Data Settings")
    auto_refresh = st.checkbox(
        "Auto Refresh Data",
        value=settings.get('auto_refresh', False)
    )
    refresh_interval = st.number_input(
        "Refresh Interval (minutes)",
        min_value=1,
        value=settings.get('refresh_interval', 5)
    )
    
    # Save settings
    if st.button("Save Settings"):
        settings.update({
            'theme': theme.lower(),
            'auto_refresh': auto_refresh,
            'refresh_interval': refresh_interval
        })
        
        with open(config_path, 'w') as cfg:
            yaml.dump(settings, cfg)
        
        st.success("Settings saved successfully!")