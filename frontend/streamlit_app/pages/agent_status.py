st.title("🤖 Agent Status Dashboard")

# Refresh button
if st.button("🔄 Refresh Status"):
    st.rerun()

# Mock agent data (replace with real API calls)
agents_data = {
    "Research Agent": {
        "status": "healthy",
        "load": 2,
        "max_load": 10,
        "success_rate": 0.94,
        "avg_response_time": 8.5,
        "last_used": "2 mins ago"
    },
    "Analysis Agent": {
        "status": "healthy", 
        "load": 1,
        "max_load": 8,
        "success_rate": 0.89,
        "avg_response_time": 12.3,
        "last_used": "5 mins ago"
    },
    "Decision Agent": {
        "status": "healthy",
        "load": 0,
        "max_load": 5,
        "success_rate": 0.97,
        "avg_response_time": 3.2,
        "last_used": "1 hour ago"
    }
}

# Agent status cards
st.subheader("🔍 Agent Overview")

cols = st.columns(3)

for idx, (agent_name, data) in enumerate(agents_data.items()):
    with cols[idx]:
        status_color = "🟢" if data["status"] == "healthy" else "🔴"
        st.markdown(f"### {status_color} {agent_name}")
        
        # Metrics
        st.metric("Current Load", f"{data['load']}/{data['max_load']}")
        st.metric("Success Rate", f"{data['success_rate']*100:.1f}%")
        st.metric("Avg Response", f"{data['avg_response_time']}s")
        
        # Load progress bar
        load_percentage = data['load'] / data['max_load']
        st.progress(load_percentage)
        
        st.caption(f"Last used: {data['last_used']}")

# Performance metrics
st.subheader("📊 Performance Metrics")

col1, col2 = st.columns(2)

with col1:
    st.markdown("#### Success Rates")
    success_data = {
        agent: data["success_rate"] * 100 
        for agent, data in agents_data.items()
    }
    st.bar_chart(success_data)

with col2:
    st.markdown("#### Response Times")
    response_data = {
        agent: data["avg_response_time"] 
        for agent, data in agents_data.items()
    }
    st.bar_chart(response_data)

# System health
st.subheader("🏥 System Health")

health_metrics = {
    "Total Requests": 1247,
    "Active Workflows": 3,
    "Queue Length": 2,
    "Uptime": "23h 45m"
}

cols = st.columns(4)
for idx, (metric, value) in enumerate(health_metrics.items()):
    with cols[idx]:
        st.metric(metric, value)
