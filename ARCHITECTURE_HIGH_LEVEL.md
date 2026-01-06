# High-Level Architecture: CDO Monitoring & Oversight - AI-Driven Operational Intelligence

## System Overview

The CDO Monitoring & Oversight system transforms reactive case management reporting into proactive, AI-driven operational intelligence. It analyzes case data to identify risks, patterns, inefficiencies, and provides actionable insights through an interactive web interface.

---

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         USER INTERFACE LAYER                              │
│  ┌───────────────────────────────────────────────────────────────────┐  │
│  │         Streamlit Web Application (pattern_recognition_webapp.py)  │  │
│  │  • CSV Upload Interface                                            │  │
│  │  • Interactive Dashboards                                          │  │
│  │  • Chat Interface (LLM-powered)                                    │  │
│  │  • Visualization Components (Plotly)                                │  │
│  └───────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                        APPLICATION LOGIC LAYER                           │
│  ┌───────────────────────────────────────────────────────────────────┐  │
│  │  AI-Enhanced Analysis Layer                                        │  │
│  │  (pattern_recognition_ai_enhanced.py)                              │  │
│  │  • Azure OpenAI Integration                                        │  │
│  │  • AI-Generated Insights                                           │  │
│  │  • Executive Summaries                                             │  │
│  │  • Risk Analysis & Recommendations                                 │  │
│  └───────────────────────────────────────────────────────────────────┘  │
│                                    │                                      │
│                                    ▼                                      │
│  ┌───────────────────────────────────────────────────────────────────┐  │
│  │  Core Analysis Engine                                             │  │
│  │  (pattern_recognition_analysis.py)                                 │  │
│  │  • KPI Calculation                                                 │  │
│  │  • Pattern Detection                                                │  │
│  │  • Risk Identification                                              │  │
│  │  • Inefficiency Detection                                          │  │
│  │  • Root Cause Analysis                                             │  │
│  └───────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                          DATA PROCESSING LAYER                            │
│  ┌───────────────────────────────────────────────────────────────────┐  │
│  │  Data Preparation & Transformation                                 │  │
│  │  • CSV Parsing (pandas)                                            │  │
│  │  • Date/Time Processing                                            │  │
│  │  • SLA Configuration Loading (SLA_sheet.csv)                        │  │
│  │  • Data Validation & Cleaning                                      │  │
│  │  • Metric Calculation (Resolution Time, Days Open, etc.)           │  │
│  └───────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                          EXTERNAL SERVICES LAYER                          │
│  ┌───────────────────────────────────────────────────────────────────┐  │
│  │  Azure OpenAI Service                                              │  │
│  │  • GPT-4.1-mini-summary Deployment                                 │  │
│  │  • Chat Completions API                                            │  │
│  │  • AI-Generated Insights                                           │  │
│  └───────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                            DATA SOURCES                                   │
│  ┌──────────────────────┐  ┌──────────────────────┐                    │
│  │  Case Data CSV       │  │  SLA Configuration    │                    │
│  │  (DummyData.csv)     │  │  (SLA_sheet.csv)      │                    │
│  │  • Case Details      │  │  • Team SLAs          │                    │
│  │  • Dates & Status    │  │  • Severity Targets   │                    │
│  │  • Assignments       │  │  • TTR Hours           │                    │
│  └──────────────────────┘  └──────────────────────┘                    │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Component Architecture

### 1. **User Interface Layer**

**Technology**: Streamlit

**Components**:
- **Web Application** (`pattern_recognition_webapp.py`)
  - CSV file upload interface
  - Navigation menu (Overview, KPIs, Risks, Patterns, etc.)
  - Interactive dashboards with Plotly visualizations
  - Chat interface for LLM-powered queries
  - Download functionality (JSON, CSV reports)

**Key Features**:
- Microsoft Fluent Design-inspired UI
- Real-time data visualization
- Session state management
- Responsive layout

---

### 2. **Application Logic Layer**

#### 2.1 AI-Enhanced Analysis Module
**File**: `pattern_recognition_ai_enhanced.py`

**Responsibilities**:
- Extends core analysis with AI capabilities
- Integrates with Azure OpenAI API
- Generates executive summaries
- Provides AI-powered risk analysis
- Creates actionable recommendations
- Powers chat interface responses

**Key Methods**:
- `generate_ai_enhanced_report()`: Orchestrates AI analysis
- `generate_executive_summary_ai()`: Creates executive summaries
- `analyze_risks_ai()`: AI-powered risk assessment
- `generate_recommendations_ai()`: Creates recommendations

#### 2.2 Core Analysis Engine
**File**: `pattern_recognition_analysis.py`

**Responsibilities**:
- KPI calculation and analysis
- Pattern detection (temporal, case type, assignment group)
- Risk identification (SLA breaches, high priority, aging cases)
- Inefficiency detection (bottlenecks, recurring issues)
- Root cause analysis
- Correlation analysis

**Key Methods**:
- `analyze_kpis()`: Calculates key performance indicators
- `analyze_patterns()`: Detects patterns in case data
- `analyze_risks()`: Identifies at-risk cases
- `analyze_inefficiencies()`: Finds bottlenecks and recurring issues
- `prepare_data()`: Cleans and prepares data for analysis

---

### 3. **Data Processing Layer**

**Technology**: pandas, NumPy

**Responsibilities**:
- CSV file parsing and validation
- Date/time parsing and normalization
- SLA configuration loading from `SLA_sheet.csv`
- Data cleaning and transformation
- Metric calculation:
  - Resolution Time (End Date - Create Date)
  - Days Open (Current Date - Create Date)
  - SLA Risk Percentage
  - Closure Rate
  - SLA Compliance Rate

**Data Flow**:
1. CSV uploaded via Streamlit
2. Data loaded into pandas DataFrame
3. Dates parsed and normalized
4. SLA targets loaded from `SLA_sheet.csv`
5. Derived metrics calculated
6. Data prepared for analysis

---

### 4. **External Services Layer**

#### Azure OpenAI Integration
**Configuration**: `azure_openai_config.json`

**Services Used**:
- **Chat Completions API**: For AI-generated insights and chat responses
- **Deployment**: `gpt-4.1-mini-summary`

**Integration Points**:
- AI-enhanced report generation
- Chat interface responses
- Executive summary generation
- Risk analysis and recommendations

---

### 5. **Data Sources**

#### Case Data CSV (`DummyData.csv`)
**Required Columns**:
- `Create Date`: Case creation timestamp
- `End Date`: Case closure timestamp (optional)
- `Case Id`: Unique identifier
- `Case Severity`: Severity level (0-4)
- `CaseStatus`: Current status
- `Case Type`: Type/category
- `AssignmentGroup`: Assigned team
- `Case Source`: Source of case
- `Case CurrentSummary`: Description
- `Case Resolution`: Resolution details (optional)

#### SLA Configuration (`SLA_sheet.csv`)
**Required Columns**:
- `Team`: Assignment group name
- `Severity`: Severity level
- `TTR_Hours`: Time to resolve in hours

---

## Data Flow

### Analysis Workflow

```
1. User uploads CSV file
   ↓
2. Streamlit saves file temporarily
   ↓
3. Core Analysis Engine loads and processes data
   ↓
4. SLA configuration loaded from SLA_sheet.csv
   ↓
5. Data prepared (dates parsed, metrics calculated)
   ↓
6. Analysis modules execute:
   - KPI Analysis
   - Pattern Detection
   - Risk Identification
   - Inefficiency Detection
   ↓
7. (If AI enabled) Azure OpenAI generates insights
   ↓
8. Results stored in session state
   ↓
9. UI displays results in interactive dashboards
```

### Chat Workflow

```
1. User asks question via chat interface
   ↓
2. Context prepared from analysis results
   ↓
3. Prompt constructed with data context
   ↓
4. Azure OpenAI API called
   ↓
5. Response generated with precise data citations
   ↓
6. Response displayed to user
```

---

## Technology Stack

### Frontend
- **Streamlit**: Web application framework
- **Plotly**: Interactive visualizations
- **Custom CSS**: Microsoft Fluent Design styling

### Backend
- **Python 3.12+**: Core language
- **pandas**: Data manipulation and analysis
- **NumPy**: Numerical computations

### AI/ML
- **Azure OpenAI**: LLM services (GPT-4.1-mini-summary)
- **OpenAI Python SDK**: API integration

### Data Storage
- **CSV Files**: Case data and SLA configuration
- **Session State**: In-memory storage for Streamlit

---

## Key Design Patterns

### 1. **Layered Architecture**
- Clear separation between UI, application logic, and data processing
- Each layer has distinct responsibilities

### 2. **Inheritance Pattern**
- `AIEnhancedPatternRecognition` extends `CDOPatternRecognition`
- Reuses core analysis while adding AI capabilities

### 3. **Configuration-Driven**
- SLA targets loaded from external CSV
- Azure OpenAI configuration in JSON file
- Easy to modify without code changes

### 4. **Session State Management**
- Streamlit session state preserves analysis results
- Enables navigation without re-analysis

---

## Scalability Considerations

### Current Architecture (Single-User)
- In-memory processing
- Session-based state management
- Suitable for small to medium datasets (<100K cases)

### Future Scalability Options

1. **Database Integration**
   - Replace CSV with database (SQL Server, PostgreSQL)
   - Enable concurrent user access
   - Support larger datasets

2. **Caching Layer**
   - Cache analysis results
   - Reduce recomputation overhead

3. **Microservices Architecture**
   - Separate analysis service
   - Separate AI service
   - API-based communication

4. **Cloud Deployment**
   - Azure App Service for web app
   - Azure Functions for analysis jobs
   - Azure Storage for data files

---

## Security Considerations

### Current Implementation
- API keys stored in JSON file (local)
- No authentication/authorization
- Suitable for internal use

### Recommended Enhancements
- **Azure Key Vault**: Secure API key storage
- **Azure AD Authentication**: User authentication
- **Role-Based Access Control**: Limit access to sensitive data
- **Data Encryption**: Encrypt data at rest and in transit

---

## Deployment Architecture

### Current: Local Development
```
User Machine
├── Python Environment
├── Streamlit Server (localhost:8501)
├── CSV Files (local)
└── Azure OpenAI API (cloud)
```

### Recommended: Production Deployment
```
Azure Cloud
├── Azure App Service (Streamlit Web App)
├── Azure Storage Account (CSV files)
├── Azure Key Vault (API keys)
├── Azure OpenAI Service
└── Azure Application Insights (monitoring)
```

---

## Integration Points

### 1. **Azure OpenAI**
- **Purpose**: AI-powered insights and chat
- **Integration**: REST API via OpenAI Python SDK
- **Configuration**: `azure_openai_config.json`

### 2. **CSV Data Sources**
- **Purpose**: Case data and SLA configuration
- **Integration**: File upload and pandas parsing
- **Format**: Standard CSV with specific column requirements

### 3. **Streamlit Framework**
- **Purpose**: Web UI and user interaction
- **Integration**: Native Python framework
- **Features**: File upload, visualization, session management

---

## Performance Characteristics

### Analysis Performance
- **Small datasets (<1K cases)**: <5 seconds
- **Medium datasets (1K-10K cases)**: 5-30 seconds
- **Large datasets (10K+ cases)**: 30+ seconds

### AI Generation Performance
- **Executive Summary**: 5-10 seconds
- **Risk Analysis**: 5-10 seconds
- **Chat Response**: 2-5 seconds

### Optimization Opportunities
- Parallel processing for large datasets
- Caching of analysis results
- Incremental analysis for updates
- Database indexing for faster queries

---

## Monitoring & Observability

### Current State
- Basic error handling and logging
- Streamlit built-in error messages

### Recommended Enhancements
- **Azure Application Insights**: Application monitoring
- **Logging**: Structured logging (Python logging module)
- **Metrics**: Track analysis performance, API usage
- **Alerts**: Notify on errors or performance degradation

---

## Future Enhancements

1. **Real-Time Analysis**
   - WebSocket connections for live updates
   - Streaming data processing

2. **Advanced AI Features**
   - Multi-agent systems for specialized analysis
   - Predictive analytics for case outcomes
   - Automated root cause detection

3. **Enhanced Visualizations**
   - Interactive drill-down capabilities
   - Custom dashboard creation
   - Export to PowerPoint/PDF

4. **Integration with Case Management Systems**
   - Direct API integration
   - Automated data synchronization
   - Real-time case updates

---

## Summary

The CDO Monitoring & Oversight system follows a **layered, modular architecture** that separates concerns and enables easy extension. The core analysis engine provides robust pattern recognition and risk identification, while the AI-enhanced layer adds intelligent insights and natural language interaction. The Streamlit-based UI provides an intuitive interface for data upload, visualization, and interaction.

The architecture is designed to be:
- **Scalable**: Can be extended to support larger datasets and concurrent users
- **Maintainable**: Clear separation of concerns and modular design
- **Extensible**: Easy to add new analysis modules or integrate with external systems
- **User-Friendly**: Intuitive web interface with interactive visualizations

