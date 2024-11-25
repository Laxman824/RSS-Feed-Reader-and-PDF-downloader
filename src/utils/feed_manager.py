
# data_loader.py
import pandas as pd
import streamlit as st
from pathlib import Path

@st.cache_data
def load_data(file_path: str) -> pd.DataFrame:
    """Load and cache data from various file formats"""
    file_path = Path(file_path)
    
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    
    if file_path.suffix == '.csv':
        return pd.read_csv(file_path)
    elif file_path.suffix in ['.xls', '.xlsx']:
        return pd.read_excel(file_path)
    elif file_path.suffix == '.json':
        return pd.read_json(file_path)
    else:
        raise ValueError(f"Unsupported file format: {file_path.suffix}")

def preprocess_data(df: pd.DataFrame) -> pd.DataFrame:
    """Preprocess the loaded data"""
    # Add your preprocessing steps here
    # Example:
    df = df.copy()
    df.dropna(inplace=True)
    df.reset_index(drop=True, inplace=True)
    return df

def save_data(df: pd.DataFrame, file_path: str) -> None:
    """Save processed data to file"""
    file_path = Path(file_path)
    file_path.parent.mkdir(parents=True, exist_ok=True)
    
    if file_path.suffix == '.csv':
        df.to_csv(file_path, index=False)
    elif file_path.suffix in ['.xlsx']:
        df.to_excel(file_path, index=False)
    elif file_path.suffix == '.json':
        df.to_json(file_path)
    else:
        raise ValueError(f"Unsupported file format: {file_path.suffix}")