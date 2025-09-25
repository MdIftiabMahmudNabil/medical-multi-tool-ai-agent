from typing import List, Tuple
from langchain.agents import create_openai_functions_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents.agent_types import AgentType
from tools.database_tools import heart_disease_db_tool, cancer_db_tool, diabetes_db_tool
from tools.web_search_tools import medical_web_search_tool, simple_medical_search_tool
from utils.load_config import LoadConfig

class MedicalAIAgent:
    """
    Main AI Agent using OpenAI Agent SDK + LangChain Agent Executor.
    Routes queries intelligently:
    🧠 Statistics/data/numbers → Database tools
    🌐 Definitions/symptoms/cures → Web search tools
    """
    
    def __init__(self):
        self.config = LoadConfig()
        self.tools = self._setup_tools()
        self.agent_executor = self._setup_agent()
    
    def _setup_tools(self):
        """Set up all available tools for the agent"""
        tools = [
            heart_disease_db_tool,
            cancer_db_tool, 
            diabetes_db_tool,
            medical_web_search_tool,
            simple_medical_search_tool
        ]
        return tools
    
    def _setup_agent(self):
        """Set up the LangChain agent executor"""
        try:
            # Create the prompt template following learning materials pattern
            prompt = ChatPromptTemplate.from_messages([
                ("system", self.config.agent_system_role + """
                
                INTELLIGENT ROUTING RULES:
                
                🧠 Use DATABASE TOOLS when questions are about STATISTICS, DATA, or NUMBERS:
                - "What is the average age..."
                - "How many patients..."
                - "Show me statistics..."
                - "Count of cases..."
                - "Percentage of..."
                - Any numerical analysis of patient data
                
                Database Selection:
                - Heart disease queries → heart_disease_db_tool
                - Cancer queries → cancer_db_tool  
                - Diabetes queries → diabetes_db_tool
                
                🌐 Use WEB SEARCH TOOLS when questions are about DEFINITIONS, SYMPTOMS, or CURES:
                - "What is [medical condition]..."
                - "What are the symptoms of..."
                - "How is [condition] treated..."
                - "What causes..."
                - "How to prevent..."
                - General medical knowledge
                
                CRITICAL: Analyze the question type first, then route accordingly.
                """),
                ("user", "{input}"),
                MessagesPlaceholder(variable_name="agent_scratchpad"),
            ])
            
            # Create the agent
            agent = create_openai_functions_agent(
                llm=self.config.langchain_llm,
                tools=self.tools,
                prompt=prompt
            )
            
            # Create agent executor
            agent_executor = AgentExecutor(
                agent=agent,
                tools=self.tools,
                verbose=True,
                handle_parsing_errors=True,
                max_iterations=5,
                return_intermediate_steps=True
            )
            
            return agent_executor
            
        except Exception as e:
            print(f"Error setting up agent: {str(e)}")
            return None
    
    def query(self, user_input: str) -> str:
        """
        Process user query using OpenAI Agent SDK + LangChain Agent Executor
        
        Args:
            user_input: User's medical question or query
            
        Returns:
            AI agent's response using the most appropriate tool
        """
        try:
            if not self.agent_executor:
                return "❌ Agent not properly initialized. Please check your configuration."
            
            # Use OpenAI Agent SDK + LangChain for intelligent routing
            response = self.agent_executor.invoke({
                "input": user_input
            })
            
            return response.get("output", "No response generated")
            
        except Exception as e:
            error_msg = str(e)
            if "max iterations" in error_msg.lower() or "agent stopped" in error_msg.lower():
                # Fallback to direct routing if agent gets stuck
                return self._fallback_routing(user_input)
            return f"❌ Error processing query: {error_msg}"
    
    def _fallback_routing(self, user_input: str) -> str:
        """Fallback routing when OpenAI Agent gets stuck (direct tool calls)"""
        try:
            user_lower = user_input.lower()
            
            # Check for database query indicators
            database_indicators = ["average", "mean", "count", "how many", "statistics", "data", "records", "patients"]
            is_database_query = any(indicator in user_lower for indicator in database_indicators)
            
            if is_database_query:
                # Route to specific database based on medical domain
                if any(word in user_lower for word in ["heart", "cardiac", "coronary"]):
                    return heart_disease_db_tool.invoke({"query": user_input})
                
                elif any(word in user_lower for word in ["cancer", "tumor", "malignant", "benign"]):
                    return cancer_db_tool.invoke({"query": user_input})
                
                elif any(word in user_lower for word in ["diabetes", "glucose", "insulin", "blood sugar"]):
                    return diabetes_db_tool.invoke({"query": user_input})
                
                else:
                    # Default to heart disease if domain unclear
                    return heart_disease_db_tool.invoke({"query": user_input})
            
            # Web search for definitions, symptoms, treatments
            else:
                try:
                    return medical_web_search_tool.invoke({"query": user_input})
                except:
                    return simple_medical_search_tool.invoke({"query": user_input})
                
        except Exception as e:
            return f"❌ Fallback routing failed: {str(e)}"
    
    def get_available_tools_info(self) -> str:
        """Return information about available tools"""
        info = """🛠️ **Available Medical AI Tools:**

**📊 Database Tools:**
• 🫀 **Heart Disease DB** - Statistics and data about heart disease patients
• 🎗️ **Cancer DB** - Cancer diagnosis and tumor characteristic data  
• 🩺 **Diabetes DB** - Diabetes patient health metrics and risk factors

**🌐 Web Search Tools:**
• 🔍 **Medical Web Search** - General medical information, definitions, symptoms, treatments
• 📚 **Simple Medical Search** - Fallback tool for basic medical information

**💡 Example Queries:**

*Database queries (for statistics):*
- "What is the average age of heart disease patients?"
- "How many cancer cases are in the dataset?"
- "Show me diabetes statistics by age group"

*Web search queries (for general knowledge):*
- "What are the symptoms of type 2 diabetes?"
- "How is coronary heart disease treated?"
- "What causes breast cancer?"
"""
        return info