st.title("🔍 Workflow Monitor")

# Auto-refresh toggle
auto_refresh = st.sidebar.checkbox("Auto-refresh (5s)", value=True)

if auto_refresh:
    time.sleep(5)
    st.rerun()

# Current workflow selector
if st.session_state.workflows:
    workflow_options = list(st.session_state.workflows.keys())
    selected_workflow = st.selectbox(
        "Select Workflow:",
        workflow_options,
        index=workflow_options.index(st.session_state.current_workflow_id) 
        if st.session_state.current_workflow_id in workflow_options else 0
    )
    
    if selected_workflow:
        st.session_state.current_workflow_id = selected_workflow
        
        # Workflow status header
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Workflow ID", selected_workflow[-8:])
        with col2:
            status = st.session_state.workflows[selected_workflow]["status"]
            st.metric("Status", status.upper())
        with col3:
            st.metric("Agents", "3")
        with col4:
            created_time = st.session_state.workflows[selected_workflow]["created_at"]
            elapsed = (datetime.now() - created_time).seconds
            st.metric("Elapsed", f"{elapsed}s")
        
        # Workflow visualization
        st.subheader("🔄 Workflow Progress")
        
        # Mock progress data (replace with real API calls)
        progress_data = {
            "Research Agent": {"status": "completed", "confidence": 0.85, "time": "12s"},
            "Analysis Agent": {"status": "running", "confidence": 0.0, "time": "8s"},
            "Decision Agent": {"status": "pending", "confidence": 0.0, "time": "0s"}
        }
        
        for agent_name, data in progress_data.items():
            with st.container():
                col1, col2, col3, col4 = st.columns([3, 2, 2, 2])
                
                with col1:
                    if data["status"] == "completed":
                        st.success(f"✅ {agent_name}")
                    elif data["status"] == "running":
                        st.warning(f"⏳ {agent_name}")
                    else:
                        st.info(f"⏸️ {agent_name}")
                
                with col2:
                    st.write(f"Status: {data['status'].title()}")
                
                with col3:
                    if data["confidence"] > 0:
                        st.write(f"Confidence: {data['confidence']:.2f}")
                    else:
                        st.write("Confidence: N/A")
                
                with col4:
                    st.write(f"Time: {data['time']}")
        
        # Real-time logs
        st.subheader("📝 Execution Logs")
        
        logs_container = st.container()
        with logs_container:
            log_messages = [
                "2024-10-05 14:33:01 - Research Agent started",
                "2024-10-05 14:33:05 - Perplexity API called successfully",
                "2024-10-05 14:33:12 - Research completed with confidence 0.85",
                "2024-10-05 14:33:13 - Analysis Agent started",
                "2024-10-05 14:33:15 - Processing research data...",
            ]
            
            for log in log_messages:
                st.text(log)

else:
    st.info("No workflows to monitor. Create a workflow first!")
