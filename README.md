# 🏥 Multi-Tool AI Agent for Medical Datasets

**A comprehensive AI agent system that intelligently analyzes medical datasets and provides web-based medical knowledge using LangChain, Streamlit, and GitHub Models API.**

## 🎯 Overview

This project implements a **Multi-Tool OpenAI Agent** that can:
- 📊 **Answer data-specific queries** from three medical datasets (Heart Disease, Cancer, Diabetes)
- 🌐 **Use Web Search Tool** for general medical knowledge (definitions, symptoms, cures)
- � **Intelligently route queries** to the appropriate tool based on question type
- 💬 **Interactive chat interface** via Streamlit web application

## 🚀 Quick Start

### 1. Clone & Setup
```bash
git clone <your-repo-url>
cd "Medical Multi-Tool AI Agent"
pip install -r requirements.txt
```

### 2. Configure API Keys
Create a `.env` file:
```env
GITHUB_API_KEY=your_github_models_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here
```

### 3. Setup Databases (One-time)
```bash
python src/prepare_databases.py
```

### 4. Launch Application
```bash
streamlit run app.py
```
🌐 **Access at:** `http://localhost:8501`

## 📁 Project Structure

```
Medical Multi-Tool AI Agent/
├── 📱 app.py                           # Streamlit web interface
├── 📋 requirements.txt                 # Python dependencies  
├── 🔐 .env                            # API keys (not in repo)
├── 📊 configs/
│   └── app_config.yml                 # Application configuration
├── 🧠 src/
│   ├── medical_agent.py               # 🤖 Main AI Agent (OpenAI SDK + LangChain)
│   ├── prepare_databases.py           # 🛠️ Database creation from CSVs
│   ├── 🔧 tools/
│   │   ├── database_tools.py          # 📊 HeartDiseaseDBTool, CancerDBTool, DiabetesDBTool
│   │   └── web_search_tools.py        # 🌐 MedicalWebSearchTool (Tavily API)
│   └── ⚙️ utils/
│       └── load_config.py             # Configuration management
├── 📊 data/
│   ├── heart_disease.db               # ❤️ 1,025 heart disease records
│   ├── cancer.db                      # 🎗️ 1,500 cancer records
│   ├── diabetes.db                    # 🩺 768 diabetes records
│   ├── heart.csv                      # Source data
│   ├── diabetes.csv                   # Source data  
│   └── The_Cancer_data_1500_V2.csv    # Source data
├── 🚀 Deployment Files/
│   ├── .streamlit/config.toml         # Streamlit production config
│   ├── Dockerfile                     # Docker deployment (optional)
│   ├── runtime.txt                    # Python version for deployment
│   └── .gitignore                     # Git ignore rules
└── 📚 Documentation/
    └── README.md                      # This file
```

### 3. Configuration

Set up your API keys:

```bash
# Copy environment template
cp .env.example .env

# Edit .env file with your keys
GITHUB_TOKEN=your_github_token_here
TAVILY_API_KEY=your_tavily_api_key_here  # Optional
```

### 4. Setup Databases

Convert CSV datasets to SQLite databases:

```bash
cd src
python prepare_databases.py
```

Expected output:
```
🏥 Setting up medical databases...
==================================================
Loaded heart disease data with X records and Y columns
✅ Heart disease database created successfully
...
📊 Database setup complete: 3/3 successful
🎉 All databases created successfully!
```

### 5. Launch the Application

```bash
streamlit run app.py
```

The application will open in your browser at `http://localhost:8501`

## 📊 Medical Datasets

The agent works with three medical datasets:

### 🫀 Heart Disease Dataset (`Datasets/heart.csv`)
- Patient demographics and heart disease indicators
- Features: age, sex, chest pain type, blood pressure, cholesterol, etc.
- Target: heart disease presence/absence

### 🎗️ Cancer Dataset (`Datasets/The_Cancer_data_1500_V2.csv`) 
- Tumor characteristics for cancer diagnosis
- Features: tumor size, texture, perimeter, area, smoothness, etc.
- Target: benign/malignant classification

### 🩺 Diabetes Dataset (`Datasets/diabetes.csv`)
- Patient health metrics for diabetes prediction
- Features: glucose levels, BMI, insulin, age, etc.
- Target: diabetes presence/absence

## 💡 Usage Examples

### 📊 Database Queries (Statistics & Data Analysis)

```
"What is the average age of patients with heart disease?"
"How many cancer cases are classified as malignant?"
"Show me diabetes statistics grouped by age ranges"
"What's the correlation between BMI and diabetes in the dataset?"
"How many heart disease patients are over 60 years old?"
```

### 🌐 Web Search Queries (General Medical Knowledge)

```  
"What are the early symptoms of type 2 diabetes?"
"How is coronary heart disease typically treated?"
"What are the main risk factors for breast cancer?"
"What lifestyle changes help prevent heart disease?"
"What medications are used for diabetes management?"
```

## 🛠️ Features

### 🤖 Intelligent Query Routing
The agent automatically determines whether to:
- Query medical databases for statistics and data analysis
- Search the web for general medical knowledge and definitions

### 📊 Database Tools
- **Heart Disease DB Tool**: Query heart disease patient data
- **Cancer DB Tool**: Analyze cancer diagnosis and tumor data  
- **Diabetes DB Tool**: Explore diabetes patient health metrics

### 🌐 Web Search Tools  
- **Medical Web Search**: Advanced web search using Tavily API
- **Simple Medical Search**: Fallback tool with basic medical information

### 💬 Interactive Interface
- Real-time chat interface built with Streamlit
- Chat history and conversation context
- Tool usage indicators
- Configuration status monitoring

## ⚙️ Configuration

### GitHub Models API Setup

1. Get your GitHub token with Models API access
2. Set the `GITHUB_TOKEN` environment variable
3. The agent uses `gpt-4` model by default (configurable in `configs/app_config.yml`)

### Tavily Search API Setup (Optional)

1. Sign up at [tavily.com](https://tavily.com) for a free API key
2. Set the `TAVILY_API_KEY` environment variable  
3. Enables enhanced web search capabilities

### Configuration File (`configs/app_config.yml`)

```yaml
llm_config:
  model_name: "gpt-4"          # GitHub Models API model
  temperature: 0.1             # Response creativity (0.0-1.0)
  max_tokens: 1000            # Maximum response length

database_config:
  heart_disease:
    table_name: "heart_disease_data"
  cancer:
    table_name: "cancer_data"  
  diabetes:
    table_name: "diabetes_data"

web_search_config:
  max_results: 5              # Number of search results
  topic: "health"             # Search focus area
```

## 🔧 Development

### Project Structure

- **`src/tools/`**: LangChain tool implementations
- **`src/utils/`**: Configuration and utility functions  
- **`src/medical_agent.py`**: Main agent orchestration
- **`app.py`**: Streamlit web interface
- **`configs/`**: YAML configuration files

### Adding New Tools

1. Create tool function with `@tool` decorator
2. Add comprehensive docstring with usage guidelines
3. Register tool in `MedicalAIAgent._setup_tools()`
4. Update routing logic if needed

### Database Management

- SQLite databases are created in `data/` directory
- CSV files should be placed in `../Datasets/` directory
- Run `prepare_databases.py` to refresh databases

## 🚨 Important Notes

### Medical Disclaimer
⚠️ **This tool is for educational and research purposes only. Always consult qualified healthcare professionals for medical advice, diagnosis, or treatment.**

### API Rate Limits
- GitHub Models API: Check your usage limits
- Tavily API: Free tier has monthly limits
- Implement caching for production use

### Data Privacy
- No patient data is transmitted to external APIs
- Database queries are processed locally
- Only general medical topics are searched online

## 🐛 Troubleshooting

### Common Issues

**Import Errors**: 
```bash
pip install -r requirements.txt
```

**Database Not Found**: 
```bash
cd src && python prepare_databases.py
```

**GitHub Token Error**:
```bash
export GITHUB_TOKEN="your_token_here"
```

**Streamlit Issues**:
```bash
streamlit run app.py --server.port 8501
```

### Debug Mode

Enable verbose logging by setting `verbose=True` in agent configuration.

## 📚 Dependencies

Key libraries used:
- `streamlit`: Web interface
- `langchain`: AI agent framework
- `langchain-openai`: GitHub Models integration
- `pandas`: Data manipulation
- `sqlite3`: Database operations  
- `tavily-python`: Web search API
- `python-dotenv`: Environment management

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Follow the existing code patterns
4. Add comprehensive tests
5. Submit a pull request

## 📄 License

This project is for educational purposes. Please respect API terms of service and medical information guidelines.

---

**Built with ❤️ using LangChain, Streamlit, and GitHub Models API**