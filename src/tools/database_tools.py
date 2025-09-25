import os
from langchain_core.tools import tool
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import create_sql_agent
from langchain.agents.agent_types import AgentType
from utils.load_config import LoadConfig

# Load configuration
APPCFG = LoadConfig()


class HeartDiseaseDBTool:
    """Heart Disease Database Tool using OpenAI Agent SDK + LangChain Agent"""
    
    def __init__(self):
        self.db_path = APPCFG.heart_disease_db
        self.agent = self._create_agent()
    
    def _create_agent(self):
        """Create SQL agent for heart disease database"""
        if not os.path.exists(self.db_path):
            return None
        
        db = SQLDatabase.from_uri(f"sqlite:///{self.db_path}")
        
        agent = create_sql_agent(
            llm=APPCFG.langchain_llm,
            db=db,
            agent_type=AgentType.OPENAI_FUNCTIONS,
            verbose=False,
            handle_parsing_errors=True,
            max_iterations=10,
            early_stopping_method="force"
        )
        return agent
    
    def query(self, question: str) -> str:
        """Execute user question via SQL and return natural language result"""
        if not self.agent:
            return "❌ Heart disease database not found. Please run database setup first."
        
        try:
            response = self.agent.invoke({"input": f"Answer this question about heart disease data: {question}"})
            return f"🫀 **Heart Disease Data**: {response.get('output', 'No response generated')}"
        except Exception as e:
            return f"❌ Error querying heart disease database: {str(e)}"


class CancerDBTool:
    """Cancer Database Tool using OpenAI Agent SDK + LangChain Agent"""
    
    def __init__(self):
        self.db_path = APPCFG.cancer_db
        self.agent = self._create_agent()
    
    def _create_agent(self):
        """Create SQL agent for cancer database"""
        if not os.path.exists(self.db_path):
            return None
        
        db = SQLDatabase.from_uri(f"sqlite:///{self.db_path}")
        
        agent = create_sql_agent(
            llm=APPCFG.langchain_llm,
            db=db,
            agent_type=AgentType.OPENAI_FUNCTIONS,
            verbose=False,
            handle_parsing_errors=True,
            max_iterations=10,
            early_stopping_method="force"
        )
        return agent
    
    def query(self, question: str) -> str:
        """Execute user question via SQL and return natural language result"""
        if not self.agent:
            return "❌ Cancer database not found. Please run database setup first."
        
        try:
            response = self.agent.invoke({"input": f"Answer this question about cancer data: {question}"})
            return f"🎗️ **Cancer Data**: {response.get('output', 'No response generated')}"
        except Exception as e:
            return f"❌ Error querying cancer database: {str(e)}"


class DiabetesDBTool:
    """Diabetes Database Tool using OpenAI Agent SDK + LangChain Agent"""
    
    def __init__(self):
        self.db_path = APPCFG.diabetes_db
        self.agent = self._create_agent()
    
    def _create_agent(self):
        """Create SQL agent for diabetes database"""
        if not os.path.exists(self.db_path):
            return None
        
        db = SQLDatabase.from_uri(f"sqlite:///{self.db_path}")
        
        agent = create_sql_agent(
            llm=APPCFG.langchain_llm,
            db=db,
            agent_type=AgentType.OPENAI_FUNCTIONS,
            verbose=False,
            handle_parsing_errors=True,
            max_iterations=10,
            early_stopping_method="force"
        )
        return agent
    
    def query(self, question: str) -> str:
        """Execute user question via SQL and return natural language result"""
        if not self.agent:
            return "❌ Diabetes database not found. Please run database setup first."
        
        try:
            response = self.agent.invoke({"input": f"Answer this question about diabetes data: {question}"})
            return f"🩺 **Diabetes Data**: {response.get('output', 'No response generated')}"
        except Exception as e:
            return f"❌ Error querying diabetes database: {str(e)}"


# Create tool instances for easy access
heart_disease_tool = HeartDiseaseDBTool()
cancer_tool = CancerDBTool()
diabetes_tool = DiabetesDBTool()


# LangChain tool wrappers for agent integration
@tool
def heart_disease_db_tool(query: str) -> str:
    """Query the heart disease database for statistics and information about heart disease patients.
    
    Use this tool for questions about:
    - Heart disease statistics
    - Patient demographics with heart conditions
    - Risk factors for heart disease
    - Heart disease prediction data
    
    Args:
        query: Natural language question about heart disease data
        
    Returns:
        Natural language answer based on the database query results
    """
    return heart_disease_tool.query(query)


@tool 
def cancer_db_tool(query: str) -> str:
    """Query the cancer database for statistics and information about cancer patients and diagnoses.
    
    Use this tool for questions about:
    - Cancer statistics and prevalence
    - Tumor characteristics and features
    - Cancer diagnosis data
    - Patient demographics with cancer
    
    Args:
        query: Natural language question about cancer data
        
    Returns:
        Natural language answer based on the database query results
    """
    return cancer_tool.query(query)


@tool
def diabetes_db_tool(query: str) -> str:
    """Query the diabetes database for statistics and information about diabetes patients.
    
    Use this tool for questions about:
    - Diabetes statistics and prevalence 
    - Patient health metrics related to diabetes
    - Diabetes risk factors and indicators
    - Blood sugar and health measurements
    
    Args:
        query: Natural language question about diabetes data
        
    Returns:
        Natural language answer based on the database query results
    """
    return diabetes_tool.query(query)