# Streamlit UI & Results Guide

## Overview

The AI Agent for Operational Excellence provides an interactive web interface built with Streamlit. This guide explains how to navigate the UI and interpret the analysis results.

---

## Getting Started

### Launching the Application

1. **Windows**: Double-click `start_webapp.bat`
2. **Manual**: Run `python -m streamlit run pattern_recognition_webapp.py`
3. The application opens in your browser at `http://localhost:8501`

### Initial Setup

1. **Upload CSV File**: Click "Upload CSV" in the sidebar and select your case data file
2. **Enable AI** (Optional): Check "AI Enhancements" in the sidebar for AI-powered insights
3. **Wait for Analysis**: The system processes your data (typically 5-30 seconds)

---

## Navigation Menu

The left sidebar contains the main navigation:

- **Overview**: Executive summary with key metrics
- **KPIs**: Detailed performance indicators
- **Risks**: Risk analysis and at-risk cases
- **Patterns**: Pattern detection and trends
- **Inefficiencies**: Bottlenecks and recurring issues
- **Recommendations**: Actionable recommendations
- **AI Insights**: AI-generated summaries (if AI enabled)
- **Chat**: Interactive Q&A about your data (if AI enabled)
- **Downloads**: Export results as JSON or CSV

---

## Understanding the Results

### 1. Overview Page

**Purpose**: High-level summary of your case management performance

**Key Metrics Displayed**:

- **Total Cases**: Total number of cases in your dataset
  - *Source*: Count of all rows in your CSV
  - *What it means*: Overall case volume

- **Closure Rate**: Percentage of cases that have been closed
  - *Formula*: (Closed Cases / Total Cases) × 100
  - *Source*: Cases where `CaseStatus` = "Closed"
  - *Target*: Typically 80%+ is considered good
  - *What it means*: How well you're resolving cases

- **SLA Compliance**: Percentage of closed cases resolved within SLA deadline
  - *Formula*: (Cases Resolved Within SLA / Total Closed Cases) × 100
  - *Source*: Compares `Resolution Time` to SLA targets from `SLA_sheet.csv`
  - *Target*: 80%+ compliance is standard
  - *What it means*: How well you're meeting service level agreements

- **High Priority Open**: Number of Critical (0) and High (1) severity cases still open
  - *Source*: Cases where `Case Severity` ≤ 1 AND `CaseStatus` ≠ "Closed"
  - *What it means*: Urgent cases requiring immediate attention

- **SLA At Risk**: Number of open cases at 75%+ of their SLA deadline
  - *Calculation*: (Days Open / SLA Target Days) × 100 ≥ 75%
  - *Source*: Compares time since case creation to severity-based SLA target
  - *What it means*: Cases likely to breach SLA if not addressed soon

**How to Use**:
- Click the "About" expander for detailed explanations
- Use this page for executive presentations
- Monitor these metrics over time to track improvements

---

### 2. KPIs Page

**Purpose**: Detailed performance indicators with visualizations

**Components**:

#### Cases by Severity (Pie Chart)
- **What it shows**: Distribution of cases across severity levels
- **Source**: Counts cases grouped by `Case Severity` column
- **Interpretation**: 
  - High percentage of Critical/High = urgent workload
  - Balanced distribution = normal operations

#### Cases by Status (Bar Chart)
- **What it shows**: Distribution of cases across different statuses
- **Source**: Counts cases grouped by `CaseStatus` column
- **Common statuses**: Draft, Analysis, Contain, Eradicate, Review, Recover, Closed
- **Interpretation**:
  - Many in "Analysis" = investigation phase bottleneck
  - Many in "Draft" = cases not being actively worked

#### Resolution Time Metrics
- **Average Resolution Time**: Mean time to resolve closed cases
  - *Formula*: Sum of (End Date - Create Date) for all closed cases / Number of closed cases
  - *Source*: Calculated from `End Date` and `Create Date` columns
  - *What it means*: Typical time to close a case

- **Median Resolution Time**: Middle value when resolution times are sorted
  - *What it means*: More robust to outliers than average; 50% of cases resolved faster, 50% slower

#### Cases by Type (Table)
- **What it shows**: Top 10 case types by frequency
- **Source**: Count of cases grouped by `Case Type` column
- **Interpretation**: 
  - High frequency types = recurring issues
  - May indicate need for preventive measures

#### Cases by Assignment Group (Table)
- **What it shows**: Workload distribution across teams
- **Source**: Count of cases grouped by `AssignmentGroup` column
- **Interpretation**:
  - Uneven distribution = workload imbalance
  - High counts = teams that may need additional resources

**How to Use**:
- Identify teams with high workload
- Find case types that occur frequently
- Track resolution times to identify slow areas

---

### 3. Risks Page

**Purpose**: Identify cases that need immediate attention

**Components**:

#### Cases at Risk of SLA Breach
- **What it shows**: Open cases at 75%+ of their SLA deadline
- **Calculation**: (Days Open / SLA Target Days) × 100 ≥ 75%
- **Display**: Table with case details including:
  - Case ID
  - Assignment Group
  - Case Type
  - Severity
  - Days Open
  - SLA Risk Percentage
- **Action Required**: Prioritize these cases to prevent SLA breaches

#### High Priority Open Cases
- **What it shows**: Critical (0) and High (1) severity cases still open
- **Source**: Cases where `Case Severity` ≤ 1 AND `CaseStatus` ≠ "Closed"
- **Display**: Table with case details
- **Action Required**: Immediate attention needed due to severity

#### Aging Cases (>30 days)
- **What it shows**: Cases open for more than 30 days
- **Calculation**: Current Date - Create Date > 30 days
- **Source**: Calculated from `Create Date` column
- **Interpretation**: 
  - Indicates potential process bottlenecks
  - May suggest resource constraints
- **Action Required**: Review and escalate if necessary

**How to Use**:
- Sort by "SLA Risk" to prioritize most urgent cases
- Filter by Assignment Group to see team-specific risks
- Export the list for action planning

---

### 4. Patterns Page

**Purpose**: Identify trends and patterns in case data

**Components**:

#### Most Common Case Types
- **What it shows**: Case types that occur most frequently
- **Source**: Counts cases grouped by `Case Type` column
- **Visualization**: Bar chart showing top 15 case types
- **Resolution Times by Case Type**: Table showing average resolution time for each type
- **Interpretation**:
  - High frequency + slow resolution = problematic case type
  - Recurring types = may need preventive measures

#### Case Distribution by Assignment Group
- **What it shows**: Workload distribution across teams
- **Source**: Counts cases grouped by `AssignmentGroup` column
- **Visualization**: Bar chart showing case counts per team
- **Resolution Times by Group**: Table showing average resolution time per team
- **Interpretation**:
  - High workload + slow resolution = bottleneck team
  - Uneven distribution = may need resource reallocation

#### Temporal Patterns
- **Cases by Day of Week**: Bar chart showing case creation patterns
  - *Source*: Day of week extracted from `Create Date` column
  - *Interpretation*: Helps optimize staffing schedules
- **Peak Hours**: Line chart showing top 5 hours with most case creation
  - *Source*: Hour extracted from `Create Date` column
  - *Interpretation*: Identifies busy periods for resource planning

**How to Use**:
- Identify recurring issues for preventive action
- Optimize staffing based on temporal patterns
- Balance workload across teams

---

### 5. Inefficiencies Page

**Purpose**: Find bottlenecks and process gaps

**Components**:

#### Recurring Issues
- **What it shows**: Case types that occur 5+ times
- **Source**: Counts cases grouped by `Case Type`, filters types with 5+ occurrences
- **Display**: Table with:
  - Case Type
  - Frequency (number of occurrences)
  - Average Resolution Time
  - Common Summaries (most frequent summary text)
- **Interpretation**: 
  - High frequency = recurring problem
  - Slow resolution = process inefficiency
- **Action**: Implement preventive measures for recurring types

#### Identified Bottlenecks
- **What it shows**: Assignment groups with high case volume AND slow resolution times
- **Criteria**: 
  - High Workload: Groups in top 25% by case count
  - Slow Resolution: Groups in top 25% by average resolution time
- **Source**: Calculated from `AssignmentGroup`, case counts, and resolution times
- **Display**: Table with group metrics
- **Interpretation**: Teams that may need additional resources or process improvements

#### Process Gaps
- **What it shows**: Data quality issues and process inconsistencies
- **Examples**:
  - Closed cases missing resolution details
  - Closed cases missing end date
  - Draft cases older than 7 days
- **Source**: Data quality checks on various columns
- **Action**: Improve data entry processes

**How to Use**:
- Address recurring issues with preventive measures
- Allocate resources to bottleneck teams
- Improve data quality processes

---

### 6. Recommendations Page

**Purpose**: Actionable recommendations based on analysis

**Display**: Expandable sections organized by:
- **Priority**: High, Medium, Low
- **Category**: SLA Compliance, Resource Allocation, Process Improvement, etc.

**Each Recommendation Includes**:
- **Recommendation**: Specific action to take
- **Action Items**: Step-by-step tasks
- **Category**: What type of improvement this addresses

**How to Use**:
- Prioritize High priority recommendations
- Assign action items to team members
- Track implementation progress

---

### 7. AI Insights Page (AI Enabled)

**Purpose**: Natural language summaries and insights generated by AI

**Components**:

#### Executive Summary (AI)
- **What it shows**: AI-generated summary of key findings
- **Content**: High-level overview of your case data analysis
- **Use Case**: Quick understanding without diving into details

#### Risk Analysis (AI)
- **What it shows**: AI-powered risk assessment
- **Content**: 
  - Severity classification
  - Risk prioritization
  - Mitigation strategies
- **Use Case**: Understanding risk landscape

#### Recommendations (AI)
- **What it shows**: AI-generated prioritized recommendations
- **Content**: Based on patterns and inefficiencies identified
- **Use Case**: Getting AI-suggested actions

#### Case Type Deep Dive (AI)
- **What it shows**: Detailed analysis for specific case types
- **Content**: AI analysis based on case summaries and patterns
- **Use Case**: Understanding specific case type issues

**How to Use**:
- Read for quick insights
- Use as starting point for deeper investigation
- Share with stakeholders who prefer narrative summaries

---

### 8. Chat Page (AI Enabled)

**Purpose**: Ask questions about your data and get precise, data-driven answers

**Features**:
- **Example Questions**: Click pre-written questions to ask
- **Custom Questions**: Type your own questions in the chat input
- **Precise Answers**: AI provides exact numbers and specific examples
- **Data Sources**: See which data sources were used to answer

**Example Questions**:
- "What are the top risks I should focus on?"
- "Why is the closure rate so low?"
- "Which assignment group has the most bottlenecks?"
- "What are the most common case types?"
- "How can I improve SLA compliance?"

**Answer Format**:
- **Crisp and Concise**: 3-5 sentences maximum
- **Data-Driven**: Cites exact numbers (e.g., "42 cases", "67.9%")
- **Specific Examples**: References specific case types, groups, etc.
- **Bullet Points**: For multiple items

**How to Use**:
- Ask follow-up questions for deeper insights
- Use for ad-hoc analysis
- Get quick answers without navigating multiple pages

---

### 9. Downloads Page

**Purpose**: Export analysis results

**Options**:

#### Download JSON Report
- **What it contains**: Complete analysis results in JSON format
- **Use Case**: 
  - Integration with other systems
  - Programmatic access to results
  - Archiving analysis results

#### Download Summary CSV
- **What it contains**: Key metrics in CSV format
- **Columns**: Metric name and value
- **Metrics Included**:
  - Total Cases
  - Closure Rate %
  - SLA Compliance %
  - High Priority Open
  - SLA At Risk
- **Use Case**: 
  - Import into Excel for reporting
  - Create custom dashboards
  - Share with stakeholders

**How to Use**:
- Export for reporting purposes
- Share with team members
- Archive for historical tracking

---

## Interpreting Metrics

### Key Performance Indicators

#### Closure Rate
- **Good**: 80%+
- **Fair**: 60-79%
- **Poor**: <60%
- **Action**: If low, investigate why cases aren't closing

#### SLA Compliance Rate
- **Good**: 80%+
- **Fair**: 60-79%
- **Poor**: <60%
- **Action**: If low, review SLA targets and resolution processes

#### Resolution Time
- **Context-Dependent**: Compare to SLA targets
- **Action**: If high, investigate bottlenecks

### Risk Indicators

#### High Priority Open Cases
- **Critical**: >20 cases
- **Warning**: 10-20 cases
- **Good**: <10 cases
- **Action**: Prioritize and allocate resources

#### SLA At Risk Cases
- **Critical**: >15 cases
- **Warning**: 5-15 cases
- **Good**: <5 cases
- **Action**: Escalate and expedite resolution

#### Aging Cases
- **Critical**: >10 cases
- **Warning**: 5-10 cases
- **Good**: <5 cases
- **Action**: Review and escalate

---

## Best Practices

### 1. Regular Monitoring
- Run analysis weekly or monthly
- Track metrics over time
- Identify trends and patterns

### 2. Action Planning
- Use Risk page to prioritize actions
- Assign cases from "SLA At Risk" list
- Address recurring issues from Patterns page

### 3. Team Communication
- Share Overview page with leadership
- Use AI Insights for stakeholder presentations
- Export data for team meetings

### 4. Continuous Improvement
- Monitor Recommendations page
- Track improvements in metrics
- Adjust processes based on findings

---

## Troubleshooting

### No Data Showing
- **Check**: Ensure CSV file was uploaded successfully
- **Check**: Verify CSV has required columns (Create Date, CaseStatus, etc.)
- **Action**: Re-upload the file

### Missing Metrics
- **Check**: Ensure data has required columns
- **Check**: Verify date columns are in correct format
- **Action**: Review data quality in Inefficiencies page

### AI Features Not Working
- **Check**: "AI Enhancements" is checked in sidebar
- **Check**: `azure_openai_config.json` is configured correctly
- **Action**: Verify Azure OpenAI credentials

### Slow Performance
- **Large Datasets**: Analysis may take 30+ seconds for 10K+ cases
- **Action**: Wait for analysis to complete, or use smaller dataset

---

## Tips for Effective Use

1. **Start with Overview**: Get high-level understanding first
2. **Drill Down**: Use navigation to explore specific areas
3. **Use Chat**: Ask questions for quick insights
4. **Export Data**: Download results for offline analysis
5. **Compare Over Time**: Run analysis regularly to track trends
6. **Share Insights**: Use AI Insights page for presentations

---

## Summary

The Streamlit UI provides a comprehensive interface for analyzing case management data. Each page offers different perspectives:

- **Overview**: Executive summary
- **KPIs**: Performance metrics
- **Risks**: Urgent issues
- **Patterns**: Trends and distributions
- **Inefficiencies**: Bottlenecks and gaps
- **Recommendations**: Actionable items
- **AI Insights**: Natural language summaries
- **Chat**: Interactive Q&A
- **Downloads**: Export capabilities

Use this guide to navigate the interface and interpret the results effectively.

