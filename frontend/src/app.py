import streamlit as st
import requests

st.set_page_config(page_title="Construction Legal AI", page_icon="🏗️")

st.title("🏗️ Construction Legal AI (CLA)")
st.caption("Contract-Centric Conflict Resolution Engine")

st.markdown("---")

# Sidebar
with st.sidebar:
    st.header("Settings")
    st.info("Connected to Backend: http://backend:8000")

# Main Content
st.header("Ask a Legal Question")
query = st.text_area("Enter your query regarding the contract:", height=150)

if st.button("Submit Query"):
    if query:
        st.write("Processing...")
        # Placeholder for API call
        # response = requests.post("http://backend:8000/query", json={"query": query})
        # st.write(response.json())
        st.success("This is a placeholder response. Backend connection will be implemented soon.")
    else:
        st.warning("Please enter a query.")
