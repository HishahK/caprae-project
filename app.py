"""
Caprae Capital Lead Generation Tool
==================================

Enhanced web-based lead processing and generation tool that demonstrates 
understanding of SaaSquatchLeads.com workflow and provides:
- Web scraping capabilities from multiple sources
- Interactive dashboard for lead management
- Intelligent scoring and enrichment
- Personalized email generation
- Export functionality

Based on analysis of SaaSquatchLeads reference tool which provides:
- Multi-source data aggregation (Apollo, LinkedIn, Crunchbase, Google Maps)
- Real-time enrichment and verification
- Automated workflow for searchers and operators
- AI-powered outreach tools
"""

from flask import Flask, render_template, request, jsonify, send_file
import csv
import json
import os
import io
import requests
from datetime import datetime
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional
import time
import random

app = Flask(__name__)

@dataclass
class Lead:
    """Enhanced Lead dataclass with additional enrichment fields"""
    first_name: str
    last_name: str
    company_name: str
    title: str
    revenue: str
    industry: str
    email: str
    phone: str = ""
    linkedin_url: str = ""
    website: str = ""
    location: str = ""
    employees: str = ""
    source: str = ""
    score: int = 0
    email_template: str = ""
    enriched: bool = False
    created_date: str = ""

class LeadProcessor:
    """Core lead processing engine inspired by SaaSquatchLeads workflow"""
    
    def __init__(self):
        self.leads: List[Lead] = []
        self.processed_count = 0
        
    def score_title(self, title: str) -> int:
        """Enhanced scoring based on SaaSquatchLeads decision-maker focus"""
        title_lower = title.lower()
        # C-level executives (highest priority for acquisition deals)
        if any(key in title_lower for key in ["ceo", "chief executive", "founder", "president"]):
            return 10
        if any(key in title_lower for key in ["cfo", "chief financial"]):
            return 9
        if any(key in title_lower for key in ["cto", "chief technology", "chief technical"]):
            return 8
        # VP/SVP level (strong decision makers)
        if any(key in title_lower for key in ["vp", "vice president", "svp"]):
            return 7
        # Directors (good influencers)
        if any(key in title_lower for key in ["director", "head of"]):
            return 5
        # Managers (entry level contacts)
        if any(key in title_lower for key in ["manager", "lead"]):
            return 3
        return 1
    
    def score_revenue(self, revenue: str) -> int:
        """Revenue scoring aligned with acquisition targets"""
        try:
            rev_num = float(revenue.replace("$", "").replace(",", "").replace("M", "000000").replace("B", "000000000"))
            # Sweet spot for acquisitions ($10M-$100M ARR)
            if 10_000_000 <= rev_num <= 100_000_000:
                return 10
            elif 5_000_000 <= rev_num < 10_000_000:
                return 8
            elif 1_000_000 <= rev_num < 5_000_000:
                return 6
            elif rev_num > 100_000_000:
                return 4  # May be too large for typical search fund
            else:
                return 2
        except:
            return 1
    
    def score_industry(self, industry: str) -> int:
        """Industry scoring for acquisition appeal"""
        industry_lower = industry.lower()
        # High-value SaaS and tech
        if any(key in industry_lower for key in ["saas", "software", "technology", "fintech"]):
            return 8
        # Recurring revenue businesses
        if any(key in industry_lower for key in ["subscription", "membership", "recurring"]):
            return 7
        # Traditional high-margin businesses
        if any(key in industry_lower for key in ["healthcare", "education", "consulting"]):
            return 6
        # Manufacturing and services
        if any(key in industry_lower for key in ["manufacturing", "logistics", "distribution"]):
            return 4
        return 2
    
    def calculate_score(self, lead: Lead) -> int:
        """Calculate composite lead score"""
        title_score = self.score_title(lead.title)
        revenue_score = self.score_revenue(lead.revenue)
        industry_score = self.score_industry(lead.industry)
        
        # Bonus points for complete contact info (like SaaSquatchLeads enrichment)
        enrichment_bonus = 0
        if lead.phone: enrichment_bonus += 2
        if lead.linkedin_url: enrichment_bonus += 2
        if lead.website: enrichment_bonus += 1
        
        return title_score + revenue_score + industry_score + enrichment_bonus
    
    def generate_personalized_email(self, lead: Lead) -> str:
        """Generate AI-inspired personalized outreach templates"""
        templates = {
            "high_exec": f"""Subject: Quick chat about {lead.company_name}'s growth trajectory

Hi {lead.first_name},

Hope you're doing well. As {lead.title} at {lead.company_name}, you're probably focused on scaling operations and exploring strategic opportunities.

At Caprae Capital, we specialize in partnering with {lead.industry.lower()} companies like yours to accelerate growth through our operator-first approach. Rather than just capital, we bring hands-on operational expertise.

Would you be open to a brief conversation about {lead.company_name}'s growth plans?

Best regards,
[Your Name]
Caprae Capital Partners""",
            
            "mid_level": f"""Subject: Operational efficiency insights for {lead.company_name}

Hi {lead.first_name},

I came across {lead.company_name} and was impressed by your position in the {lead.industry.lower()} space.

As {lead.title}, you likely see firsthand the operational challenges that come with growth. At Caprae Capital, we've helped similar companies streamline operations and unlock new opportunities through our SaaS and M&A-as-a-Service models.

Would you be interested in a quick call to discuss how we could support {lead.company_name}'s operational goals?

Best,
[Your Name]
Caprae Capital""",
            
            "standard": f"""Subject: Partnership opportunity for {lead.company_name}

Hello {lead.first_name},

I hope this message finds you well. I'm reaching out because {lead.company_name} caught our attention as an innovative player in the {lead.industry.lower()} sector.

At Caprae Capital, we focus on empowering businesses through strategic partnerships and operational support. Our unique approach combines capital with hands-on expertise to help companies achieve sustainable growth.

I'd love to explore how we might be able to support {lead.company_name}'s objectives.

Kind regards,
[Your Name]
Caprae Capital Partners"""
        }
        
        score = self.calculate_score(lead)
        if score >= 20:
            return templates["high_exec"]
        elif score >= 15:
            return templates["mid_level"]
        else:
            return templates["standard"]
    
    def enrich_lead(self, lead: Lead) -> Lead:
        """Simulate lead enrichment like SaaSquatchLeads"""
        # In real implementation, this would call APIs for enrichment
        enrichment_data = self.mock_enrichment(lead)
        
        lead.phone = enrichment_data.get("phone", "")
        lead.linkedin_url = enrichment_data.get("linkedin", "")
        lead.website = enrichment_data.get("website", "")
        lead.location = enrichment_data.get("location", "")
        lead.employees = enrichment_data.get("employees", "")
        lead.enriched = True
        
        return lead
    
    def mock_enrichment(self, lead: Lead) -> Dict:
        """Mock data enrichment for demo purposes"""
        # Simulate API response delay
        time.sleep(0.1)
        
        mock_data = {
            "phone": f"+1-{random.randint(100,999)}-{random.randint(100,999)}-{random.randint(1000,9999)}",
            "linkedin": f"https://linkedin.com/in/{lead.first_name.lower()}-{lead.last_name.lower()}",
            "website": f"https://www.{lead.company_name.lower().replace(' ', '')}.com",
            "location": random.choice(["New York, NY", "San Francisco, CA", "Austin, TX", "Seattle, WA"]),
            "employees": random.choice(["10-50", "51-200", "201-500", "501-1000"])
        }
        
        return mock_data
    
    def scrape_mock_leads(self, source: str, query: str) -> List[Lead]:
        """Mock web scraping functionality inspired by SaaSquatchLeads sources"""
        # In real implementation, this would scrape from actual sources
        mock_leads = []
        
        if source == "apollo":
            mock_leads = self.generate_apollo_mock_data(query)
        elif source == "linkedin":
            mock_leads = self.generate_linkedin_mock_data(query)
        elif source == "crunchbase":
            mock_leads = self.generate_crunchbase_mock_data(query)
        elif source == "google_maps":
            mock_leads = self.generate_google_maps_mock_data(query)
        
        return mock_leads
    
    def generate_apollo_mock_data(self, query: str) -> List[Lead]:
        """Mock Apollo.io data"""
        apollo_leads = [
            Lead("Sarah", "Chen", "TechVenture", "CEO", "25000000", "Technology", 
                 "sarah.chen@techventure.com", source="Apollo"),
            Lead("Michael", "Roberts", "DataFlow", "CTO", "15000000", "Software",
                 "m.roberts@dataflow.com", source="Apollo"),
            Lead("Jennifer", "Kim", "CloudScale", "VP Engineering", "40000000", "SaaS",
                 "jennifer.kim@cloudscale.com", source="Apollo")
        ]
        return apollo_leads
    
    def generate_linkedin_mock_data(self, query: str) -> List[Lead]:
        """Mock LinkedIn Sales Navigator data"""
        linkedin_leads = [
            Lead("David", "Thompson", "InnovaCorp", "CFO", "35000000", "Fintech",
                 "david.thompson@innovacorp.com", source="LinkedIn"),
            Lead("Lisa", "Wang", "GrowthLabs", "VP Sales", "12000000", "Marketing Tech",
                 "lisa.wang@growthlabs.com", source="LinkedIn")
        ]
        return linkedin_leads
    
    def generate_crunchbase_mock_data(self, query: str) -> List[Lead]:
        """Mock Crunchbase data"""
        crunchbase_leads = [
            Lead("Robert", "Martinez", "ScaleUp", "Founder", "8000000", "E-commerce",
                 "robert@scaleup.com", source="Crunchbase"),
            Lead("Amanda", "Foster", "NextGen", "Co-Founder", "20000000", "Healthcare Tech",
                 "amanda.foster@nextgen.com", source="Crunchbase")
        ]
        return crunchbase_leads
    
    def generate_google_maps_mock_data(self, query: str) -> List[Lead]:
        """Mock Google Maps business data"""
        gmaps_leads = [
            Lead("James", "Wilson", "Local Solutions", "Owner", "2000000", "Services",
                 "james@localsolutions.com", source="Google Maps"),
            Lead("Maria", "Garcia", "Regional Consulting", "Principal", "5000000", "Consulting",
                 "maria.garcia@regionalconsulting.com", source="Google Maps")
        ]
        return gmaps_leads
    
    def process_leads(self, leads: List[Lead]) -> List[Lead]:
        """Process and score leads"""
        processed = []
        seen_emails = set()
        
        for lead in leads:
            # Remove duplicates
            if lead.email in seen_emails:
                continue
            seen_emails.add(lead.email)
            
            # Enrich lead data
            lead = self.enrich_lead(lead)
            
            # Calculate score
            lead.score = self.calculate_score(lead)
            
            # Generate email template
            lead.email_template = self.generate_personalized_email(lead)
            
            # Add timestamp
            lead.created_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            processed.append(lead)
        
        # Sort by score (highest first)
        processed.sort(key=lambda x: x.score, reverse=True)
        return processed

# Initialize global processor
processor = LeadProcessor()

@app.route('/')
def dashboard():
    """Main dashboard page"""
    return render_template('dashboard.html')

@app.route('/api/scrape', methods=['POST'])
def scrape_leads():
    """API endpoint for scraping leads from various sources"""
    data = request.get_json()
    source = data.get('source', 'apollo')
    query = data.get('query', '')
    
    # Simulate scraping delay
    time.sleep(1)
    
    try:
        scraped_leads = processor.scrape_mock_leads(source, query)
        processed_leads = processor.process_leads(scraped_leads)
        
        # Store in global processor
        processor.leads.extend(processed_leads)
        processor.processed_count += len(processed_leads)
        
        return jsonify({
            'success': True,
            'leads': [asdict(lead) for lead in processed_leads],
            'count': len(processed_leads)
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/upload', methods=['POST'])
def upload_csv():
    """Upload and process CSV file"""
    if 'file' not in request.files:
        return jsonify({'success': False, 'error': 'No file uploaded'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'success': False, 'error': 'No file selected'}), 400
    
    try:
        # Read CSV data
        stream = io.StringIO(file.stream.read().decode("UTF8"), newline=None)
        csv_input = csv.DictReader(stream)
        
        leads = []
        for row in csv_input:
            lead = Lead(
                first_name=row.get('first_name', ''),
                last_name=row.get('last_name', ''),
                company_name=row.get('company_name', ''),
                title=row.get('title', ''),
                revenue=row.get('revenue', ''),
                industry=row.get('industry', ''),
                email=row.get('email', ''),
                phone=row.get('phone', ''),
                source='CSV Upload'
            )
            leads.append(lead)
        
        processed_leads = processor.process_leads(leads)
        processor.leads.extend(processed_leads)
        
        return jsonify({
            'success': True,
            'leads': [asdict(lead) for lead in processed_leads],
            'count': len(processed_leads)
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Error processing file: {str(e)}'
        }), 500

@app.route('/api/leads')
def get_leads():
    """Get all processed leads with filtering"""
    min_score = request.args.get('min_score', 0, type=int)
    industry = request.args.get('industry', '')
    source = request.args.get('source', '')
    
    filtered_leads = processor.leads
    
    if min_score > 0:
        filtered_leads = [lead for lead in filtered_leads if lead.score >= min_score]
    
    if industry:
        filtered_leads = [lead for lead in filtered_leads if industry.lower() in lead.industry.lower()]
    
    if source:
        filtered_leads = [lead for lead in filtered_leads if source.lower() in lead.source.lower()]
    
    return jsonify({
        'leads': [asdict(lead) for lead in filtered_leads],
        'total_count': len(processor.leads),
        'filtered_count': len(filtered_leads)
    })

@app.route('/api/export')
def export_leads():
    """Export leads to CSV"""
    output = io.StringIO()
    fieldnames = [
        'first_name', 'last_name', 'company_name', 'title', 'revenue', 
        'industry', 'email', 'phone', 'linkedin_url', 'website', 
        'location', 'employees', 'source', 'score', 'created_date'
    ]
    
    writer = csv.DictWriter(output, fieldnames=fieldnames)
    writer.writeheader()
    
    for lead in processor.leads:
        row = asdict(lead)
        # Remove email_template for CSV export (too large)
        row.pop('email_template', None)
        row.pop('enriched', None)
        writer.writerow(row)
    
    output.seek(0)
    
    return send_file(
        io.BytesIO(output.getvalue().encode()),
        mimetype='text/csv',
        as_attachment=True,
        download_name=f'caprae_leads_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
    )

@app.route('/api/clear', methods=['DELETE'])
def clear_data():
    """Clear all lead data"""
    try:
        # Clear the global processor data
        processor.leads.clear()
        processor.processed_count = 0
        
        return jsonify({
            'success': True,
            'message': 'All lead data has been cleared successfully'
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Error clearing data: {str(e)}'
        }), 500

@app.route('/api/delete-lead/<int:lead_index>', methods=['DELETE'])
def delete_single_lead(lead_index):
    """Delete a single lead by index"""
    try:
        if 0 <= lead_index < len(processor.leads):
            deleted_lead = processor.leads.pop(lead_index)
            return jsonify({
                'success': True,
                'message': f'Lead {deleted_lead.first_name} {deleted_lead.last_name} deleted successfully'
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Lead not found'
            }), 404
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Error deleting lead: {str(e)}'
        }), 500

@app.route('/api/bulk-delete', methods=['DELETE'])
def bulk_delete_leads():
    """Delete multiple leads by their indices"""
    data = request.get_json()
    indices = data.get('indices', [])
    
    if not indices:
        return jsonify({
            'success': False,
            'error': 'No lead indices provided'
        }), 400
    
    try:
        # Sort indices in reverse order to avoid index shifting issues
        indices.sort(reverse=True)
        deleted_count = 0
        
        for index in indices:
            if 0 <= index < len(processor.leads):
                processor.leads.pop(index)
                deleted_count += 1
        
        return jsonify({
            'success': True,
            'message': f'Successfully deleted {deleted_count} leads',
            'deleted_count': deleted_count
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Error during bulk delete: {str(e)}'
        }), 500

@app.route('/api/stats')
def get_stats():
    """Get dashboard statistics"""
    leads = processor.leads
    
    if not leads:
        return jsonify({
            'total_leads': 0,
            'avg_score': 0,
            'top_industries': [],
            'source_breakdown': {},
            'score_distribution': {}
        })
    
    # Calculate statistics
    total_leads = len(leads)
    avg_score = sum(lead.score for lead in leads) / total_leads
    
    # Top industries
    industry_counts = {}
    for lead in leads:
        industry_counts[lead.industry] = industry_counts.get(lead.industry, 0) + 1
    top_industries = sorted(industry_counts.items(), key=lambda x: x[1], reverse=True)[:5]
    
    # Source breakdown
    source_counts = {}
    for lead in leads:
        source_counts[lead.source] = source_counts.get(lead.source, 0) + 1
    
    # Score distribution
    score_ranges = {'0-10': 0, '11-15': 0, '16-20': 0, '21+': 0}
    for lead in leads:
        if lead.score <= 10:
            score_ranges['0-10'] += 1
        elif lead.score <= 15:
            score_ranges['11-15'] += 1
        elif lead.score <= 20:
            score_ranges['16-20'] += 1
        else:
            score_ranges['21+'] += 1
    
    return jsonify({
        'total_leads': total_leads,
        'avg_score': round(avg_score, 1),
        'top_industries': top_industries,
        'source_breakdown': source_counts,
        'score_distribution': score_ranges
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)