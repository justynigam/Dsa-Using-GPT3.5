import os
import streamlit as st

# Method 1: Environment Variable (Recommended for local development)
#OPENAI_API_KEY = os.getenv('bce4e89902160a5eed7d2279b4685a2a')

# Method 2: Streamlit Secrets (Recommended for Streamlit Cloud deployment)
# Add this to .streamlit/secrets.toml file:
# OPENAI_API_KEY = "your_openai_api_key_here"
#STREAMLIT_API_KEY = st.secrets.get('OPENAI_API_KEY')

# Method 3: Direct Configuration (Not Recommended for Production)
OPENAI_API_KEY = "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"

# Configuration Settings
class Config:
    # OpenAI API Configuration
    OPENAI_MODEL = "gpt-3.5-turbo"  # Can be changed to gpt-4 if available
    MAX_TOKENS = 1000
    TEMPERATURE = 0.7

    # Application Settings
    APP_TITLE = "DSA Learning Platform"
    APP_ICON = "🧠"

    # Difficulty Levels
    DIFFICULTY_LEVELS = ["Easy", "Medium", "Hard"]

    # DSA Topics
    DSA_TOPICS = [
        "Arrays", "Linked Lists", "Trees", "Graphs",
        "Dynamic Programming", "Strings", "Recursion",
        "Sorting", "Searching", "Stack", "Queue"
    ]

# Function to get API Key
def get_openai_api_key():
    """
    Retrieve OpenAI API Key with fallback methods
    """
    # Priority: Environment Variable > Streamlit Secrets > Direct Configuration
    if OPENAI_API_KEY:
        return OPENAI_API_KEY

    # Uncomment the following line if using direct configuration (not recommended)
    # elif DIRECT_API_KEY:
    #     return DIRECT_API_KEY
    else:
        raise ValueError(
            "OpenAI API Key not found. "
            "Please set it as an environment variable or in Streamlit secrets."
        )
