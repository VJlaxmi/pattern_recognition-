"""
CDO Monitoring & Oversight - AI-Enhanced Pattern Recognition
Integrates Azure OpenAI for natural language insights and recommendations
"""

import pandas as pd
import numpy as np
from datetime import datetime, date
import json
from typing import Dict, List, Tuple, Any, Optional
import warnings
import os
from openai import AzureOpenAI
from pattern_recognition_analysis import CDOPatternRecognition

warnings.filterwarnings('ignore')


class AIEnhancedPatternRecognition(CDOPatternRecognition):
    """Enhanced pattern recognition with Azure OpenAI integration"""
    
    def __init__(self, data_file: str, config_file: str = 'azure_openai_config.json', 
                 sla_sheet_file: str = "SLA_sheet.csv", sla_config: Dict[str, int] = None):
        """Initialize with case data and Azure OpenAI configuration"""
        super().__init__(data_file, sla_sheet_file=sla_sheet_file, sla_config=sla_config)
        self.load_azure_config(config_file)
        self.openai_client = None
        if self.azure_config:
            self.init_openai_client()
    
    def load_azure_config(self, config_file: str):
        """Load Azure OpenAI configuration"""
        try:
            with open(config_file, 'r') as f:
                config = json.load(f)
                self.azure_config = config.get('azure_openai', {})
        except FileNotFoundError:
            print(f"Config file {config_file} not found. Using environment variables.")
            self.azure_config = {
                'endpoint': os.getenv('AZURE_OPENAI_ENDPOINT'),
                'api_key': os.getenv('AZURE_OPENAI_API_KEY'),
                'api_version': os.getenv('AZURE_OPENAI_API_VERSION', '2024-02-15-preview'),
                'deployment_name': os.getenv('AZURE_OPENAI_DEPLOYMENT', 'gpt-4o'),
                'embeddings_deployment': os.getenv('AZURE_OPENAI_EMBEDDINGS_DEPLOYMENT', 'text-embedding-ada-002'),
            }
    
    def init_openai_client(self):
        """Initialize Azure OpenAI client"""
        if not self.azure_config.get('endpoint') or not self.azure_config.get('api_key'):
            print("Azure OpenAI configuration incomplete. AI features disabled.")
            return
        
        try:
            self.openai_client = AzureOpenAI(
                api_key=self.azure_config['api_key'],
                api_version=self.azure_config['api_version'],
                azure_endpoint=self.azure_config['endpoint']
            )
            print("Azure OpenAI client initialized successfully.")
        except Exception as e:
            print(f"Failed to initialize Azure OpenAI client: {e}")
            self.openai_client = None
    
    def generate_ai_insights(self, insights_summary: Dict[str, Any]) -> str:
        """Generate AI-powered natural language insights"""
        if not self.openai_client:
            return "AI insights unavailable - Azure OpenAI not configured."
        
        # Convert data types for JSON serialization
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
        
        insights_clean = convert_for_json(insights_summary)
        
        prompt = f"""You are an expert analyst for CDO Monitoring & Oversight. Analyze the following case management insights and provide:

1. Executive Summary (2-3 sentences)
2. Top 3 Critical Risks requiring immediate attention
3. Key Patterns and Trends
4. Root Cause Analysis Summary
5. Actionable Recommendations (prioritized)

Case Management Insights:
{json.dumps(insights_clean, indent=2, default=str)}

Provide clear, actionable insights that help leadership make data-driven decisions."""

        try:
            response = self.openai_client.chat.completions.create(
                model=self.azure_config['deployment_name'],
                messages=[
                    {"role": "system", "content": "You are an expert business analyst specializing in operational intelligence and risk management."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=1500
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error generating AI insights: {str(e)}"
    
    def generate_risk_analysis(self, risks: Dict[str, Any]) -> str:
        """Generate AI-powered risk analysis"""
        if not self.openai_client:
            return "AI risk analysis unavailable."
        
        # Convert data types for JSON serialization
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
        
        risks_clean = convert_for_json(risks)
        
        prompt = f"""Analyze these case management risks and provide:

1. Risk Severity Assessment (Critical/High/Medium/Low)
2. Impact Analysis (potential business impact)
3. Urgency Assessment (immediate/short-term/long-term)
4. Mitigation Strategies

Risks Identified:
{json.dumps(risks_clean, indent=2, default=str)}

Focus on actionable risk mitigation strategies."""

        try:
            response = self.openai_client.chat.completions.create(
                model=self.azure_config['deployment_name'],
                messages=[
                    {"role": "system", "content": "You are a risk management expert specializing in operational risk assessment."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=1000
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error generating risk analysis: {str(e)}"
    
    def generate_recommendations(self, inefficiencies: Dict[str, Any], patterns: Dict[str, Any]) -> str:
        """Generate AI-powered recommendations"""
        if not self.openai_client:
            return "AI recommendations unavailable."
        
        # Convert data types for JSON serialization
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
        
        inefficiencies_clean = convert_for_json(inefficiencies)
        patterns_clean = convert_for_json(patterns)
        
        prompt = f"""Based on these case management inefficiencies and patterns, provide prioritized recommendations:

1. Immediate Actions (next 24-48 hours)
2. Short-term Improvements (next week)
3. Long-term Strategic Changes (next month+)

Inefficiencies:
{json.dumps(inefficiencies_clean, indent=2, default=str)}

Patterns:
{json.dumps(patterns_clean, indent=2, default=str)}

Provide specific, actionable recommendations with expected impact."""

        try:
            response = self.openai_client.chat.completions.create(
                model=self.azure_config['deployment_name'],
                messages=[
                    {"role": "system", "content": "You are a process improvement consultant specializing in operational efficiency."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.4,
                max_tokens=1200
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error generating recommendations: {str(e)}"
    
    def summarize_case_type(self, case_type: str, cases: pd.DataFrame) -> str:
        """Generate AI summary for a specific case type"""
        if not self.openai_client:
            return "AI summary unavailable."
        
        case_summaries = cases['Case CurrentSummary'].dropna().tolist()[:10]  # Limit to 10 for context
        
        prompt = f"""Analyze this case type and provide insights:

Case Type: {case_type}
Number of Cases: {len(cases)}
Case Summaries (sample):
{chr(10).join(case_summaries)}

Provide:
1. Common characteristics
2. Typical resolution patterns
3. Root cause themes
4. Prevention strategies"""

        try:
            response = self.openai_client.chat.completions.create(
                model=self.azure_config['deployment_name'],
                messages=[
                    {"role": "system", "content": "You are a security operations analyst specializing in case analysis."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=800
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error generating case type summary: {str(e)}"
    
    def generate_ai_enhanced_report(self) -> Dict[str, Any]:
        """Generate comprehensive report with AI enhancements"""
        # Run base analysis
        base_report = self.generate_insights_report()
        
        if not self.openai_client:
            base_report['ai_enhanced'] = False
            base_report['ai_message'] = "Azure OpenAI not configured. Using base analysis only."
            return base_report
        
        print("Generating AI-enhanced insights...")
        
        # Generate AI insights
        executive_summary = {
            'total_cases': base_report['executive_summary']['total_cases'],
            'closure_rate': base_report['executive_summary']['closure_rate'],
            'sla_compliance_rate': base_report['executive_summary']['sla_compliance_rate'],
            'high_priority_open': base_report['executive_summary']['high_priority_open'],
            'sla_at_risk_count': base_report['executive_summary']['sla_at_risk_count'],
        }
        
        ai_insights = {
            'executive_summary_ai': self.generate_ai_insights(executive_summary),
            'risk_analysis_ai': self.generate_risk_analysis(base_report['insights']['risks']),
            'recommendations_ai': self.generate_recommendations(
                base_report['insights']['inefficiencies'],
                base_report['insights']['patterns']
            ),
        }
        
        # Generate summaries for top recurring issues
        recurring_issues = base_report['insights']['inefficiencies'].get('recurring_issues', [])
        if recurring_issues:
            top_issue = recurring_issues[0]
            case_type = top_issue['case_type']
            type_cases = self.df[self.df['Case Type'] == case_type]
            ai_insights[f'case_type_analysis_{case_type}'] = self.summarize_case_type(case_type, type_cases)
        
        base_report['ai_enhanced'] = True
        base_report['ai_insights'] = ai_insights
        
        return base_report
    
    def export_ai_enhanced_insights(self, output_file: str = 'pattern_recognition_ai_insights.json'):
        """Export AI-enhanced insights to JSON file"""
        report = self.generate_ai_enhanced_report()
        
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
        
        print(f"AI-enhanced insights exported to {output_file}")
        return report


if __name__ == "__main__":
    # Initialize AI-enhanced analyzer
    print("Initializing AI-Enhanced Pattern Recognition...")
    analyzer = AIEnhancedPatternRecognition('DummyData.csv', 'azure_openai_config.json')
    
    # Generate comprehensive AI-enhanced report
    print("\nGenerating comprehensive analysis with AI insights...")
    report = analyzer.export_ai_enhanced_insights('pattern_recognition_ai_insights.json')
    
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
    
    # Print AI insights if available
    if report.get('ai_enhanced'):
        print("\n" + "="*80)
        print("AI-GENERATED INSIGHTS")
        print("="*80)
        ai_insights = report.get('ai_insights', {})
        if 'executive_summary_ai' in ai_insights:
            print("\nExecutive Summary (AI):")
            print(ai_insights['executive_summary_ai'])
        
        if 'risk_analysis_ai' in ai_insights:
            print("\n" + "-"*80)
            print("Risk Analysis (AI):")
            print(ai_insights['risk_analysis_ai'])
        
        if 'recommendations_ai' in ai_insights:
            print("\n" + "-"*80)
            print("Recommendations (AI):")
            print(ai_insights['recommendations_ai'])
    else:
        print("\nAI enhancements not available. Check Azure OpenAI configuration.")
    
    print("\n" + "="*80)
    print(f"Full report saved to: pattern_recognition_ai_insights.json")
    print("="*80)

