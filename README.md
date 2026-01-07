# AI Agent for Operational Excellence

AI-driven operational intelligence system for transforming reactive case management reporting into proactive insights.

## Quick Start

1. **Install Dependencies**
   ```bash
   pip install -r requirements_pattern_analysis.txt
   ```

2. **Configure Azure OpenAI**
   - Copy `azure_openai_config.json.example` to `azure_openai_config.json`
   - Update with your Azure OpenAI endpoint, API key, and deployment name

3. **Run the Web Application**
   ```bash
   # Windows
   start_webapp.bat
   
   # Or manually
   python -m streamlit run pattern_recognition_webapp.py
   ```

4. **Upload Your Data**
   - Upload a CSV file with case data through the web interface
   - Ensure `SLA_sheet.csv` is in the same directory for SLA configuration

## Configuration

### Azure OpenAI Setup

1. Create `azure_openai_config.json` from the example file:
   ```bash
   cp azure_openai_config.json.example azure_openai_config.json
   ```

2. Fill in your Azure OpenAI credentials:
   - `endpoint`: Your Azure OpenAI resource endpoint
   - `api_key`: Your API key
   - `deployment_name`: Your model deployment name

### SLA Configuration

The system uses `SLA_sheet.csv` for SLA targets. The file should contain:
- `Team`: Assignment group name
- `Severity`: Severity level
- `TTR_Hours`: Time to resolve in hours

## Features

- **KPI Analysis**: Case volumes, closure rates, SLA compliance
- **Pattern Detection**: Temporal patterns, case type trends, assignment group analysis
- **Risk Identification**: SLA at-risk cases, high priority open cases, aging cases
- **Inefficiency Detection**: Bottlenecks, recurring issues, process gaps
- **AI-Enhanced Insights**: Natural language insights and recommendations
- **Interactive Chat**: Ask questions about your data and get precise, data-driven answers

## Project Structure

```
pattern_recognition/
├── pattern_recognition_analysis.py      # Core analysis engine
├── pattern_recognition_ai_enhanced.py    # AI-enhanced analysis
├── pattern_recognition_webapp.py         # Streamlit web application
├── azure_openai_config.json             # Azure OpenAI configuration (not in repo)
├── SLA_sheet.csv                        # SLA configuration
├── DummyData.csv                        # Sample data
└── requirements_pattern_analysis.txt     # Python dependencies
```

## Documentation

See `ARCHITECTURE_HIGH_LEVEL.md` for detailed architecture documentation.

## Security Note

**Never commit `azure_openai_config.json` to version control.** This file contains sensitive API keys and should be kept local or stored securely.

