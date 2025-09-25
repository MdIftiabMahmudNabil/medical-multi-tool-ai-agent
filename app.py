import streamlit as st
import os
import sys
from pathlib import Path

# Add src directory to Python path for imports
src_path = Path(__file__).parent / "src"
sys.path.append(str(src_path))

try:
    from medical_agent import MedicalAIAgent
    from prepare_databases import DatabaseSetup
except ImportError as e:
    st.error(f"Import error: {e}")
    st.error("Please make sure all dependencies are installed: pip install -r requirements.txt")
    st.stop()

def main():
    # Page configuration
    st.set_page_config(
        page_title="🧑‍⚕️ Medical Multi-Tool AI Agent",
        page_icon="🏥",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Main title and description
    st.title("🧑‍⚕️ Medical Multi-Tool AI Agent")
    st.markdown("""
    **Powered by LangChain + Streamlit + GitHub Models API**
    
    This AI agent can answer questions about medical datasets and provide general medical information using:
    - 📊 **Database Tools** for medical dataset statistics 
    - 🌐 **Web Search Tools** for general medical knowledge
    """)
    
    # Sidebar for configuration and setup
    with st.sidebar:
        st.header("🔧 Configuration")
        
        # API Key status
        github_token = os.getenv("GITHUB_TOKEN")
        tavily_key = os.getenv("TAVILY_API_KEY")
        
        if github_token:
            st.success("✅ GitHub Token configured")
        else:
            st.error("❌ GitHub Token not found")
            st.code("export GITHUB_TOKEN='your_token_here'")
        
        if tavily_key:
            st.success("✅ Tavily API Key configured") 
        else:
            st.warning("⚠️ Tavily API Key not found (web search limited)")
            st.code("export TAVILY_API_KEY='your_key_here'")
        
        st.markdown("---")
        
        # Database setup section
        st.header("🏗️ Database Setup")
        
        if st.button("🔄 Setup/Refresh Databases", type="primary"):
            with st.spinner("Setting up medical databases..."):
                try:
                    db_setup = DatabaseSetup()
                    results = db_setup.setup_all_databases()
                    
                    for db_name, success in results.items():
                        if success:
                            st.success(f"✅ {db_name.replace('_', ' ').title()} DB ready")
                        else:
                            st.error(f"❌ {db_name.replace('_', ' ').title()} DB failed")
                            
                except Exception as e:
                    st.error(f"Database setup error: {str(e)}")
        
        st.markdown("---")
        
        # Help section
        st.header("💡 Example Queries")
        
        st.markdown("**📊 Database Queries:**")
        st.code("""
• "Average age of heart disease patients?"
• "How many diabetes cases in dataset?"
• "Cancer statistics by tumor size?"
        """)
        
        st.markdown("**🌐 Web Search Queries:**")
        st.code("""
• "What are symptoms of diabetes?"
• "How is heart disease treated?"
• "What causes lung cancer?"
        """)
    
    # Main chat interface
    st.header("💬 Ask Your Medical Question")
    
    # Initialize session state for chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []
        # Add welcome message
        st.session_state.messages.append({
            "role": "assistant", 
            "content": "👋 Hello! I'm your Medical AI Assistant. I can help you with:\n\n📊 **Medical dataset statistics** (heart disease, cancer, diabetes)\n🌐 **General medical information** (symptoms, treatments, definitions)\n\nWhat would you like to know?"
        })
    
    # Initialize agent
    if "agent" not in st.session_state:
        if github_token:
            try:
                with st.spinner("Initializing AI Agent..."):
                    st.session_state.agent = MedicalAIAgent()
                st.success("🤖 AI Agent ready!")
            except Exception as e:
                st.error(f"Failed to initialize agent: {str(e)}")
                st.session_state.agent = None
        else:
            st.session_state.agent = None
    
    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Ask about medical data or general health information..."):
        
        # Check if agent is available
        if not st.session_state.agent:
            st.error("❌ AI Agent not available. Please configure your GitHub Token and refresh the page.")
            return
        
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Generate and display assistant response
        with st.chat_message("assistant"):
            with st.spinner("🤔 Thinking..."):
                try:
                    response = st.session_state.agent.query(prompt)
                    st.markdown(response)
                    
                    # Add to chat history
                    st.session_state.messages.append({
                        "role": "assistant", 
                        "content": response
                    })
                    
                except Exception as e:
                    error_msg = f"❌ Error processing query: {str(e)}"
                    st.error(error_msg)
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": error_msg
                    })
    
    # Footer with tool information
    with st.expander("🛠️ Available Tools Information"):
        if st.session_state.get("agent"):
            st.markdown(st.session_state.agent.get_available_tools_info())
        else:
            st.info("Agent not initialized. Please configure API keys.")
    
    # Clear chat button
    if st.button("🗑️ Clear Chat History"):
        st.session_state.messages = []
        st.rerun()


if __name__ == "__main__":
    main()