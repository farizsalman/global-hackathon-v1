import streamlit as st
import requests
import time
import pandas as pd
from datetime import datetime
import json

# Page config
st.set_page_config(
    page_title="Agent Orchestration Dashboard",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# API Configuration
API_BASE_URL = "http://localhost:8000/api"

# Initialize session state
if "workflows" not in st.session_state:
    st.session_state.workflows = {}
if "current_workflow_id" not in st.session_state:
    st.session_state.current_workflow_id = None

# Sidebar navigation
st.sidebar.title("🤖 Agent Orchestrator")
page = st.sidebar.selectbox(
    "Navigate to:",
    ["Task Input", "Workflow Monitor", "Agent Status", "Results Display"]
)

# API helper functions
def call_api(endpoint, method="GET", data=None):
    """Make API calls to FastAPI backend"""
    try:
        url = f"{API_BASE_URL}{endpoint}"
        if method == "GET":
            response = requests.get(url)
        elif method == "POST":
            response = requests.post(url, json=data)
        return response.json() if response.status_code == 200 else None
    except Exception as e:
        st.error(f"API Error: {str(e)}")
        return None

# Route to pages
if page == "Task Input":
    exec(open("pages/task_input.py").read())
elif page == "Workflow Monitor":
    exec(open("pages/workflow_monitor.py").read())
elif page == "Agent Status":
    exec(open("pages/agent_status.py").read())
elif page == "Results Display":
    exec(open("pages/results_display.py").read())

