import os
from langchain_core.tools import tool
from tavily import TavilyClient
from utils.load_config import LoadConfig

# Load configuration
APPCFG = LoadConfig()


class MedicalWebSearchTool:
    """Medical Web Search Tool using Tavily API for general medical knowledge"""
    
    def __init__(self):
        self.tavily_client = self._setup_tavily()
    
    def _setup_tavily(self):
        """Initialize Tavily client if API key is available"""
        if APPCFG.tavily_api_key:
            try:
                return TavilyClient(api_key=APPCFG.tavily_api_key)
            except Exception as e:
                print(f"Failed to initialize Tavily client: {e}")
                return None
        return None
    
    def search(self, query: str) -> str:
        """Search for general medical knowledge, definitions, symptoms, treatments"""
        if not self.tavily_client:
            return self._fallback_search(query)
        
        try:
            # Perform medical-focused search
            search_results = self.tavily_client.search(
                query=f"medical health {query}",
                search_depth="advanced",
                max_results=APPCFG.max_search_results,
                topic="health"
            )
            
            if not search_results.get('results'):
                return f"🔍 No web search results found for: {query}"
            
            # Format results
            formatted_results = "🌐 **Medical Web Search Results**:\n\n"
            
            for i, result in enumerate(search_results['results'][:APPCFG.max_search_results], 1):
                title = result.get('title', 'No title')
                content = result.get('content', 'No content available')
                url = result.get('url', '')
                
                formatted_results += f"**{i}. {title}**\n"
                formatted_results += f"{content}\n"
                if url:
                    formatted_results += f"*Source: {url}*\n"
                formatted_results += "\n"
            
            # Add medical disclaimer
            formatted_results += "⚠️ **Medical Disclaimer**: This information is for educational purposes only. Always consult healthcare professionals for medical advice."
            
            return formatted_results
            
        except Exception as e:
            return self._fallback_search(query)
    
    def _fallback_search(self, query: str) -> str:
        """Fallback search when Tavily is unavailable"""
        common_responses = {
            "heart disease": "Heart disease refers to several types of heart conditions including coronary artery disease, arrhythmias, and heart defects. Common symptoms include chest pain, shortness of breath, and fatigue.",
            "diabetes": "Diabetes is a group of metabolic disorders characterized by high blood sugar levels. Type 1 and Type 2 are the most common forms. Symptoms include increased thirst, frequent urination, and fatigue.",
            "cancer": "Cancer is a group of diseases involving abnormal cell growth with potential to invade other parts of the body. Early detection and treatment are crucial for better outcomes.",
            "symptoms": "Medical symptoms are subjective experiences that indicate the presence of disease or injury. Always consult healthcare professionals for proper diagnosis.",
            "treatment": "Medical treatments vary depending on the condition and should always be prescribed and supervised by qualified healthcare professionals."
        }
        
        query_lower = query.lower()
        
        for key, response in common_responses.items():
            if key in query_lower:
                return f"🩺 **Medical Information**: {response}\n\n⚠️ **Disclaimer**: This is general information only. Consult healthcare professionals for specific medical advice."
        
        return f"🔍 For detailed information about '{query}', please consult medical literature or healthcare professionals. This tool provides general information only.\n\n⚠️ **Disclaimer**: Always seek professional medical advice for health concerns."


# Create tool instance
medical_web_search_tool_instance = MedicalWebSearchTool()


@tool
def medical_web_search_tool(query: str) -> str:
    """Search the web for general medical information, definitions, symptoms, treatments, and cures.
    
    Use this tool for questions about:
    - Medical definitions and terminology
    - Disease symptoms and signs
    - Treatment options and medications
    - General health information
    - Medical procedures and tests
    - Prevention strategies
    
    Do NOT use this tool for:
    - Statistics from specific datasets
    - Numerical data analysis
    - Patient-specific data queries
    
    Args:
        query: Natural language question about general medical topics
        
    Returns:
        Comprehensive medical information from web sources
    """
    return medical_web_search_tool_instance.search(query)


@tool  
def simple_medical_search_tool(query: str) -> str:
    """Simple medical information search tool (fallback when Tavily is unavailable).
    
    Args:
        query: Medical question or topic to search for
        
    Returns:
        Basic medical information response
    """
    return medical_web_search_tool_instance._fallback_search(query)