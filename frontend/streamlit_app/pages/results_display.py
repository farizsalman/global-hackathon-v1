st.title("📊 Results Display")

# Workflow selector for results
if st.session_state.workflows:
    workflow_options = list(st.session_state.workflows.keys())
    selected_workflow = st.selectbox(
        "View Results for Workflow:",
        workflow_options,
        key="results_workflow_selector"
    )
    
    if selected_workflow:
        # Mock results data
        workflow_results = {
            "research": {
                "success": True,
                "confidence": 0.85,
                "result": {
                    "summary": "Found comprehensive information about the topic with high confidence.",
                    "sources": ["Source 1", "Source 2", "Source 3"],
                    "key_findings": ["Finding 1", "Finding 2", "Finding 3"]
                }
            },
            "analysis": {
                "success": True,
                "confidence": 0.78,
                "result": {
                    "insights": ["Insight 1", "Insight 2"],
                    "trends": ["Trend 1", "Trend 2"],
                    "statistics": {"mean": 45.7, "std": 12.3}
                }
            },
            "decision": {
                "success": True,
                "confidence": 0.81,
                "result": {
                    "recommendation": "Proceed with moderate confidence",
                    "human_review_required": False,
                    "reasoning": "Based on analysis, the recommendation is solid."
                }
            }
        }
        
        # Display results by agent
        for agent_name, result_data in workflow_results.items():
            with st.expander(f"🤖 {agent_name.title()} Agent Results", expanded=True):
                
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    if result_data["success"]:
                        st.success("✅ Completed Successfully")
                    else:
                        st.error("❌ Failed")
                
                with col2:
                    st.metric("Confidence", f"{result_data['confidence']:.2f}")
                
                # Display specific results
                if "result" in result_data:
                    result = result_data["result"]
                    
                    if agent_name == "research":
                        st.markdown("**Summary:**")
                        st.write(result["summary"])
                        
                        st.markdown("**Key Findings:**")
                        for finding in result["key_findings"]:
                            st.write(f"• {finding}")
                            
                        st.markdown("**Sources:**")
                        for source in result["sources"]:
                            st.write(f"• {source}")
                    
                    elif agent_name == "analysis":
                        st.markdown("**Insights:**")
                        for insight in result["insights"]:
                            st.write(f"• {insight}")
                            
                        st.markdown("**Statistics:**")
                        st.json(result["statistics"])
                    
                    elif agent_name == "decision":
                        st.markdown("**Recommendation:**")
                        st.write(result["recommendation"])
                        
                        if result["human_review_required"]:
                            st.warning("⚠️ Human review required")
                        
                        st.markdown("**Reasoning:**")
                        st.write(result["reasoning"])
        
        # Export results
        st.subheader("📥 Export Results")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📄 Export as JSON"):
                st.download_button(
                    "Download JSON",
                    data=json.dumps(workflow_results, indent=2),
                    file_name=f"workflow_results_{selected_workflow}.json",
                    mime="application/json"
                )
        
        with col2:
            if st.button("📊 Export as CSV"):
                # Convert to CSV format
                csv_data = "Agent,Status,Confidence,Details\n"
                for agent, data in workflow_results.items():
                    status = "Success" if data["success"] else "Failed"
                    details = str(data.get("result", ""))
                    csv_data += f"{agent},{status},{data['confidence']},{details}\n"
                
                st.download_button(
                    "Download CSV", 
                    data=csv_data,
                    file_name=f"workflow_results_{selected_workflow}.csv",
                    mime="text/csv"
                )

else:
    st.info("No workflow results available. Complete a workflow first!")
