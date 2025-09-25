import os
from dotenv import load_dotenv
import yaml
from pyprojroot import here
from openai import OpenAI

print("Environment variables are loaded:", load_dotenv())


class LoadConfig:
    def __init__(self) -> None:
        with open(here("configs/app_config.yml")) as cfg:
            app_config = yaml.load(cfg, Loader=yaml.FullLoader)

        self.load_directories(app_config=app_config)
        self.load_llm_configs(app_config=app_config)
        self.load_database_configs(app_config=app_config)
        self.load_web_search_configs(app_config=app_config)
        self.load_github_models_client()

    def load_directories(self, app_config):
        """Load directory configurations"""
        self.datasets_directory = here(app_config["directories"]["datasets_directory"])
        self.data_directory = here(app_config["directories"]["data_directory"])
        self.heart_disease_db = str(here(app_config["directories"]["heart_disease_db"]))
        self.cancer_db = str(here(app_config["directories"]["cancer_db"]))
        self.diabetes_db = str(here(app_config["directories"]["diabetes_db"]))

    def load_llm_configs(self, app_config):
        """Load LLM configuration settings"""
        self.agent_system_role = app_config["llm_config"]["agent_system_role"]
        self.db_agent_system_role = app_config["llm_config"]["db_agent_system_role"]
        self.web_search_system_role = app_config["llm_config"]["web_search_system_role"]
        self.model_name = app_config["llm_config"]["model_name"]
        self.temperature = app_config["llm_config"]["temperature"]
        self.max_tokens = app_config["llm_config"]["max_tokens"]

    def load_database_configs(self, app_config):
        """Load database configuration settings"""
        self.heart_disease_config = app_config["database_config"]["heart_disease"]
        self.cancer_config = app_config["database_config"]["cancer"]
        self.diabetes_config = app_config["database_config"]["diabetes"]

    def load_web_search_configs(self, app_config):
        """Load web search configuration settings"""
        self.tavily_api_key = os.getenv(app_config["web_search_config"]["tavily_api_key_env"])
        self.max_search_results = app_config["web_search_config"]["max_results"]
        self.search_topic = app_config["web_search_config"]["topic"]

    def load_github_models_client(self):
        """Initialize GitHub Models API client"""
        github_token = os.getenv("GITHUB_TOKEN")
        if not github_token:
            raise ValueError("GITHUB_TOKEN environment variable not set. Please provide a valid GitHub token.")
        
        self.github_client = OpenAI(
            base_url="https://models.inference.ai.azure.com",
            api_key=github_token,
        )
        
        # For LangChain compatibility
        from langchain_openai import ChatOpenAI
        self.langchain_llm = ChatOpenAI(
            model=self.model_name,
            openai_api_key=github_token,
            openai_api_base="https://models.inference.ai.azure.com",
            temperature=self.temperature,
            max_tokens=self.max_tokens
        )