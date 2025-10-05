st.title("📝 Task Input & Workflow Creation")

# Task creation form
with st.form("task_form"):
    st.subheader("Create New Workflow")
    
    col1, col2 = st.columns(2)
    
    with col1:
        workflow_type = st.selectbox(
            "Workflow Type:",
            ["Research → Analysis → Decision", "Research Only", "Analysis Only", "Custom"]
        )
        
        task_query = st.text_area(
            "Task Description:",
            placeholder="Enter your research question or task...",
            height=100
        )
        
        priority = st.selectbox("Priority:", ["High", "Medium", "Low"])
    
    with col2:
        # File upload for additional context
        uploaded_file = st.file_uploader(
            "Upload Context File (optional):",
            type=['txt', 'csv', 'json', 'pdf']
        )
        
        # Advanced parameters
        with st.expander("Advanced Parameters"):
            max_tokens = st.number_input("Max Tokens:", min_value=100, max_value=4000, value=1000)
            confidence_threshold = st.slider("Confidence Threshold:", 0.0, 1.0, 0.7)
            enable_human_review = st.checkbox("Enable Human Review", value=True)
    
    submitted = st.form_submit_button("🚀 Start Workflow", type="primary")
    
    if submitted and task_query:
        # Prepare workflow request
        workflow_request = {
            "workflow_id": f"workflow_{int(time.time())}",
            "tasks": [
                {
                    "agent_id": "research",
                    "query": task_query,
                    "params": {
                        "max_tokens": max_tokens,
                        "priority": priority.lower()
                    }
                }
            ]
        }
        
        # Add file content if uploaded
        if uploaded_file:
            file_content = uploaded_file.read().decode('utf-8')
            workflow_request["tasks"][0]["params"]["context"] = file_content
        
        # Submit to API
        result = call_api("/orchestrate", "POST", workflow_request)
        
        if result:
            st.success(f"✅ Workflow started! ID: {workflow_request['workflow_id']}")
            st.session_state.workflows[workflow_request['workflow_id']] = {
                "status": "running",
                "created_at": datetime.now(),
                "query": task_query,
                "type": workflow_type
            }
            st.session_state.current_workflow_id = workflow_request['workflow_id']
            st.rerun()
        else:
            st.error("❌ Failed to start workflow")

# Recent workflows
st.subheader("📋 Recent Workflows")
if st.session_state.workflows:
    workflows_df = pd.DataFrame([
        {
            "Workflow ID": wf_id,
            "Query": data["query"][:50] + "...",
            "Type": data["type"],
            "Status": data["status"],
            "Created": data["created_at"].strftime("%H:%M:%S")
        }
        for wf_id, data in st.session_state.workflows.items()
    ])
    st.dataframe(workflows_df, use_container_width=True)
else:
    st.info("No workflows created yet. Create your first workflow above!")
