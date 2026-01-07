"""
AI Agent for Operational Excellence - Pattern Recognition Analysis
Analyzes case management data to identify patterns, risks, inefficiencies, and root causes
"""

import pandas as pd
import numpy as np
from datetime import datetime, date
import json
from typing import Dict, List, Tuple, Any, Optional
import warnings
warnings.filterwarnings('ignore')

class CDOPatternRecognition:
    """Main class for pattern recognition and analysis"""
    
    def __init__(self, data_file: str, sla_sheet_file: str = "SLA_sheet.csv", sla_config: Dict[str, int] = None):
        """Initialize with case data
        
        Args:
            data_file: Path to CSV file with case data
            sla_sheet_file: Path to CSV file with SLA configuration (Team, Severity, TTR_Hours)
            sla_config: Optional dictionary mapping severity to SLA days (fallback if SLA sheet not found)
                       Format: {0: 1, 1: 5, 2: 10, 3: 20, 4: 30}
        """
        self.df = pd.read_csv(data_file)
        
        # Default SLA targets (fallback)
        self.default_sla_targets = {
            0: 1,   # Critical: 1 day
            1: 5,   # High: 5 days
            2: 10,  # Medium: 10 days
            3: 20,  # Low: 20 days
            4: 30   # Informational: 30 days
        }
        
        # Load SLA from CSV sheet
        self.sla_sheet = None
        self.sla_targets = sla_config if sla_config else self.default_sla_targets
        
        try:
            sla_df = pd.read_csv(sla_sheet_file)
            # Clean up the data
            sla_df = sla_df.dropna(subset=['Team', 'Severity', 'TTR_Hours'])
            # Convert TTR_Hours to days and create mapping
            sla_df['TTR_Days'] = pd.to_numeric(sla_df['TTR_Hours'], errors='coerce') / 24
            sla_df = sla_df.dropna(subset=['TTR_Days'])
            # Extract severity number from "Sev0", "Sev1", etc.
            sla_df['Severity_Num'] = sla_df['Severity'].str.extract(r'Sev(\d+)').astype(int)
            # Store the full SLA sheet for team-specific lookups
            self.sla_sheet = sla_df
            print(f"Loaded SLA configuration from {sla_sheet_file}")
        except FileNotFoundError:
            print(f"Warning: SLA sheet {sla_sheet_file} not found. Using defaults.")
        except Exception as e:
            print(f"Warning: Error loading SLA sheet: {e}. Using defaults.")
        
        self.prepare_data()
        self.insights = {}
        
    def prepare_data(self):
        """Clean and prepare data for analysis"""
        # Parse dates
        date_columns = ['Create Date', 'End Date', 'Updated On']
        for col in date_columns:
            self.df[col] = pd.to_datetime(self.df[col], errors='coerce', format='mixed')
        
        # Calculate resolution time (only for closed cases with valid End Date)
        # Only calculate where End Date exists and is after Create Date
        self.df['Resolution Time (days)'] = None
        mask = self.df['End Date'].notna() & self.df['Create Date'].notna()
        self.df.loc[mask, 'Resolution Time (days)'] = (
            self.df.loc[mask, 'End Date'] - self.df.loc[mask, 'Create Date']
        ).dt.total_seconds() / 86400
        
        # Filter out negative values (data errors where End Date < Create Date)
        self.df.loc[self.df['Resolution Time (days)'] < 0, 'Resolution Time (days)'] = None
        
        # Calculate time to update
        self.df['Time to Update (days)'] = (
            self.df['Updated On'] - self.df['Create Date']
        ).dt.total_seconds() / 86400
        
        # Extract severity numeric value
        self.df['Severity Numeric'] = self.df['Case Severity'].str.extract(r'(\d+)').astype(float)
        
        # Categorize cases
        self.df['Is Closed'] = self.df['CaseStatus'] == 'Closed'
        self.df['Is High Priority'] = self.df['Severity Numeric'] <= 1
        self.df['Is Critical'] = self.df['Severity Numeric'] == 0
        
        # Calculate SLA Target based on team and severity from SLA sheet
        if self.sla_sheet is not None and len(self.sla_sheet) > 0:
            # Create a function to lookup SLA for each case
            def get_sla_target(row):
                team = row['AssignmentGroup']
                severity = int(row['Severity Numeric']) if pd.notna(row['Severity Numeric']) else None
                
                if pd.isna(severity):
                    return None
                
                # Lookup SLA for this team and severity
                team_sla = self.sla_sheet[
                    (self.sla_sheet['Team'] == team) & 
                    (self.sla_sheet['Severity_Num'] == severity)
                ]
                
                if len(team_sla) > 0:
                    return team_sla.iloc[0]['TTR_Days']
                
                # Fallback to default if team/severity not found
                return self.sla_targets.get(severity, None)
            
            self.df['SLA Target (days)'] = self.df.apply(get_sla_target, axis=1)
            # Fill any missing values with defaults
            self.df['SLA Target (days)'] = self.df['SLA Target (days)'].fillna(
                self.df['Severity Numeric'].map(self.sla_targets)
            )
        else:
            # Fallback to simple severity-based mapping
            self.df['SLA Target (days)'] = self.df['Severity Numeric'].map(self.sla_targets)
        
    def analyze_kpis(self) -> Dict[str, Any]:
        """Analyze Key Performance Indicators"""
        # Only calculate for closed cases with valid resolution times (positive, non-null)
        closed_with_resolution = self.df[
            (self.df['Is Closed']) & 
            (self.df['Resolution Time (days)'].notna()) & 
            (self.df['Resolution Time (days)'] >= 0)
        ]
        
        kpis = {
            'total_cases': len(self.df),
            'closed_cases': self.df['Is Closed'].sum(),
            'open_cases': (~self.df['Is Closed']).sum(),
            'closure_rate': (self.df['Is Closed'].sum() / len(self.df)) * 100,
            'high_priority_cases': self.df['Is High Priority'].sum(),
            'critical_cases': self.df['Is Critical'].sum(),
            'avg_resolution_time': closed_with_resolution['Resolution Time (days)'].mean() if len(closed_with_resolution) > 0 else None,
            'median_resolution_time': closed_with_resolution['Resolution Time (days)'].median() if len(closed_with_resolution) > 0 else None,
            'cases_by_severity': self.df['Case Severity'].value_counts().to_dict(),
            'cases_by_status': self.df['CaseStatus'].value_counts().to_dict(),
            'cases_by_type': self.df['Case Type'].value_counts().to_dict(),
            'cases_by_assignment_group': self.df['AssignmentGroup'].value_counts().to_dict(),
        }
        
        # SLA Target is already calculated in prepare_data() based on team and severity from SLA sheet
        # Use the existing 'SLA Target (days)' column
        # Only use closed cases with valid resolution times for SLA compliance
        closed_cases = self.df[
            (self.df['Is Closed']) & 
            (self.df['Resolution Time (days)'].notna()) & 
            (self.df['Resolution Time (days)'] >= 0)
        ].copy()
        if len(closed_cases) > 0:
            closed_cases['SLA Met'] = closed_cases['Resolution Time (days)'] <= closed_cases['SLA Target (days)']
            kpis['sla_compliance_rate'] = (closed_cases['SLA Met'].sum() / len(closed_cases)) * 100
            kpis['sla_breaches'] = (~closed_cases['SLA Met']).sum()
        else:
            kpis['sla_compliance_rate'] = 0
            kpis['sla_breaches'] = 0
            
        self.insights['kpis'] = kpis
        return kpis
    
    def detect_patterns(self) -> Dict[str, Any]:
        """Detect patterns in case data"""
        patterns = {
            'temporal_patterns': self._analyze_temporal_patterns(),
            'severity_trends': self._analyze_severity_trends(),
            'case_type_patterns': self._analyze_case_type_patterns(),
            'assignment_group_patterns': self._analyze_assignment_group_patterns(),
            'source_patterns': self._analyze_source_patterns(),
            'status_transition_patterns': self._analyze_status_transitions(),
        }
        
        self.insights['patterns'] = patterns
        return patterns
    
    def _analyze_temporal_patterns(self) -> Dict[str, Any]:
        """Analyze time-based patterns"""
        self.df['Create Date'] = pd.to_datetime(self.df['Create Date'], errors='coerce')
        self.df['Day of Week'] = self.df['Create Date'].dt.day_name()
        self.df['Hour'] = self.df['Create Date'].dt.hour
        self.df['Date'] = self.df['Create Date'].dt.date
        
        return {
            'cases_by_day_of_week': self.df['Day of Week'].value_counts().to_dict(),
            'cases_by_hour': self.df['Hour'].value_counts().to_dict(),
            'daily_case_volume': self.df.groupby('Date').size().to_dict(),
            'peak_hours': self.df['Hour'].value_counts().head(5).to_dict(),
        }
    
    def _analyze_severity_trends(self) -> Dict[str, Any]:
        """Analyze severity distribution and trends"""
        severity_analysis = {
            'distribution': self.df['Case Severity'].value_counts().to_dict(),
            'severity_by_type': pd.crosstab(self.df['Case Type'], self.df['Case Severity']).to_dict(),
            'avg_resolution_by_severity': self.df[
                (self.df['Is Closed']) & 
                (self.df['Resolution Time (days)'].notna()) & 
                (self.df['Resolution Time (days)'] >= 0)
            ].groupby('Case Severity')['Resolution Time (days)'].mean().to_dict(),
        }
        
        # Identify severity escalation patterns
        high_severity_cases = self.df[self.df['Is High Priority']]
        severity_analysis['high_severity_by_group'] = high_severity_cases['AssignmentGroup'].value_counts().to_dict()
        severity_analysis['high_severity_by_type'] = high_severity_cases['Case Type'].value_counts().to_dict()
        
        return severity_analysis
    
    def _analyze_case_type_patterns(self) -> Dict[str, Any]:
        """Analyze patterns by case type"""
        type_analysis = {
            'most_common_types': self.df['Case Type'].value_counts().head(10).to_dict(),
            'type_by_severity': pd.crosstab(self.df['Case Type'], self.df['Case Severity']).to_dict(),
            'type_resolution_times': self.df[
                (self.df['Is Closed']) & 
                (self.df['Resolution Time (days)'].notna()) & 
                (self.df['Resolution Time (days)'] >= 0)
            ].groupby('Case Type')['Resolution Time (days)'].mean().to_dict(),
            'type_closure_rates': (self.df.groupby('Case Type')['Is Closed'].mean() * 100).to_dict(),
        }
        
        # Identify recurring issues
        type_analysis['recurring_issues'] = self._identify_recurring_issues()
        
        return type_analysis
    
    def _analyze_assignment_group_patterns(self) -> Dict[str, Any]:
        """Analyze patterns by assignment group"""
        group_analysis = {
            'case_distribution': self.df['AssignmentGroup'].value_counts().to_dict(),
            'group_workload': self.df['AssignmentGroup'].value_counts().to_dict(),
            'group_resolution_times': self.df[
                (self.df['Is Closed']) & 
                (self.df['Resolution Time (days)'].notna()) & 
                (self.df['Resolution Time (days)'] >= 0)
            ].groupby('AssignmentGroup')['Resolution Time (days)'].mean().to_dict(),
            'group_closure_rates': (self.df.groupby('AssignmentGroup')['Is Closed'].mean() * 100).to_dict(),
            'group_by_severity': pd.crosstab(self.df['AssignmentGroup'], self.df['Case Severity']).to_dict(),
        }
        
        # Identify bottlenecks
        group_analysis['bottlenecks'] = self._identify_bottlenecks()
        
        return group_analysis
    
    def _analyze_source_patterns(self) -> Dict[str, Any]:
        """Analyze patterns by case source"""
        source_analysis = {
            'source_distribution': self.df['Case Source'].value_counts().to_dict(),
            'source_by_severity': pd.crosstab(self.df['Case Source'], self.df['Case Severity']).to_dict(),
            'source_resolution_times': self.df[
                (self.df['Is Closed']) & 
                (self.df['Resolution Time (days)'].notna()) & 
                (self.df['Resolution Time (days)'] >= 0)
            ].groupby('Case Source')['Resolution Time (days)'].mean().to_dict(),
        }
        
        return source_analysis
    
    def _analyze_status_transitions(self) -> Dict[str, Any]:
        """Analyze case status patterns"""
        status_analysis = {
            'status_distribution': self.df['CaseStatus'].value_counts().to_dict(),
            'status_by_severity': pd.crosstab(self.df['CaseStatus'], self.df['Case Severity']).to_dict(),
            'stuck_cases': self._identify_stuck_cases(),
            'status_duration': self._calculate_status_durations(),
        }
        
        return status_analysis
    
    def identify_risks(self) -> Dict[str, Any]:
        """Identify risks and potential SLA breaches"""
        risks = {
            'sla_at_risk': self._identify_sla_at_risk(),
            'high_priority_open': self._identify_high_priority_open(),
            'aging_cases': self._identify_aging_cases(),
            'escalation_risks': self._identify_escalation_risks(),
        }
        
        self.insights['risks'] = risks
        return risks
    
    def _identify_sla_at_risk(self) -> List[Dict[str, Any]]:
        """Identify cases at risk of SLA breach"""
        open_cases = self.df[~self.df['Is Closed']].copy()
        if len(open_cases) == 0:
            return []
        
        open_cases['Days Open'] = (pd.Timestamp.now() - open_cases['Create Date']).dt.total_seconds() / 86400
        open_cases['SLA Risk'] = (open_cases['Days Open'] / open_cases['SLA Target (days)']) * 100
        
        at_risk = open_cases[open_cases['SLA Risk'] >= 75].sort_values('SLA Risk', ascending=False)
        
        return at_risk[['Case Id', 'Case Severity', 'Case Type', 'AssignmentGroup', 
                        'Days Open', 'SLA Target (days)', 'SLA Risk']].head(20).to_dict('records')
    
    def _identify_high_priority_open(self) -> List[Dict[str, Any]]:
        """Identify high priority cases that are still open"""
        high_priority_open = self.df[(self.df['Is High Priority']) & (~self.df['Is Closed'])].copy()
        high_priority_open['Days Open'] = (pd.Timestamp.now() - high_priority_open['Create Date']).dt.total_seconds() / 86400
        
        return high_priority_open[['Case Id', 'Case Severity', 'Case Type', 'AssignmentGroup', 
                                   'CaseStatus', 'Days Open']].to_dict('records')
    
    def _identify_aging_cases(self) -> List[Dict[str, Any]]:
        """Identify cases that have been open for extended periods"""
        open_cases = self.df[~self.df['Is Closed']].copy()
        open_cases['Days Open'] = (pd.Timestamp.now() - open_cases['Create Date']).dt.total_seconds() / 86400
        
        aging = open_cases[open_cases['Days Open'] > 30].sort_values('Days Open', ascending=False)
        
        return aging[['Case Id', 'Case Severity', 'Case Type', 'AssignmentGroup', 
                      'CaseStatus', 'Days Open']].head(20).to_dict('records')
    
    def _identify_escalation_risks(self) -> Dict[str, Any]:
        """Identify patterns that may lead to escalations"""
        # Cases with multiple updates but still open
        open_cases = self.df[~self.df['Is Closed']].copy()
        open_cases['Update Count'] = open_cases.groupby('Case Id').size()
        
        # Cases in certain statuses for too long
        status_risks = {}
        for status in ['Analysis', 'Contain', 'Review']:
            status_cases = open_cases[open_cases['CaseStatus'] == status]
            if len(status_cases) > 0:
                status_cases['Days in Status'] = (pd.Timestamp.now() - status_cases['Create Date']).dt.total_seconds() / 86400
                long_status = status_cases[status_cases['Days in Status'] > 7]
                status_risks[status] = len(long_status)
        
        return {
            'cases_stuck_in_status': status_risks,
            'high_update_count_cases': len(open_cases[open_cases['Update Count'] > 5]),
        }
    
    def identify_inefficiencies(self) -> Dict[str, Any]:
        """Identify process inefficiencies"""
        inefficiencies = {
            'bottlenecks': self._identify_bottlenecks(),
            'recurring_issues': self._identify_recurring_issues(),
            'process_gaps': self._identify_process_gaps(),
            'resource_utilization': self._analyze_resource_utilization(),
        }
        
        self.insights['inefficiencies'] = inefficiencies
        return inefficiencies
    
    def _identify_bottlenecks(self) -> Dict[str, Any]:
        """Identify bottlenecks in case processing"""
        bottlenecks = {}
        
        # Assignment groups with high workload and slow resolution
        group_metrics = self.df.groupby('AssignmentGroup').agg({
            'Case Id': 'count',
            'Resolution Time (days)': lambda x: x[self.df[self.df['AssignmentGroup'] == x.name]['Is Closed']].mean() if any(self.df[self.df['AssignmentGroup'] == x.name]['Is Closed']) else np.nan
        }).rename(columns={'Case Id': 'Case Count', 'Resolution Time (days)': 'Avg Resolution'})
        
        # Groups with high case count and slow resolution
        high_workload = group_metrics[group_metrics['Case Count'] > group_metrics['Case Count'].quantile(0.75)]
        slow_resolution = high_workload[high_workload['Avg Resolution'] > group_metrics['Avg Resolution'].quantile(0.75)]
        
        bottlenecks['high_workload_slow_resolution'] = slow_resolution.to_dict('index') if len(slow_resolution) > 0 else {}
        
        # Status bottlenecks
        status_counts = self.df['CaseStatus'].value_counts()
        bottlenecks['status_bottlenecks'] = status_counts[status_counts > status_counts.quantile(0.75)].to_dict()
        
        return bottlenecks
    
    def _identify_recurring_issues(self) -> List[Dict[str, Any]]:
        """Identify recurring case types and patterns"""
        recurring = []
        
        # Case types with high frequency
        type_counts = self.df['Case Type'].value_counts()
        high_frequency_types = type_counts[type_counts >= 5]
        
        for case_type in high_frequency_types.index:
            type_cases = self.df[self.df['Case Type'] == case_type]
            recurring.append({
                'case_type': case_type,
                'frequency': int(type_counts[case_type]),
                'avg_resolution_days': float(
                    type_cases[
                        (type_cases['Is Closed']) & 
                        (type_cases['Resolution Time (days)'].notna()) & 
                        (type_cases['Resolution Time (days)'] >= 0)
                    ]['Resolution Time (days)'].mean()
                ) if any(type_cases['Is Closed']) else None,
                'common_severity': type_cases['Case Severity'].mode().iloc[0] if len(type_cases['Case Severity'].mode()) > 0 else None,
                'common_summaries': type_cases['Case CurrentSummary'].value_counts().head(3).to_dict(),
            })
        
        return sorted(recurring, key=lambda x: x['frequency'], reverse=True)
    
    def _identify_process_gaps(self) -> Dict[str, Any]:
        """Identify gaps in processes"""
        gaps = {
            'missing_resolutions': len(self.df[(self.df['Is Closed']) & (self.df['Case Resolution'].isna())]),
            'cases_without_end_date': len(self.df[(self.df['Is Closed']) & (self.df['End Date'].isna())]),
            'draft_cases_old': len(self.df[(self.df['CaseStatus'] == 'Draft') & 
                                          ((pd.Timestamp.now() - self.df['Create Date']).dt.days > 7)]),
            'inconsistent_status': self._check_status_consistency(),
        }
        
        return gaps
    
    def _check_status_consistency(self) -> Dict[str, Any]:
        """Check for status inconsistencies"""
        inconsistencies = {}
        
        # Closed cases without end date
        closed_no_end = self.df[(self.df['CaseStatus'] == 'Closed') & (self.df['End Date'].isna())]
        inconsistencies['closed_without_end_date'] = len(closed_no_end)
        
        # Cases with end date but not closed
        end_not_closed = self.df[(self.df['End Date'].notna()) & (self.df['CaseStatus'] != 'Closed')]
        inconsistencies['end_date_but_not_closed'] = len(end_not_closed)
        
        return inconsistencies
    
    def _analyze_resource_utilization(self) -> Dict[str, Any]:
        """Analyze resource utilization across assignment groups"""
        utilization = {}
        
        for group in self.df['AssignmentGroup'].unique():
            group_cases = self.df[self.df['AssignmentGroup'] == group]
            utilization[group] = {
                'total_cases': len(group_cases),
                'open_cases': len(group_cases[~group_cases['Is Closed']]),
                'closed_cases': len(group_cases[group_cases['Is Closed']]),
                'high_priority_open': len(group_cases[(group_cases['Is High Priority']) & (~group_cases['Is Closed'])]),
                'avg_resolution_days': float(
                    group_cases[
                        (group_cases['Is Closed']) & 
                        (group_cases['Resolution Time (days)'].notna()) & 
                        (group_cases['Resolution Time (days)'] >= 0)
                    ]['Resolution Time (days)'].mean()
                ) if any(group_cases['Is Closed']) else None,
            }
        
        return utilization
    
    def _identify_stuck_cases(self) -> List[Dict[str, Any]]:
        """Identify cases stuck in certain statuses"""
        stuck = []
        
        for status in ['Analysis', 'Contain', 'Review', 'Draft']:
            status_cases = self.df[(self.df['CaseStatus'] == status) & (~self.df['Is Closed'])]
            if len(status_cases) > 0:
                status_cases = status_cases.copy()
                status_cases['Days in Status'] = (pd.Timestamp.now() - status_cases['Create Date']).dt.total_seconds() / 86400
                long_status = status_cases[status_cases['Days in Status'] > 10]
                
                for _, case in long_status.iterrows():
                    stuck.append({
                        'case_id': case['Case Id'],
                        'status': status,
                        'days_in_status': float(case['Days in Status']),
                        'severity': case['Case Severity'],
                        'assignment_group': case['AssignmentGroup'],
                    })
        
        return sorted(stuck, key=lambda x: x['days_in_status'], reverse=True)
    
    def _calculate_status_durations(self) -> Dict[str, float]:
        """Calculate average time in each status"""
        # Simplified - would need status history for accurate calculation
        status_durations = {}
        
        for status in self.df['CaseStatus'].unique():
            status_cases = self.df[self.df['CaseStatus'] == status]
            if len(status_cases) > 0:
                status_cases = status_cases.copy()
                status_cases['Days in Status'] = (pd.Timestamp.now() - status_cases['Create Date']).dt.total_seconds() / 86400
                status_durations[status] = float(status_cases['Days in Status'].mean())
        
        return status_durations
    
    def root_cause_analysis(self) -> Dict[str, Any]:
        """Perform root cause analysis"""
        rca = {
            'common_root_causes': self._identify_common_root_causes(),
            'case_type_correlations': self._analyze_case_type_correlations(),
            'severity_drivers': self._identify_severity_drivers(),
            'resolution_factors': self._analyze_resolution_factors(),
        }
        
        self.insights['root_cause_analysis'] = rca
        return rca
    
    def _identify_common_root_causes(self) -> List[Dict[str, Any]]:
        """Identify common root causes from case summaries"""
        # Analyze case summaries for common themes
        summary_analysis = {}
        
        # Group by case type and analyze summaries
        for case_type in self.df['Case Type'].unique():
            type_cases = self.df[self.df['Case Type'] == case_type]
            summaries = type_cases['Case CurrentSummary'].dropna()
            
            if len(summaries) > 0:
                # Extract common keywords/phrases
                common_phrases = {}
                for summary in summaries:
                    words = summary.lower().split()
                    for word in words:
                        if len(word) > 4:  # Filter short words
                            common_phrases[word] = common_phrases.get(word, 0) + 1
                
                # Get top phrases
                top_phrases = sorted(common_phrases.items(), key=lambda x: x[1], reverse=True)[:5]
                
                summary_analysis[case_type] = {
                    'frequency': len(type_cases),
                    'common_phrases': dict(top_phrases),
                    'avg_resolution': float(
                        type_cases[
                            (type_cases['Is Closed']) & 
                            (type_cases['Resolution Time (days)'].notna()) & 
                            (type_cases['Resolution Time (days)'] >= 0)
                        ]['Resolution Time (days)'].mean()
                    ) if any(type_cases['Is Closed']) else None,
                }
        
        return sorted(summary_analysis.items(), key=lambda x: x[1]['frequency'], reverse=True)
    
    def _analyze_case_type_correlations(self) -> Dict[str, Any]:
        """Analyze correlations between case types and other factors"""
        correlations = {
            'type_severity_correlation': pd.crosstab(self.df['Case Type'], self.df['Case Severity']).to_dict(),
            'type_source_correlation': pd.crosstab(self.df['Case Type'], self.df['Case Source']).to_dict(),
            'type_group_correlation': pd.crosstab(self.df['Case Type'], self.df['AssignmentGroup']).to_dict(),
        }
        
        return correlations
    
    def _identify_severity_drivers(self) -> Dict[str, Any]:
        """Identify factors that drive case severity"""
        drivers = {
            'source_severity': pd.crosstab(self.df['Case Source'], self.df['Case Severity']).to_dict(),
            'type_severity': pd.crosstab(self.df['Case Type'], self.df['Case Severity']).to_dict(),
            'high_severity_patterns': self.df[self.df['Is High Priority']].groupby('Case Type').size().to_dict(),
        }
        
        return drivers
    
    def _analyze_resolution_factors(self) -> Dict[str, Any]:
        """Analyze factors affecting resolution time"""
        # Only use closed cases with valid resolution times
        closed_cases = self.df[
            (self.df['Is Closed']) & 
            (self.df['Resolution Time (days)'].notna()) & 
            (self.df['Resolution Time (days)'] >= 0)
        ].copy()
        
        if len(closed_cases) == 0:
            return {}
        
        factors = {
            'resolution_by_type': closed_cases.groupby('Case Type')['Resolution Time (days)'].mean().to_dict(),
            'resolution_by_severity': closed_cases.groupby('Case Severity')['Resolution Time (days)'].mean().to_dict(),
            'resolution_by_group': closed_cases.groupby('AssignmentGroup')['Resolution Time (days)'].mean().to_dict(),
            'resolution_by_source': closed_cases.groupby('Case Source')['Resolution Time (days)'].mean().to_dict(),
        }
        
        return factors
    
    def generate_insights_report(self) -> Dict[str, Any]:
        """Generate comprehensive insights report"""
        # Run all analyses
        self.analyze_kpis()
        self.detect_patterns()
        self.identify_risks()
        self.identify_inefficiencies()
        self.root_cause_analysis()
        
        # Compile executive summary
        summary = {
            'executive_summary': {
                'total_cases': self.insights['kpis']['total_cases'],
                'closure_rate': round(self.insights['kpis']['closure_rate'], 2),
                'sla_compliance_rate': round(self.insights['kpis'].get('sla_compliance_rate', 0), 2),
                'high_priority_open': len(self.insights['risks']['high_priority_open']),
                'sla_at_risk_count': len(self.insights['risks']['sla_at_risk']),
                'aging_cases_count': len(self.insights['risks']['aging_cases']),
                'top_risk_areas': self._identify_top_risk_areas(),
            },
            'insights': self.insights,
            'recommendations': self._generate_recommendations(),
        }
        
        return summary
    
    def _identify_top_risk_areas(self) -> List[Dict[str, Any]]:
        """Identify top risk areas"""
        risks = []
        
        # High priority open cases by group
        high_priority = self.insights['risks']['high_priority_open']
        if high_priority:
            group_counts = {}
            for case in high_priority:
                group = case.get('AssignmentGroup', 'Unknown')
                group_counts[group] = group_counts.get(group, 0) + 1
            
            for group, count in sorted(group_counts.items(), key=lambda x: x[1], reverse=True)[:5]:
                risks.append({
                    'risk_type': 'High Priority Open Cases',
                    'area': group,
                    'count': count,
                    'severity': 'High',
                })
        
        # SLA at risk cases
        sla_risk = self.insights['risks']['sla_at_risk']
        if sla_risk:
            type_counts = {}
            for case in sla_risk:
                case_type = case.get('Case Type', 'Unknown')
                type_counts[case_type] = type_counts.get(case_type, 0) + 1
            
            for case_type, count in sorted(type_counts.items(), key=lambda x: x[1], reverse=True)[:3]:
                risks.append({
                    'risk_type': 'SLA At Risk',
                    'area': case_type,
                    'count': count,
                    'severity': 'High',
                })
        
        return risks
    
    def _generate_recommendations(self) -> List[Dict[str, Any]]:
        """Generate actionable recommendations"""
        recommendations = []
        
        # SLA compliance recommendations
        if self.insights['kpis'].get('sla_compliance_rate', 100) < 80:
            recommendations.append({
                'category': 'SLA Compliance',
                'priority': 'High',
                'recommendation': f"Improve SLA compliance (currently {self.insights['kpis'].get('sla_compliance_rate', 0):.1f}%). Focus on cases at risk of breach.",
                'action_items': [
                    'Review and prioritize cases approaching SLA deadlines',
                    'Reallocate resources to high-risk cases',
                    'Implement automated SLA monitoring alerts',
                ],
            })
        
        # Bottleneck recommendations
        bottlenecks = self.insights['inefficiencies']['bottlenecks']
        if bottlenecks.get('high_workload_slow_resolution'):
            recommendations.append({
                'category': 'Process Efficiency',
                'priority': 'High',
                'recommendation': 'Address bottlenecks in assignment groups with high workload and slow resolution',
                'action_items': [
                    'Review workload distribution across teams',
                    'Identify training needs for slow-resolving groups',
                    'Consider resource reallocation',
                ],
            })
        
        # Recurring issues recommendations
        recurring = self.insights['inefficiencies']['recurring_issues']
        if recurring:
            top_recurring = recurring[0] if recurring else None
            if top_recurring and top_recurring['frequency'] > 10:
                recommendations.append({
                    'category': 'Preventive Measures',
                    'priority': 'Medium',
                    'recommendation': f"Address recurring issue: {top_recurring['case_type']} (occurs {top_recurring['frequency']} times)",
                    'action_items': [
                        'Investigate root cause of recurring case type',
                        'Implement preventive controls',
                        'Create knowledge base articles for common resolution',
                    ],
                })
        
        # High priority open cases
        if len(self.insights['risks']['high_priority_open']) > 0:
            recommendations.append({
                'category': 'Risk Management',
                'priority': 'Critical',
                'recommendation': f"Immediately address {len(self.insights['risks']['high_priority_open'])} high priority open cases",
                'action_items': [
                    'Escalate high priority cases to management',
                    'Assign dedicated resources',
                    'Implement daily review process',
                ],
            })
        
        return recommendations
    
    def export_insights(self, output_file: str = 'pattern_recognition_insights.json'):
        """Export insights to JSON file"""
        report = self.generate_insights_report()
        
        # Convert numpy types to native Python types for JSON serialization
        def convert_types(obj):
            if isinstance(obj, (pd.Timestamp, datetime)):
                return obj.isoformat() if pd.notna(obj) else None
            elif isinstance(obj, (pd._libs.tslibs.nattype.NaTType, type(pd.NaT))):
                return None
            elif isinstance(obj, (date,)):
                return obj.isoformat()
            elif isinstance(obj, np.integer):
                return int(obj)
            elif isinstance(obj, np.floating):
                return float(obj)
            elif isinstance(obj, np.ndarray):
                return obj.tolist()
            elif isinstance(obj, dict):
                return {str(key): convert_types(value) for key, value in obj.items()}
            elif isinstance(obj, list):
                return [convert_types(item) for item in obj]
            elif pd.isna(obj):
                return None
            return obj
        
        report = convert_types(report)
        
        with open(output_file, 'w') as f:
            json.dump(report, f, indent=2, default=str)
        
        print(f"Insights exported to {output_file}")
        return report


if __name__ == "__main__":
    # Initialize pattern recognition
    analyzer = CDOPatternRecognition('DummyData.csv')
    
    # Generate comprehensive report
    print("Analyzing case data for patterns, risks, and inefficiencies...")
    report = analyzer.export_insights('pattern_recognition_insights.json')
    
    # Print executive summary
    print("\n" + "="*80)
    print("EXECUTIVE SUMMARY")
    print("="*80)
    summary = report['executive_summary']
    print(f"Total Cases: {summary['total_cases']}")
    print(f"Closure Rate: {summary['closure_rate']:.2f}%")
    print(f"SLA Compliance Rate: {summary['sla_compliance_rate']:.2f}%")
    print(f"High Priority Open Cases: {summary['high_priority_open']}")
    print(f"Cases at Risk of SLA Breach: {summary['sla_at_risk_count']}")
    print(f"Aging Cases (>30 days): {summary['aging_cases_count']}")
    
    print("\n" + "="*80)
    print("TOP RECOMMENDATIONS")
    print("="*80)
    for i, rec in enumerate(report['recommendations'][:5], 1):
        print(f"\n{i}. [{rec['priority']}] {rec['category']}: {rec['recommendation']}")
        print("   Action Items:")
        for item in rec['action_items']:
            print(f"   - {item}")
    
    print("\n" + "="*80)
    print(f"Full report saved to: pattern_recognition_insights.json")
    print("="*80)

