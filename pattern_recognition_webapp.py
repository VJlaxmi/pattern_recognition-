"""
AI Agent for Operational Excellence - Pattern Recognition Web Application
Streamlit-based web UI for uploading CSV and viewing insights
"""

import streamlit as st
import pandas as pd
import json
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, date
import io
import numpy as np
from pattern_recognition_analysis import CDOPatternRecognition
from pattern_recognition_ai_enhanced import AIEnhancedPatternRecognition

# Page configuration
st.set_page_config(
    page_title="AI Agent for Operational Excellence",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded"
)

# Professional Microsoft Fluent Design-inspired CSS
css_content = """
    <style>
    /* Microsoft Fluent Design Color Palette */
    :root {{
        --ms-blue: #0078D4;
        --ms-blue-dark: #005A9E;
        --ms-gray-10: #FAF9F8;
        --ms-gray-20: #F3F2F1;
        --ms-gray-30: #EDEBE9;
        --ms-gray-50: #E1DFDD;
        --ms-gray-90: #323130;
        --ms-gray-100: #201F1E;
        --ms-red: #D13438;
        --ms-orange: #FF8C00;
        --ms-green: #107C10;
        --bg-primary: #FFFFFF;
        --bg-secondary: #FAF9F8;
        --bg-tertiary: #F3F2F1;
        --text-primary: #323130;
        --text-secondary: #605E5C;
        --text-tertiary: #A19F9D;
        --border-color: #EDEBE9;
        --hover-bg: #F3F2F1;
    }}
    
    /* Main app styling */
    .stApp,
    .stApp > div,
    .main {{
        background-color: var(--bg-primary) !important;
        color: var(--text-primary) !important;
    }}
    
    /* Sidebar styling */
    section[data-testid="stSidebar"],
    section[data-testid="stSidebar"] > div {{
        background-color: var(--bg-primary) !important;
        border-right: 1px solid var(--border-color) !important;
    }}
    
    /* Main content styling */
    [data-testid="stAppViewContainer"],
    [data-testid="stAppViewContainer"] > div {{
        background-color: var(--bg-primary) !important;
    }}
    
    /* Block containers */
    .block-container,
    .element-container {{
        background-color: var(--bg-primary) !important;
        color: var(--text-primary) !important;
    }}
    
    /* Main container styling */
    .main .block-container {{
        padding-top: 3rem;
        padding-bottom: 2rem;
    }}
    
    /* Professional header styling */
    h1 {{
        font-family: 'Segoe UI', 'Segoe UI Web (West European)', -apple-system, BlinkMacSystemFont, 'Roboto', 'Helvetica Neue', sans-serif;
        font-size: 2rem;
        font-weight: 600;
        color: var(--text-primary);
        margin-bottom: 1.5rem;
        letter-spacing: -0.02em;
    }}
    
    h2 {{
        font-family: 'Segoe UI', 'Segoe UI Web (West European)', -apple-system, BlinkMacSystemFont, 'Roboto', 'Helvetica Neue', sans-serif;
        font-size: 1.5rem;
        font-weight: 600;
        color: var(--text-primary);
        margin-top: 2rem;
        margin-bottom: 1rem;
        letter-spacing: -0.01em;
    }}
    
    h3 {{
        font-family: 'Segoe UI', 'Segoe UI Web (West European)', -apple-system, BlinkMacSystemFont, 'Roboto', 'Helvetica Neue', sans-serif;
        font-size: 1.25rem;
        font-weight: 600;
        color: var(--text-primary);
        margin-top: 1.5rem;
        margin-bottom: 0.75rem;
    }}
    
    /* Microsoft Logo Header */
    .ms-logo-header {{
        display: flex;
        align-items: center;
        gap: 1rem;
        padding: 1.5rem 0;
        border-bottom: 1px solid var(--border-color);
        margin-bottom: 2rem;
    }}
    
    .ms-logo {{
        height: 32px;
        width: auto;
    }}
    
    .ms-logo-text {{
        font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, 'Roboto', sans-serif;
        font-size: 1.25rem;
        font-weight: 400;
        color: var(--text-secondary);
        margin: 0;
    }}
    
    /* Metric cards with subtle shadows - theme aware */
    .metric-card {{
        background-color: var(--bg-secondary);
        padding: 1.5rem;
        border-radius: 4px;
        border: 1px solid var(--border-color);
        margin: 0.75rem 0;
        box-shadow: 0 1.6px 3.6px rgba(0, 0, 0, 0.13), 0 0.3px 0.9px rgba(0, 0, 0, 0.11);
        transition: box-shadow 0.2s ease;
    }}
    
    .metric-card:hover {{
        box-shadow: 0 3.2px 7.2px rgba(0, 0, 0, 0.13), 0 0.6px 1.8px rgba(0, 0, 0, 0.11);
    }}
    
    /* Professional status indicators */
    .status-critical {{
        color: var(--ms-red);
        font-weight: 600;
    }}
    
    .status-warning {{
        color: var(--ms-orange);
        font-weight: 600;
    }}
    
    .status-success {{
        color: var(--ms-green);
        font-weight: 600;
    }}
    
    .status-info {{
        color: var(--ms-blue);
        font-weight: 600;
    }}
    
    /* Button styling */
    .stButton > button {{
        background-color: var(--ms-blue);
        color: white;
        border: none;
        border-radius: 2px;
        padding: 0.5rem 1rem;
        font-weight: 500;
        transition: background-color 0.2s ease;
    }}
    
    .stButton > button:hover {{
        background-color: var(--ms-blue-dark);
    }}
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 0.5rem;
        border-bottom: 1px solid var(--ms-gray-30);
    }}
    
    .stTabs [data-baseweb="tab"] {{
        padding: 0.75rem 1.5rem;
        font-weight: 500;
        color: var(--ms-gray-90);
    }}
    
    .stTabs [aria-selected="true"] {{
        color: var(--ms-blue);
        border-bottom: 2px solid var(--ms-blue);
    }}
    
    /* Simple Navigation Menu - Text List Style */
    .nav-menu-item {{
        display: block;
        padding: 0.5rem 0.75rem;
        margin: 0;
        color: var(--text-primary);
        text-decoration: none;
        font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, 'Roboto', sans-serif;
        font-size: 0.875rem;
        font-weight: 400;
        cursor: pointer;
        transition: all 0.15s ease;
        border-left: 3px solid transparent;
        border-radius: 0;
    }}
    
    .nav-menu-item:hover {{
        background-color: var(--hover-bg);
        color: var(--text-primary);
    }}
    
    .nav-menu-item.active {{
        color: var(--ms-blue);
        font-weight: 600;
        border-left: 3px solid var(--ms-blue);
        background-color: transparent;
    }}
    
    /* Simple navigation menu - no buttons, just text */
    .simple-nav-item {{
        display: block;
        padding: 0.5rem 0.75rem;
        margin: 0;
        color: var(--text-primary);
        text-decoration: none;
        font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, 'Roboto', sans-serif;
        font-size: 0.875rem;
        font-weight: 400;
        cursor: pointer;
        transition: all 0.15s ease;
        border-left: 3px solid transparent;
        border-radius: 0;
        background: transparent;
    }}
    
    .simple-nav-item:hover {{
        background-color: var(--hover-bg);
        color: var(--text-primary);
    }}
    
    .simple-nav-item.active {{
        color: var(--ms-blue);
        font-weight: 600;
        border-left: 3px solid var(--ms-blue);
        background-color: transparent;
    }}
    
    /* Completely remove button styling - make it look like plain text */
    div[data-testid="stSidebar"] .simple-nav-container button {{
        all: unset !important;
        display: block !important;
        width: 100% !important;
        padding: 0.5rem 0.75rem !important;
        margin: 0 !important;
        margin-bottom: 1px !important;
        text-align: left !important;
        color: var(--text-primary) !important;
        font-weight: 400 !important;
        font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, 'Roboto', sans-serif !important;
        font-size: 0.875rem !important;
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
        border-left: 3px solid transparent !important;
        border-radius: 0 !important;
        cursor: pointer !important;
        transition: all 0.15s ease !important;
    }}
    
    div[data-testid="stSidebar"] .simple-nav-container button:hover {{
        background-color: var(--hover-bg) !important;
        color: var(--text-primary) !important;
    }}
    
    div[data-testid="stSidebar"] .simple-nav-container button[kind="primary"] {{
        color: var(--ms-blue) !important;
        font-weight: 600 !important;
        border-left: 3px solid var(--ms-blue) !important;
        background: transparent !important;
    }}
    
    div[data-testid="stSidebar"] .simple-nav-container button[kind="secondary"] {{
        color: var(--text-primary) !important;
        background: transparent !important;
    }}
    
    /* Remove button container styling */
    div[data-testid="stSidebar"] .simple-nav-container div[data-testid="stButton"] {{
        margin: 0 !important;
        padding: 0 !important;
        width: 100% !important;
    }}
    
    /* Remove gaps between navigation items */
    div[data-testid="stSidebar"] .simple-nav-container div[data-testid="stVerticalBlock"] {{
        gap: 0 !important;
    }}
    
    div[data-testid="stSidebar"] .simple-nav-container div[data-testid="stVerticalBlock"] > div {{
        margin: 0 !important;
        padding: 0 !important;
    }}
    
    /* Navigation section headers */
    .nav-section-header {{
        font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, 'Roboto', sans-serif;
        font-size: 0.6875rem;
        font-weight: 600;
        color: #605E5C;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        padding: 1rem 0 0.5rem 0;
        margin: 0;
        margin-top: 1.5rem;
    }}
    
    .nav-section-header:first-child {{
        margin-top: 0;
        padding-top: 0;
    }}
    
    /* Info boxes */
    .stInfo {{
        background-color: #E8F4F8;
        border-left: 4px solid var(--ms-blue);
        border-radius: 2px;
    }}
    
    .stSuccess {{
        background-color: #E8F5E9;
        border-left: 4px solid var(--ms-green);
        border-radius: 2px;
    }}
    
    .stWarning {{
        background-color: #FFF4E5;
        border-left: 4px solid var(--ms-orange);
        border-radius: 2px;
    }}
    
    .stError {{
        background-color: #FDE7E9;
        border-left: 4px solid var(--ms-red);
        border-radius: 2px;
    }}
    
    /* Data table styling */
    .dataframe {{
        border: 1px solid var(--ms-gray-30);
        border-radius: 4px;
    }}
    
    /* Remove Streamlit branding */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    header {{visibility: hidden;}}
    
    /* Professional spacing */
    .element-container {{
        margin-bottom: 1.5rem;
    }}
    
    /* Compact sidebar spacing */
    section[data-testid="stSidebar"] > div {{
        padding-top: 1rem;
    }}
    
    /* Remove excessive margins from sidebar elements */
    section[data-testid="stSidebar"] .element-container {{
        margin-bottom: 0.5rem;
    }}
    
    /* Sidebar header spacing */
    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {{
        margin-top: 1rem;
        margin-bottom: 0.75rem;
    }}
    
    section[data-testid="stSidebar"] h1:first-child,
    section[data-testid="stSidebar"] h2:first-child,
    section[data-testid="stSidebar"] h3:first-child {{
        margin-top: 0;
    }}
    </style>
"""
st.markdown(css_content, unsafe_allow_html=True)

def load_data(uploaded_file):
    """Load and validate CSV data"""
    try:
        df = pd.read_csv(uploaded_file)
        return df, None
    except Exception as e:
        return None, str(e)

def display_executive_summary(summary):
    """Display executive summary metrics with explanations"""
    st.header("Executive Summary")
    
    # Add explanation expander
    with st.expander("About"):
        st.markdown("""
        **Total Cases**: The total number of cases in your uploaded dataset. This is the count of all rows in your CSV file.
        
        **Closure Rate**: Percentage of cases that have been closed (Status = "Closed"). 
        - Formula: (Number of Closed Cases / Total Cases) × 100
        - Source: Counts cases where `CaseStatus` = "Closed"
        - Target: Typically 80%+ is considered good
        
        **SLA Compliance**: Percentage of closed cases that were resolved within their SLA deadline.
        - Formula: (Cases Resolved Within SLA / Total Closed Cases) × 100
        - **SLA Targets**: Currently using **default assumptions** (not from your CSV):
          - Critical (0): 1 day (default - configure in sidebar)
          - High (1): 5 days (default - configure in sidebar)
          - Medium (2): 10 days (default - configure in sidebar)
          - Low (3): 20 days (default - configure in sidebar)
          - Informational (4): 30 days (default - configure in sidebar)
        - Source: Compares `Resolution Time` (End Date - Create Date) to SLA target
        - **Action Required**: Configure your actual SLA targets in the sidebar for accurate compliance rates!
        - Target: 80%+ compliance is standard
        
        **High Priority Open**: Number of Critical (0) and High (1) severity cases that are still open.
        - Source: Counts cases where `Case Severity` ≤ 1 AND `CaseStatus` ≠ "Closed"
        - These cases require immediate attention
        
        **SLA At Risk**: Number of open cases that are at 75% or more of their SLA deadline.
        - Source: Calculates (Days Open / SLA Target) × 100 for each open case
        - **Uses configured SLA targets** (defaults if not configured)
        - Flags cases likely to breach SLA if not addressed soon
        """)
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("Total Cases", summary['total_cases'],
                 help="Total number of cases in your dataset")
    
    with col2:
        closure_rate = summary['closure_rate']
        st.metric("Closure Rate", f"{closure_rate:.1f}%", 
                 delta=f"{closure_rate - 50:.1f}%" if closure_rate < 50 else None,
                 help="Percentage of cases that have been closed")
    
    with col3:
        sla_rate = summary['sla_compliance_rate']
        st.metric("SLA Compliance", f"{sla_rate:.1f}%",
                 delta=f"{sla_rate - 80:.1f}%" if sla_rate < 80 else None,
                 help="Percentage of closed cases resolved within SLA")
    
    with col4:
        st.metric("High Priority Open", summary['high_priority_open'],
                 delta=f"-{summary['high_priority_open']}" if summary['high_priority_open'] > 0 else None,
                 help="Critical and High severity cases still open")
    
    with col5:
        st.metric("SLA At Risk", summary['sla_at_risk_count'],
                 delta=f"-{summary['sla_at_risk_count']}" if summary['sla_at_risk_count'] > 0 else None,
                 help="Open cases at 75%+ of SLA deadline")

def display_kpis(kpis):
    """Display KPI charts and metrics with explanations"""
    st.header("Key Performance Indicators")
    
    # Add explanation
    with st.expander("About"):
        st.markdown("""
        **Cases by Severity**: Distribution of cases across severity levels.
        - Source: Counts cases grouped by `Case Severity` column
        - Shows how many Critical (0), High (1), Medium (2), Low (3), and Informational (4) cases exist
        
        **Cases by Status**: Distribution of cases across different statuses.
        - Source: Counts cases grouped by `CaseStatus` column
        - Common statuses: Draft, Analysis, Contain, Eradicate, Review, Recover, Closed
        
        **Average Resolution Time**: Mean time to resolve closed cases.
        - Formula: Sum of (End Date - Create Date) for all closed cases / Number of closed cases
        - Source: Calculated from `End Date` and `Create Date` columns
        - Only includes cases with both dates and Status = "Closed"
        
        **Median Resolution Time**: Middle value when resolution times are sorted.
        - More robust to outliers than average
        - 50% of cases resolved faster, 50% slower than this value
        """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Cases by Severity
        if 'cases_by_severity' in kpis:
            severity_data = kpis['cases_by_severity']
            fig = px.pie(
                values=list(severity_data.values()),
                names=list(severity_data.keys()),
                title="Cases by Severity",
                labels={'value': 'Count'}
            )
            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Cases by Status
        if 'cases_by_status' in kpis:
            status_data = kpis['cases_by_status']
            fig = px.bar(
                x=list(status_data.keys()),
                y=list(status_data.values()),
                title="Cases by Status",
                labels={'x': 'Status', 'y': 'Count'}
            )
            fig.update_xaxes(tickangle=45)
            st.plotly_chart(fig, use_container_width=True)
    
    # Resolution Time Analysis
    if 'avg_resolution_time' in kpis and kpis['avg_resolution_time']:
        st.subheader("Resolution Time Metrics")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Avg Resolution Time", f"{kpis['avg_resolution_time']:.1f} days",
)
        with col2:
            st.metric("Median Resolution Time", f"{kpis['median_resolution_time']:.1f} days")
    
    # Additional KPI details
    if 'cases_by_type' in kpis:
        st.subheader("Cases by Type")
        type_data = kpis['cases_by_type']
        type_df = pd.DataFrame(list(type_data.items()), columns=['Case Type', 'Count'])
        type_df = type_df.sort_values('Count', ascending=False).head(10)
        st.dataframe(type_df, use_container_width=True, hide_index=True)
        st.caption("Source: Count of cases grouped by Case Type column")
    
    if 'cases_by_assignment_group' in kpis:
        st.subheader("Cases by Assignment Group")
        group_data = kpis['cases_by_assignment_group']
        group_df = pd.DataFrame(list(group_data.items()), columns=['Assignment Group', 'Case Count'])
        group_df = group_df.sort_values('Case Count', ascending=False)
        st.dataframe(group_df, use_container_width=True, hide_index=True)
        st.caption("Source: Count of cases grouped by AssignmentGroup column")

def display_risks(risks):
    """Display risk analysis with explanations"""
    st.header("Risk Analysis")
    
    with st.expander("Understanding Risk Metrics"):
        st.markdown("""
        **Cases at Risk of SLA Breach**: Open cases that are at 75% or more of their SLA deadline.
        - Calculation: (Days Open / SLA Target Days) × 100 ≥ 75%
        - Days Open = Current Date - Create Date
        - SLA Target based on severity (Critical: 1 day, High: 5 days, Medium: 10 days, Low: 20 days, Informational: 30 days)
        - Source: Compares time since case creation to severity-based SLA target
        
        **High Priority Open Cases**: Critical (0) and High (1) severity cases that are still open.
        - Source: Filters cases where `Case Severity` ≤ 1 AND `CaseStatus` ≠ "Closed"
        - These require immediate attention due to their severity
        
        **Aging Cases**: Cases that have been open for more than 30 days.
        - Calculation: Current Date - Create Date > 30 days
        - Source: Calculated from `Create Date` column
        - Indicates potential process bottlenecks or resource constraints
        """)
    
    # SLA At Risk Cases
    if 'sla_at_risk' in risks and risks['sla_at_risk']:
        st.subheader("Cases at Risk of SLA Breach")
        st.caption("Cases at 75%+ of their SLA deadline - likely to breach if not addressed soon")
        sla_df = pd.DataFrame(risks['sla_at_risk'])
        if len(sla_df) > 0:
            # Format the dataframe for better display
            if 'SLA Risk' in sla_df.columns:
                sla_df['SLA Risk'] = sla_df['SLA Risk'].apply(lambda x: f"{x:.1f}%" if pd.notna(x) else "N/A")
            if 'Days Open' in sla_df.columns:
                sla_df['Days Open'] = sla_df['Days Open'].apply(lambda x: f"{x:.1f}" if pd.notna(x) else "N/A")
            st.dataframe(sla_df, use_container_width=True, hide_index=True)
            st.info(f"{len(sla_df)} cases at risk")
        else:
            st.success("No cases at risk")
    
    # High Priority Open Cases
    if 'high_priority_open' in risks and risks['high_priority_open']:
        st.subheader("High Priority Open Cases")
        st.caption("Critical (0) and High (1) severity cases that are still open")
        high_priority_df = pd.DataFrame(risks['high_priority_open'])
        if len(high_priority_df) > 0:
            if 'Days Open' in high_priority_df.columns:
                high_priority_df['Days Open'] = high_priority_df['Days Open'].apply(lambda x: f"{x:.1f}" if pd.notna(x) else "N/A")
            st.dataframe(high_priority_df, use_container_width=True, hide_index=True)
            st.warning(f"{len(high_priority_df)} high priority cases")
        else:
            st.success("No high priority cases")
    
    # Aging Cases
    if 'aging_cases' in risks and risks['aging_cases']:
        st.subheader("Aging Cases (>30 days)")
        st.caption("Cases open for more than 30 days - may indicate process bottlenecks")
        aging_df = pd.DataFrame(risks['aging_cases'])
        if len(aging_df) > 0:
            if 'Days Open' in aging_df.columns:
                aging_df['Days Open'] = aging_df['Days Open'].apply(lambda x: f"{x:.1f}" if pd.notna(x) else "N/A")
            st.dataframe(aging_df, use_container_width=True, hide_index=True)
            st.info(f"{len(aging_df)} aging cases")
        else:
            st.success("No aging cases")

def display_patterns(patterns):
    """Display pattern analysis with explanations"""
    st.header("Pattern Detection")
    
    with st.expander("Understanding Pattern Detection"):
        st.markdown("""
        **Most Common Case Types**: Identifies which types of cases occur most frequently.
        - Source: Counts cases grouped by `Case Type` column
        - Helps identify recurring issues that may need preventive measures
        
        **Case Distribution by Assignment Group**: Shows workload distribution across teams.
        - Source: Counts cases grouped by `AssignmentGroup` column
        - Helps identify teams with high workload that may need resource reallocation
        
        **Temporal Patterns**: Analyzes when cases are created (day of week, hour of day).
        - Source: Extracts day/hour from `Create Date` column
        - Helps optimize staffing schedules based on case arrival patterns
        """)
    
    # Case Type Patterns
    if 'case_type_patterns' in patterns and 'most_common_types' in patterns['case_type_patterns']:
        st.subheader("Most Common Case Types")
        st.caption("Source: Count of cases grouped by Case Type column")
        type_data = patterns['case_type_patterns']['most_common_types']
        type_df = pd.DataFrame(list(type_data.items()), columns=['Case Type', 'Count'])
        type_df = type_df.sort_values('Count', ascending=False).head(15)
        fig = px.bar(type_df, x='Case Type', y='Count', title="Top Case Types by Frequency")
        fig.update_xaxes(tickangle=45)
        st.plotly_chart(fig, use_container_width=True)
        
        # Show table with additional details
        if 'type_resolution_times' in patterns['case_type_patterns']:
            st.write("**Resolution Times by Case Type:**")
            res_data = patterns['case_type_patterns']['type_resolution_times']
            res_df = pd.DataFrame(list(res_data.items()), columns=['Case Type', 'Avg Resolution (days)'])
            res_df = res_df.sort_values('Avg Resolution (days)', ascending=False)
            st.dataframe(res_df, use_container_width=True, hide_index=True)
            st.caption("Source: Average of (End Date - Create Date) for closed cases, grouped by Case Type")
    
    # Assignment Group Patterns
    if 'assignment_group_patterns' in patterns and 'case_distribution' in patterns['assignment_group_patterns']:
        st.subheader("Case Distribution by Assignment Group")
        st.caption("Source: Count of cases grouped by AssignmentGroup column")
        group_data = patterns['assignment_group_patterns']['case_distribution']
        group_df = pd.DataFrame(list(group_data.items()), columns=['Assignment Group', 'Case Count'])
        group_df = group_df.sort_values('Case Count', ascending=False)
        fig = px.bar(group_df, x='Assignment Group', y='Case Count', title="Workload Distribution by Team")
        fig.update_xaxes(tickangle=45)
        st.plotly_chart(fig, use_container_width=True)
        
        # Show resolution times by group
        if 'group_resolution_times' in patterns['assignment_group_patterns']:
            st.write("**Resolution Times by Assignment Group:**")
            group_res_data = patterns['assignment_group_patterns']['group_resolution_times']
            group_res_df = pd.DataFrame(list(group_res_data.items()), columns=['Assignment Group', 'Avg Resolution (days)'])
            group_res_df = group_res_df.sort_values('Avg Resolution (days)', ascending=False)
            st.dataframe(group_res_df, use_container_width=True, hide_index=True)
            st.caption("Source: Average of (End Date - Create Date) for closed cases, grouped by AssignmentGroup")
    
    # Temporal Patterns
    if 'temporal_patterns' in patterns:
        st.subheader("Temporal Patterns")
        temp = patterns['temporal_patterns']
        
        if 'cases_by_day_of_week' in temp:
            col1, col2 = st.columns(2)
            with col1:
                day_data = temp['cases_by_day_of_week']
                day_df = pd.DataFrame(list(day_data.items()), columns=['Day of Week', 'Count'])
                # Order by day of week
                day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
                day_df['Day'] = day_df['Day of Week'].apply(lambda x: day_order.index(x) if x in day_order else 99)
                day_df = day_df.sort_values('Day')
                fig = px.bar(day_df, x='Day of Week', y='Count', title="Cases by Day of Week")
                st.plotly_chart(fig, use_container_width=True)
                st.caption("Source: Day of week extracted from Create Date column")
            
            with col2:
                if 'peak_hours' in temp:
                    hour_data = temp['peak_hours']
                    hour_df = pd.DataFrame(list(hour_data.items()), columns=['Hour', 'Count'])
                    hour_df = hour_df.sort_values('Hour')
                    fig = px.line(hour_df, x='Hour', y='Count', title="Peak Hours (Top 5)", markers=True)
                    st.plotly_chart(fig, use_container_width=True)
                    st.caption("Source: Hour extracted from Create Date column")

def display_inefficiencies(inefficiencies):
    """Display inefficiency analysis with explanations"""
    st.header("Inefficiency Detection")
    
    with st.expander("Understanding Inefficiency Metrics"):
        st.markdown("""
        **Recurring Issues**: Case types that occur frequently (5+ times).
        - Source: Counts cases grouped by `Case Type`, filters types with 5+ occurrences
        - Frequency: Number of times this case type appears
        - Avg Resolution: Average time to resolve this case type (from closed cases only)
        - Common Summaries: Most frequent summary text for this case type
        - Indicates areas where preventive measures could reduce case volume
        
        **Bottlenecks**: Assignment groups with high case volume AND slow resolution times.
        - High Workload: Groups in top 25% by case count
        - Slow Resolution: Groups in top 25% by average resolution time
        - Source: Calculated from `AssignmentGroup`, case counts, and resolution times
        - Indicates teams that may need additional resources or process improvements
        """)
    
    # Recurring Issues
    if 'recurring_issues' in inefficiencies and inefficiencies['recurring_issues']:
        st.subheader("Recurring Issues")
        st.caption("Case types that occur 5+ times - may benefit from preventive measures")
        recurring_df = pd.DataFrame(inefficiencies['recurring_issues'])
        if len(recurring_df) > 0:
            # Format the dataframe
            if 'avg_resolution_days' in recurring_df.columns:
                recurring_df['avg_resolution_days'] = recurring_df['avg_resolution_days'].apply(
                    lambda x: f"{x:.1f} days" if pd.notna(x) and x is not None else "N/A"
                )
            st.dataframe(recurring_df, use_container_width=True, hide_index=True)
            st.info(f"{len(recurring_df)} recurring issues")
        else:
            st.success("No recurring issues")
    
    # Bottlenecks
    if 'bottlenecks' in inefficiencies:
        st.subheader("Identified Bottlenecks")
        bottlenecks = inefficiencies['bottlenecks']
        if 'high_workload_slow_resolution' in bottlenecks and bottlenecks['high_workload_slow_resolution']:
            st.caption("Groups with high case volume AND slow resolution times (top 25% in both metrics)")
            bottleneck_data = bottlenecks['high_workload_slow_resolution']
            if isinstance(bottleneck_data, dict) and len(bottleneck_data) > 0:
                bottleneck_df = pd.DataFrame(bottleneck_data).T
                st.dataframe(bottleneck_df, use_container_width=True)
                st.warning(f"{len(bottleneck_df)} bottlenecks")
            else:
                st.success("No bottlenecks")
        else:
            st.info("No bottlenecks found")
    
    # Process Gaps
    if 'process_gaps' in inefficiencies:
        st.subheader("Process Gaps")
        gaps = inefficiencies['process_gaps']
        gap_items = []
        if gaps.get('missing_resolutions', 0) > 0:
            gap_items.append(f"**{gaps['missing_resolutions']}** closed cases missing resolution details")
        if gaps.get('cases_without_end_date', 0) > 0:
            gap_items.append(f"**{gaps['cases_without_end_date']}** closed cases missing end date")
        if gaps.get('draft_cases_old', 0) > 0:
            gap_items.append(f"**{gaps['draft_cases_old']}** draft cases older than 7 days")
        
        if gap_items:
            for item in gap_items:
                st.markdown(f"- {item}")
            st.caption("Source: Data quality checks on Case Resolution, End Date, and CaseStatus columns")
        else:
            st.success("No process gaps")

def display_recommendations(recommendations):
    """Display recommendations with explanations"""
    st.header("Recommendations")
    
    
    if not recommendations:
        st.success("No recommendations")
        return
    
    for i, rec in enumerate(recommendations, 1):
        priority = rec.get('priority', 'Medium')
        category = rec.get('category', 'General')
        
        with st.expander(f"[{priority}] {category}"):
            st.write(f"**Recommendation:** {rec.get('recommendation', 'N/A')}")
            st.write("**Action Items:**")
            for item in rec.get('action_items', []):
                st.write(f"- {item}")
            st.caption(f"Generated based on analysis of: {rec.get('category', 'General')} metrics")

def display_ai_insights(ai_insights):
    """Display AI-generated insights with explanations"""
    st.header("AI-Generated Insights")
    
    
    if 'executive_summary_ai' in ai_insights:
        st.subheader("Executive Summary (AI)")
        st.caption("AI-generated summary of key findings from your case data analysis")
        st.write(ai_insights['executive_summary_ai'])
    
    if 'risk_analysis_ai' in ai_insights:
        st.subheader("Risk Analysis (AI)")
        st.caption("AI-powered risk assessment with severity classification and mitigation strategies")
        st.write(ai_insights['risk_analysis_ai'])
    
    if 'recommendations_ai' in ai_insights:
        st.subheader("Recommendations (AI)")
        st.caption("AI-generated prioritized recommendations based on patterns and inefficiencies identified")
        st.write(ai_insights['recommendations_ai'])
    
    # Show which case type was analyzed if available
    case_type_keys = [key for key in ai_insights.keys() if key.startswith('case_type_analysis_')]
    if case_type_keys:
        st.subheader("Case Type Deep Dive (AI)")
        for key in case_type_keys:
            case_type = key.replace('case_type_analysis_', '')
            st.write(f"**Analysis for: {case_type}**")
            st.write(ai_insights[key])
            st.caption(f"AI analysis based on case summaries and patterns for {case_type} cases")

def display_chat_interface(analyzer, report, use_ai):
    """Display chat interface for querying data with LLM"""
    st.header("Chat with Your Data")
    
    if not use_ai:
        st.warning("Enable AI in sidebar")
        return
    
    if not hasattr(analyzer, 'openai_client') or analyzer.openai_client is None:
        st.error("Azure OpenAI not configured. Please check your configuration.")
        return
    
    
    # Initialize chat history
    if "chat_messages" not in st.session_state:
        st.session_state.chat_messages = []
    
    # Example questions
    st.subheader("Example Questions")
    st.caption("Click any question below to ask it, or type your own question in the chat input")
    example_questions = [
        "What are the top risks I should focus on?",
        "Why is the closure rate so low?",
        "Which assignment group has the most bottlenecks?",
        "What are the most common case types?",
        "How can I improve SLA compliance?",
        "What patterns do you see in the data?",
        "Which cases are at risk of SLA breach?",
        "What are the recurring issues?",
        "How is workload distributed across teams?",
        "What recommendations do you have?"
    ]
    
    cols = st.columns(2)
    selected_question = None
    for i, question in enumerate(example_questions):
        with cols[i % 2]:
            if st.button(question, key=f"example_{i}", use_container_width=True):
                selected_question = question
    
    # Display chat history
    chat_container = st.container()
    with chat_container:
        for message in st.session_state.chat_messages:
            with st.chat_message(message["role"]):
                st.write(message["content"])
                if "sources" in message:
                    with st.expander("Data Sources"):
                        st.json(message["sources"])
    
    # Chat input
    chat_input = st.chat_input("Ask a question about your case data...")
    
    # Use example question or chat input
    user_question = selected_question or chat_input
    
    if user_question:
        # Add user message to history
        st.session_state.chat_messages.append({"role": "user", "content": user_question})
        
        # Display user message
        with st.chat_message("user"):
            st.write(user_question)
        
        # Generate response
        with st.chat_message("assistant"):
            with st.spinner("Analyzing data and generating response..."):
                try:
                    response, sources = generate_chat_response(
                        analyzer, 
                        report, 
                        user_question
                    )
                    st.write(response)
                    
                    # Show data sources if available
                    if sources:
                        with st.expander("Data Sources Used"):
                            st.json(sources)
                    
                    # Add assistant response to history
                    st.session_state.chat_messages.append({
                        "role": "assistant", 
                        "content": response,
                        "sources": sources
                    })
                except Exception as e:
                    error_msg = f"Error generating response: {str(e)}"
                    st.error(error_msg)
                    st.session_state.chat_messages.append({
                        "role": "assistant", 
                        "content": error_msg
                    })
    
    # Clear chat button
    if st.button("Clear Chat History"):
        st.session_state.chat_messages = []
        st.rerun()

def generate_chat_response(analyzer, report, question):
    """Generate chat response using Azure OpenAI with data context"""
    if not hasattr(analyzer, 'openai_client') or analyzer.openai_client is None:
        return "Azure OpenAI not configured.", {}
    
    # Prepare data context
    context = prepare_data_context(report, analyzer)
    
    # Create prompt with context
    system_prompt = """You are a precision-focused data analyst specializing in case management and operational intelligence. 
Your role is to provide CRISP, CONCISE, DATA-DRIVEN answers based solely on the provided analysis data.

CRITICAL REQUIREMENTS:
1. Keep answers SHORT - maximum 3-5 sentences, use bullet points for multiple items
2. ALWAYS cite specific numbers, percentages, and counts from the data
3. Use exact values - do not approximate or round unless the data shows rounded values
4. Reference specific case types, assignment groups, or categories by their exact names
5. Be precise and factual - avoid generic statements
6. Format numbers consistently (e.g., "42 cases" not "about 40 cases")
7. If data is not available for a question, state that clearly in one sentence
8. NO long paragraphs - use concise sentences and bullet points
9. Get straight to the point - lead with the most important number or finding"""
    
    # Convert context to readable format
    context_str = format_context_for_llm(context)
    
    user_prompt = f"""Question: {question}

Data Context:
{context_str}

INSTRUCTIONS:
- Answer in 3-5 SHORT sentences maximum, use bullet points for lists
- Lead with the most important number or finding
- Cite exact values (e.g., "42 cases", "67.9%", "SecurityOps: 31 cases")
- Reference specific case types, assignment groups, or categories by their exact names
- Be CRISP and CONCISE - no long paragraphs or verbose explanations
- Every number must come from the data provided above"""
    
    try:
        response = analyzer.openai_client.chat.completions.create(
            model=analyzer.azure_config['deployment_name'],
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.1,  # Lower temperature for more precise, deterministic answers
            max_tokens=500  # Reduced for crisp, concise answers (3-5 sentences)
        )
        
        answer = response.choices[0].message.content
        
        # Identify which data sources were used
        sources = identify_data_sources(question, context)
        
        return answer, sources
    except Exception as e:
        return f"Error generating response: {str(e)}", {}

def prepare_data_context(report, analyzer):
    """Prepare condensed data context for LLM"""
    exec_summary = report.get('executive_summary', {})
    
    context = {
        "executive_summary": exec_summary,
        "key_metrics": {
            "total_cases": exec_summary.get('total_cases', 0),
            "closure_rate": exec_summary.get('closure_rate', 0),
            "sla_compliance": exec_summary.get('sla_compliance_rate', 0),
            "high_priority_open": exec_summary.get('high_priority_open', 0),
            "sla_at_risk": exec_summary.get('sla_at_risk_count', 0),
            "aging_cases": exec_summary.get('aging_cases_count', 0),
        }
    }
    
    # Add sample case data for context
    if hasattr(analyzer, 'df'):
        context['data_sample'] = {
            "total_rows": len(analyzer.df),
            "columns": list(analyzer.df.columns),
            "severity_distribution": analyzer.df['Case Severity'].value_counts().head(10).to_dict() if 'Case Severity' in analyzer.df.columns else {},
            "status_distribution": analyzer.df['CaseStatus'].value_counts().to_dict() if 'CaseStatus' in analyzer.df.columns else {},
        }
    
    # Add insights if available
    if 'insights' in report:
        insights = report['insights']
        
        # Detailed risks with breakdowns
        if 'risks' in insights:
            risks = insights['risks']
            context['top_risks'] = {
                "sla_at_risk_count": len(risks.get('sla_at_risk', [])),
                "high_priority_open_count": len(risks.get('high_priority_open', [])),
                "aging_cases_count": len(risks.get('aging_cases', []))
            }
            # Add detailed risk breakdowns
            if risks.get('sla_at_risk'):
                sla_risk_by_group = {}
                sla_risk_by_type = {}
                for case in risks.get('sla_at_risk', [])[:20]:  # Top 20
                    group = case.get('AssignmentGroup', 'Unknown')
                    case_type = case.get('Case Type', 'Unknown')
                    sla_risk_by_group[group] = sla_risk_by_group.get(group, 0) + 1
                    sla_risk_by_type[case_type] = sla_risk_by_type.get(case_type, 0) + 1
                context['sla_at_risk_breakdown'] = {
                    "by_group": sla_risk_by_group,
                    "by_type": sla_risk_by_type
                }
            if risks.get('high_priority_open'):
                high_priority_by_group = {}
                high_priority_by_type = {}
                for case in risks.get('high_priority_open', []):
                    group = case.get('AssignmentGroup', 'Unknown')
                    case_type = case.get('Case Type', 'Unknown')
                    high_priority_by_group[group] = high_priority_by_group.get(group, 0) + 1
                    high_priority_by_type[case_type] = high_priority_by_type.get(case_type, 0) + 1
                context['high_priority_breakdown'] = {
                    "by_group": high_priority_by_group,
                    "by_type": high_priority_by_type
                }
        
        # Top case types with detailed metrics
        if 'patterns' in insights and 'case_type_patterns' in insights['patterns']:
            type_patterns = insights['patterns']['case_type_patterns']
            case_types = type_patterns.get('most_common_types', {})
            context['top_case_types'] = dict(list(case_types.items())[:10])
            # Add resolution times by case type
            if 'type_resolution_times' in type_patterns:
                context['type_resolution_times'] = type_patterns.get('type_resolution_times', {})
            if 'type_closure_rates' in type_patterns:
                context['type_closure_rates'] = type_patterns.get('type_closure_rates', {})
        
        # Assignment groups
        if 'patterns' in insights and 'assignment_group_patterns' in insights['patterns']:
            groups = insights['patterns']['assignment_group_patterns'].get('case_distribution', {})
            context['assignment_groups'] = dict(list(groups.items())[:10])
        
        # Recurring issues
        if 'inefficiencies' in insights:
            recurring = insights['inefficiencies'].get('recurring_issues', [])
            context['recurring_issues'] = recurring[:5] if recurring else []
        
        # Bottlenecks
        if 'inefficiencies' in insights and 'bottlenecks' in insights['inefficiencies']:
            bottlenecks = insights['inefficiencies']['bottlenecks']
            context['bottlenecks'] = bottlenecks
    
    # Add SLA configuration
    if hasattr(analyzer, 'sla_targets'):
        context['sla_targets'] = analyzer.sla_targets
    
    return context

def format_context_for_llm(context):
    """Format context in a readable way for LLM"""
    lines = []
    
    # Executive Summary
    if 'executive_summary' in context:
        es = context['executive_summary']
        lines.append("EXECUTIVE SUMMARY:")
        lines.append(f"- Total Cases: {es.get('total_cases', 'N/A')}")
        lines.append(f"- Closure Rate: {es.get('closure_rate', 0):.2f}%")
        lines.append(f"- SLA Compliance Rate: {es.get('sla_compliance_rate', 0):.2f}%")
        lines.append(f"- High Priority Open Cases: {es.get('high_priority_open', 0)}")
        lines.append(f"- Cases at Risk of SLA Breach: {es.get('sla_at_risk_count', 0)}")
        lines.append(f"- Aging Cases (>30 days): {es.get('aging_cases_count', 0)}")
        lines.append("")
    
    # Key Metrics
    if 'key_metrics' in context:
        lines.append("KEY METRICS:")
        for key, value in context['key_metrics'].items():
            lines.append(f"- {key}: {value}")
        lines.append("")
    
    # Detailed KPI Information
    if 'kpi_details' in context:
        kpis = context['kpi_details']
        lines.append("DETAILED KPIs:")
        if kpis.get('total_cases'):
            lines.append(f"- Total Cases: {kpis['total_cases']}")
        if kpis.get('closed_cases'):
            lines.append(f"- Closed Cases: {kpis['closed_cases']}")
        if kpis.get('open_cases'):
            lines.append(f"- Open Cases: {kpis['open_cases']}")
        if kpis.get('closure_rate') is not None:
            lines.append(f"- Closure Rate: {kpis['closure_rate']:.2f}%")
        if kpis.get('sla_compliance_rate') is not None:
            lines.append(f"- SLA Compliance Rate: {kpis['sla_compliance_rate']:.2f}%")
        if kpis.get('avg_resolution_time') is not None and not pd.isna(kpis['avg_resolution_time']):
            lines.append(f"- Average Resolution Time: {kpis['avg_resolution_time']:.1f} days")
        if kpis.get('median_resolution_time') is not None and not pd.isna(kpis['median_resolution_time']):
            lines.append(f"- Median Resolution Time: {kpis['median_resolution_time']:.1f} days")
        if kpis.get('high_priority_cases'):
            lines.append(f"- High Priority Cases: {kpis['high_priority_cases']}")
        if kpis.get('critical_cases'):
            lines.append(f"- Critical Cases: {kpis['critical_cases']}")
        if kpis.get('sla_breaches') is not None:
            lines.append(f"- SLA Breaches: {kpis['sla_breaches']}")
        if 'cases_by_severity' in context:
            lines.append("Cases by Severity:")
            for severity, count in context['cases_by_severity'].items():
                lines.append(f"  {severity}: {count} cases")
        if 'cases_by_status' in context:
            lines.append("Cases by Status:")
            for status, count in list(context['cases_by_status'].items())[:10]:
                lines.append(f"  {status}: {count} cases")
        lines.append("")
    
    # Top Case Types
    if 'top_case_types' in context:
        lines.append("TOP CASE TYPES:")
        for case_type, count in list(context['top_case_types'].items())[:10]:
            lines.append(f"- {case_type}: {count} cases")
        lines.append("")
    
    # Assignment Groups
    if 'assignment_groups' in context:
        lines.append("ASSIGNMENT GROUPS (Workload):")
        for group, count in list(context['assignment_groups'].items())[:10]:
            lines.append(f"- {group}: {count} cases")
        lines.append("")
    
    # Recurring Issues
    if 'recurring_issues' in context and context['recurring_issues']:
        lines.append("RECURRING ISSUES:")
        for issue in context['recurring_issues'][:5]:
            lines.append(f"- {issue.get('case_type', 'Unknown')}: {issue.get('frequency', 0)} occurrences")
        lines.append("")
    
    # Top Risks
    if 'top_risks' in context:
        lines.append("RISK SUMMARY:")
        risks = context['top_risks']
        lines.append(f"- Cases at SLA Risk: {risks.get('sla_at_risk_count', 0)}")
        lines.append(f"- High Priority Open: {risks.get('high_priority_open_count', 0)}")
        lines.append(f"- Aging Cases: {risks.get('aging_cases_count', 0)}")
        lines.append("")
    
    # SLA Targets
    if 'sla_targets' in context:
        lines.append("SLA TARGETS (by Severity):")
        for severity, days in context['sla_targets'].items():
            severity_name = {0: "Critical", 1: "High", 2: "Medium", 3: "Low", 4: "Informational"}.get(severity, f"Severity {severity}")
            lines.append(f"- {severity_name} ({severity}): {days} days")
        lines.append("")
    
    return "\n".join(lines)

def identify_data_sources(question, context):
    """Identify which data sources were likely used to answer the question"""
    sources = {}
    question_lower = question.lower()
    
    # Check what the question is asking about
    if any(word in question_lower for word in ['risk', 'sla', 'breach', 'at risk', 'aging']):
        sources['risk_data'] = "SLA risk identification, high priority cases, aging cases"
    
    if any(word in question_lower for word in ['closure', 'close', 'resolution', 'resolve', 'compliance']):
        sources['kpi_data'] = "Closure rate, resolution times, SLA compliance"
    
    if any(word in question_lower for word in ['pattern', 'trend', 'type', 'common', 'frequent']):
        sources['pattern_data'] = "Case type patterns, temporal patterns, assignment group patterns"
    
    if any(word in question_lower for word in ['bottleneck', 'inefficiency', 'slow', 'workload', 'recurring']):
        sources['inefficiency_data'] = "Bottlenecks, recurring issues, process gaps"
    
    if any(word in question_lower for word in ['group', 'team', 'assignment']):
        sources['assignment_data'] = "Assignment group distribution, workload analysis"
    
    if any(word in question_lower for word in ['severity', 'critical', 'high priority']):
        sources['severity_data'] = "Case severity distribution, high priority cases"
    
    return sources


def render_navigation_menu():
    """Render simple text-based navigation menu - no blue boxes"""
    st.markdown("""
    <div class="nav-section-header">Navigation</div>
    """, unsafe_allow_html=True)
    
    # Navigation pages
    pages = [
        ("Overview", "overview"),
        ("KPIs", "kpis"),
        ("Risks", "risks"),
        ("Patterns", "patterns"),
        ("Inefficiencies", "inefficiencies"),
        ("Recommendations", "recommendations"),
        ("AI Insights", "ai_insights"),
        ("Chat", "chat"),
        ("Downloads", "downloads")
    ]
    
    # Initialize current page
    if 'current_page' not in st.session_state:
        st.session_state.current_page = "overview"
    
    # Render menu items as simple text list (no blue boxes)
    with st.container():
        st.markdown('<div class="simple-nav-container">', unsafe_allow_html=True)
        for page_name, page_id in pages:
            is_active = st.session_state.current_page == page_id
            
            if st.button(
                page_name,
                key=f"nav_{page_id}",
                use_container_width=True,
                type="primary" if is_active else "secondary"
            ):
                st.session_state.current_page = page_id
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="nav-section-header">Configuration</div>
    """, unsafe_allow_html=True)

def main():
    """Main application"""
    # Microsoft Logo and Header
    st.markdown("""
    <div class="ms-logo-header">
        <svg class="ms-logo" width="32" height="32" viewBox="0 0 23 23" fill="none" xmlns="http://www.w3.org/2000/svg">
            <rect x="0" y="0" width="10" height="10" fill="#F25022"/>
            <rect x="12" y="0" width="10" height="10" fill="#7FBA00"/>
            <rect x="0" y="12" width="10" height="10" fill="#00A4EF"/>
            <rect x="12" y="12" width="10" height="10" fill="#FFB900"/>
        </svg>
        <div>
            <h1 style="font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, 'Roboto', sans-serif; 
                       font-size: 2.5rem; 
                       font-weight: 600; 
                       color: var(--text-primary); 
                       margin: 0;
                       letter-spacing: -0.02em;">
                AI Agent for Operational Excellence
            </h1>
            <p class="ms-logo-text">
                AI Insights
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar with Navigation
    with st.sidebar:
        render_navigation_menu()
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # File upload
        uploaded_file = st.file_uploader(
            "Upload CSV",
            type=['csv']
        )
        
        # AI Enhancement toggle
        use_ai = st.checkbox(
            "AI Enhancements",
            value=True
        )
    
    # Main content - check for uploaded file OR existing report in session state
    if uploaded_file is not None:
        # New file uploaded - process it
        df, error = load_data(uploaded_file)
        
        if error:
            st.error(f"Error loading file: {error}")
            return
        
        st.success(f"Loaded {len(df)} cases from {uploaded_file.name}")
        
        # Save uploaded file temporarily
        with open("temp_upload.csv", "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        # Run analysis (SLA will be loaded automatically from SLA_sheet.csv)
        with st.spinner("Analyzing case data..."):
            try:
                if use_ai:
                    analyzer = AIEnhancedPatternRecognition(
                        "temp_upload.csv", 
                        "azure_openai_config.json",
                        sla_sheet_file="SLA_sheet.csv"
                    )
                    report = analyzer.generate_ai_enhanced_report()
                else:
                    analyzer = CDOPatternRecognition(
                        "temp_upload.csv", 
                        sla_sheet_file="SLA_sheet.csv"
                    )
                    report = analyzer.generate_insights_report()
                
                # Store report and analyzer in session state for navigation
                st.session_state.report = report
                st.session_state.analyzer = analyzer
                st.session_state.use_ai = use_ai
                st.session_state.analyze_kpis = True
                st.session_state.analyze_patterns = True
                st.session_state.analyze_risks = True
                st.session_state.analyze_inefficiencies = True
                
            except Exception as e:
                st.error(f"Error during analysis: {str(e)}")
                st.exception(e)
                return
    
    # Display content if report exists (either from new upload or previous session)
    if 'report' in st.session_state:
        report = st.session_state.report
        analyzer = st.session_state.analyzer
        use_ai = st.session_state.get('use_ai', False)
        analyze_kpis = st.session_state.get('analyze_kpis', True)
        analyze_patterns = st.session_state.get('analyze_patterns', True)
        analyze_risks = st.session_state.get('analyze_risks', True)
        analyze_inefficiencies = st.session_state.get('analyze_inefficiencies', True)
        
        # Display based on current page
        current_page = st.session_state.get('current_page', 'overview')
        
        if current_page == 'overview':
            if 'executive_summary' in report:
                display_executive_summary(report['executive_summary'])
        
        elif current_page == 'kpis':
            if analyze_kpis and 'insights' in report and 'kpis' in report['insights']:
                display_kpis(report['insights']['kpis'])
            else:
                st.info("KPIs disabled")
        
        elif current_page == 'risks':
            if analyze_risks and 'insights' in report and 'risks' in report['insights']:
                display_risks(report['insights']['risks'])
            else:
                st.info("Risks disabled")
        
        elif current_page == 'patterns':
            if analyze_patterns and 'insights' in report and 'patterns' in report['insights']:
                display_patterns(report['insights']['patterns'])
            else:
                st.info("Patterns disabled")
        
        elif current_page == 'inefficiencies':
            if analyze_inefficiencies and 'insights' in report and 'inefficiencies' in report['insights']:
                display_inefficiencies(report['insights']['inefficiencies'])
            else:
                st.info("Inefficiencies disabled")
        
        elif current_page == 'recommendations':
            if 'recommendations' in report:
                display_recommendations(report['recommendations'])
        
        elif current_page == 'ai_insights':
            if use_ai and 'ai_insights' in report:
                display_ai_insights(report['ai_insights'])
            elif use_ai:
                st.info("AI not configured")
            else:
                st.info("Enable AI in sidebar")
        
        elif current_page == 'chat':
            display_chat_interface(analyzer, report, use_ai)
        
        elif current_page == 'downloads':
            st.header("Download Results")
            col1, col2 = st.columns(2)
            
            with col1:
                # Convert dates and other non-serializable types
                def convert_for_json(obj):
                    if isinstance(obj, (pd.Timestamp, datetime)):
                        return obj.isoformat() if pd.notna(obj) else None
                    elif isinstance(obj, (date,)):
                        return obj.isoformat()
                    elif isinstance(obj, np.integer):
                        return int(obj)
                    elif isinstance(obj, np.floating):
                        return float(obj)
                    elif isinstance(obj, np.ndarray):
                        return obj.tolist()
                    elif isinstance(obj, dict):
                        return {str(key): convert_for_json(value) for key, value in obj.items()}
                    elif isinstance(obj, list):
                        return [convert_for_json(item) for item in obj]
                    elif pd.isna(obj):
                        return None
                    return obj
                
                report_clean = convert_for_json(report)
                json_str = json.dumps(report_clean, indent=2, default=str)
                st.download_button(
                    label="Download JSON Report",
                    data=json_str,
                    file_name=f"pattern_recognition_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json"
                )
            
            with col2:
                # Create summary CSV
                if 'executive_summary' in report:
                    summary_data = {
                        'Metric': ['Total Cases', 'Closure Rate %', 'SLA Compliance %', 
                                  'High Priority Open', 'SLA At Risk'],
                        'Value': [
                            report['executive_summary']['total_cases'],
                            report['executive_summary']['closure_rate'],
                            report['executive_summary']['sla_compliance_rate'],
                            report['executive_summary']['high_priority_open'],
                            report['executive_summary']['sla_at_risk_count']
                        ]
                    }
                    summary_df = pd.DataFrame(summary_data)
                    csv = summary_df.to_csv(index=False)
                    st.download_button(
                        label="Download Summary CSV",
                        data=csv,
                        file_name=f"pattern_recognition_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                        mime="text/csv"
                    )
    
    else:
        # Welcome screen
        st.info("Upload CSV to begin")
        
        st.markdown("""
        ## How This System Works
        
        This Pattern Recognition System analyzes your case management data to provide actionable insights. Here's how it works:
        
        ### Data Processing
        
        1. **Upload**: You upload a CSV file with case data
        2. **Parsing**: The system reads and parses dates, calculates time differences
        3. **Analysis**: Multiple algorithms analyze patterns, risks, and inefficiencies
        4. **Visualization**: Results are displayed in interactive charts and tables
        
        ### What Gets Calculated
        
        **From Your CSV Columns:**
        - `Create Date` → Used to calculate: Days Open, Temporal Patterns, Aging Cases
        - `End Date` → Used to calculate: Resolution Time, SLA Compliance
        - `Case Severity` → Used to: Categorize cases, Set SLA targets, Identify high priority
        - `CaseStatus` → Used to: Count open vs closed, Calculate closure rate
        - `Case Type` → Used to: Identify recurring issues, Analyze patterns
        - `AssignmentGroup` → Used to: Analyze workload distribution, Identify bottlenecks
        
        **Calculated Metrics:**
        - **Resolution Time** = End Date - Create Date (for closed cases)
        - **Days Open** = Current Date - Create Date (for open cases)
        - **SLA Target** = Based on severity (**Configurable** - see SLA Configuration in sidebar)
          - Default assumptions: Critical: 1 day, High: 5 days, Medium: 10 days, Low: 20 days, Info: 30 days
          - **You should configure your actual SLA targets!**
        - **SLA Risk %** = (Days Open / SLA Target) × 100
        - **Closure Rate** = (Closed Cases / Total Cases) × 100
        - **SLA Compliance** = (Cases Resolved Within SLA / Total Closed Cases) × 100
        
        **Important**: SLA targets are **NOT in your CSV** - they're currently using default assumptions. Configure your actual SLA targets in the sidebar for accurate analysis!
        
        ### Expected CSV Format
        
        Your CSV file should contain the following columns:
        - `Create Date` - Case creation timestamp (required)
        - `End Date` - Case closure timestamp (optional, for closed cases)
        - `Updated On` - Last update timestamp (required)
        - `Case Id` - Unique case identifier (required)
        - `Case Severity` - Severity level: 0-4 or text like "1 - High" (required)
        - `AssignmentGroup` - Team assigned to case (required)
        - `CaseOwnerName` - Individual case owner (optional)
        - `CaseStatus` - Current case status: Draft, Analysis, Contain, Closed, etc. (required)
        - `Case Source` - Source of the case (optional)
        - `Case Type` - Type/category of case (required)
        - `Case CurrentSummary` - Case description/summary (optional, used for AI analysis)
        - `Case Resolution` - Resolution details (optional)
        
        ### Features
        
        - **KPI Analysis**: Case volumes, closure rates, SLA compliance
        - **Pattern Detection**: Temporal patterns, case type trends, assignment group analysis
        - **Risk Identification**: SLA at risk cases, high priority open cases, aging cases
        - **Inefficiency Detection**: Bottlenecks, recurring issues, process gaps
        - **Root Cause Analysis**: Common themes, correlations, resolution factors
        - **AI Enhancements**: Natural language insights and recommendations (when enabled)
        
        ### Understanding the Results
        
        Each section includes:
        - **Expandable Info Boxes**: Click to see detailed explanations
        - **Source Captions**: Shows which CSV columns were used
        - **Formulas**: Explains how metrics are calculated
        - **Context**: What the numbers mean and why they matter
        """)

if __name__ == "__main__":
    main()

