import streamlit as st
import httpx
import json
import time
import asyncio
from typing import Dict, List, Optional

# Set page config
st.set_page_config(
    page_title="AI SEO Buddy",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main {
        background-color: #f5f5f5;
    }
    .stButton>button {
        width: 100%;
        background-color: #2E86C1;
        color: white;
    }
    .stProgress>div>div {
        background-color: #2E86C1;
    }
    .metric-card {
        background-color: white;
        padding: 1rem;
        border-radius: 0.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

def display_metrics(metrics: Dict) -> None:
    """Display SEO metrics in a clean, organized format."""
    
    # Create three columns for main scores
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h3 style="margin:0">Performance</h3>
            <h2 style="color:#2E86C1;margin:0">{:.0f}/100</h2>
        </div>
        """.format(metrics["performance"]), unsafe_allow_html=True)
        
    with col2:
        st.markdown("""
        <div class="metric-card">
            <h3 style="margin:0">SEO</h3>
            <h2 style="color:#2E86C1;margin:0">{:.0f}/100</h2>
        </div>
        """.format(metrics["seo"]), unsafe_allow_html=True)
        
    with col3:
        st.markdown("""
        <div class="metric-card">
            <h3 style="margin:0">Accessibility</h3>
            <h2 style="color:#2E86C1;margin:0">{:.0f}/100</h2>
        </div>
        """.format(metrics["accessibility"]), unsafe_allow_html=True)
        
    with col4:
        st.markdown("""
        <div class="metric-card">
            <h3 style="margin:0">Best Practices</h3>
            <h2 style="color:#2E86C1;margin:0">{:.0f}/100</h2>
        </div>
        """.format(metrics["best_practices"]), unsafe_allow_html=True)

def display_recommendations(recommendations: Dict[str, List[str]]) -> None:
    """Display recommendations in an organized format with expandable sections."""
    
    if recommendations.get("critical"):
        with st.expander("Critical Issues 🚨", expanded=True):
            for rec in recommendations["critical"]:
                st.markdown(f"- {rec}")
    
    if recommendations.get("important"):
        with st.expander("Important Recommendations ⚠️", expanded=True):
            for rec in recommendations["important"]:
                st.markdown(f"- {rec}")
    
    if recommendations.get("minor"):
        with st.expander("Minor Suggestions 💡", expanded=True):
            for rec in recommendations["minor"]:
                st.markdown(f"- {rec}")

async def analyze_website(url: str, keyword_list: Optional[List[str]] = None) -> Dict:
    """Analyze website using the FastAPI backend."""
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://localhost:8000/analyze",
            json={"url": url, "keywords": keyword_list}
        )
        
        if response.status_code == 200:
            data = response.json()
            task_id = data["task_id"]
            
            # Poll for results
            while True:
                status_response = await client.get(f"http://localhost:8000/status/{task_id}")
                status_data = status_response.json()
                
                if status_data["status"] == "completed":
                    return status_data["results"]
                    
                time.sleep(1)
        else:
            raise Exception(response.text)

def main():
    st.title("AI SEO Buddy 🔍")
    st.markdown("### Your AI-powered SEO analysis tool")
    
    # URL input
    url = st.text_input("Enter the URL to analyze:", placeholder="https://example.com")
    
    # Keywords input
    keywords = st.text_input(
        "Enter target keywords (optional, separate with commas):",
        placeholder="keyword1, keyword2, keyword3"
    )
    
    # Convert keywords string to list
    keyword_list = None
    if keywords:
        keyword_list = [k.strip() for k in keywords.split(",") if k.strip()]
    
    # Analysis button
    if st.button("Analyze"):
        if not url:
            st.error("Please enter a URL to analyze")
            return
            
        try:
            with st.spinner("Analyzing your website..."):
                # Run analysis
                results = asyncio.run(analyze_website(url, keyword_list))
                
                # Display results
                st.success("Analysis completed!")
                
                # Display metrics
                st.header("Performance Metrics")
                display_metrics(results["lighthouse"])
                
                # Display content analysis
                st.header("Content Analysis")
                with st.expander("View Details", expanded=True):
                    st.json(results["analysis"])
                
                # Display recommendations
                st.header("Recommendations")
                display_recommendations(results["recommendations"])
                
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main() 