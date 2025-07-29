"""
lead_tool.py
===============

This script processes a CSV of raw leads, removes duplicates, computes a simple
lead score based on heuristics, and generates a personalised outreach email for
each contact. The output is written to a new CSV with additional columns for
score and email template. A summary of the results is printed to the console.

Usage:
    python lead_tool.py --input dataset.csv --output processed_leads.csv

The input CSV is expected to have the following columns:

    first_name,last_name,company_name,title,revenue,industry,email

Revenue should be expressed either as a numeric string (e.g. "1000000")
representing annual revenue in USD, or as a descriptor such as "small",
"medium", or "large".

The script will deduplicate rows based on the email address. If an email
appears more than once in the input file, only the first occurrence is kept.

The lead score is calculated as the sum of individual subscores:

* Title score: High-ranking roles (e.g. CEO, CFO, CTO) receive more points.
* Revenue score: Larger companies receive more points.
* Industry score: Certain industries may be weighted higher based on
  typical value to Caprae Capital.

You can extend or modify the scoring logic by editing the `_score_title`,
`_score_revenue`, and `_score_industry` functions below.
"""

import argparse
import csv
from dataclasses import dataclass
from typing import Dict, List


@dataclass
class Lead:
    """Dataclass to store lead information and calculated attributes."""
    first_name: str
    last_name: str
    company_name: str
    title: str
    revenue: str
    industry: str
    email: str
    score: int = 0
    email_template: str = ""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Process and score leads from a CSV, removing duplicates."
    )
    parser.add_argument(
        "--input",
        required=True,
        help="Path to the input CSV containing raw leads.",
    )
    parser.add_argument(
        "--output",
        required=True,
        help="Path to write the processed leads CSV with scores and emails.",
    )
    return parser.parse_args()


def read_leads(csv_path: str) -> List[Lead]:
    """Read leads from a CSV file into Lead objects."""
    leads: List[Lead] = []
    with open(csv_path, newline="", encoding="utf-8") as infile:
        reader = csv.DictReader(infile)
        for row in reader:
            lead = Lead(
                first_name=row.get("first_name", "").strip(),
                last_name=row.get("last_name", "").strip(),
                company_name=row.get("company_name", "").strip(),
                title=row.get("title", "").strip(),
                revenue=row.get("revenue", "").strip(),
                industry=row.get("industry", "").strip(),
                email=row.get("email", "").strip().lower(),
            )
            leads.append(lead)
    return leads


def _score_title(title: str) -> int:
    """Assign a score based on the job title."""
    title_lower = title.lower()
    if any(key in title_lower for key in ["ceo", "chief executive"]):
        return 5
    if any(key in title_lower for key in ["cfo", "chief financial"]):
        return 5
    if any(key in title_lower for key in ["cto", "chief technology"]):
        return 4
    if any(key in title_lower for key in ["vp", "vice president"]):
        return 3
    if any(key in title_lower for key in ["manager", "director"]):
        return 2
    # Default minimal score for other titles
    return 1


def _parse_revenue(revenue: str) -> float:
    """Try to parse revenue into a float. Fails gracefully to 0."""
    revenue = revenue.replace("$", "").replace(",", "").strip().lower()
    if revenue in ("small", "medium", "large"):
        # Assign arbitrary numeric values for descriptive revenue sizes
        return {"small": 5e6, "medium": 100e6, "large": 1e9}[revenue]
    try:
        return float(revenue)
    except ValueError:
        return 0.0


def _score_revenue(revenue: str) -> int:
    """Assign a score based on company revenue."""
    rev = _parse_revenue(revenue)
    if rev >= 500e6:
        return 5
    if rev >= 100e6:
        return 4
    if rev >= 10e6:
        return 3
    if rev >= 1e6:
        return 2
    return 1


def _score_industry(industry: str) -> int:
    """Assign a score based on industry alignment."""
    industry_lower = industry.lower()
    # Customize these values based on Caprae's target sectors
    if any(key in industry_lower for key in ["technology", "software"]):
        return 4
    if any(key in industry_lower for key in ["health", "biotech"]):
        return 3
    if any(key in industry_lower for key in ["manufacturing", "industrial"]):
        return 2
    # Default minimal score
    return 1


def score_lead(lead: Lead) -> None:
    """Compute the total score for a single lead and generate an email."""
    title_score = _score_title(lead.title)
    revenue_score = _score_revenue(lead.revenue)
    industry_score = _score_industry(lead.industry)
    lead.score = title_score + revenue_score + industry_score
    lead.email_template = generate_email(lead)


def generate_email(lead: Lead) -> str:
    """Generate a personalised email template for the given lead."""
    lines = [
        f"Subject: Empowering {lead.company_name} to scale", "",
        f"Hi {lead.first_name},",
        "",
        f"I hope you're doing well. I'm reaching out because, as {lead.title} at {lead.company_name}, you play an essential role in driving growth.",
        "At Caprae Capital, we've developed a lightweight tool that helps entrepreneurs streamline operations, uncover opportunities, and close more deals.",
        f"I’d love to schedule a quick call to discuss how we can support {lead.company_name} in reaching its next milestone.",
        "",
        "Best regards,",
        "Your Name",
        "Caprae Capital"
    ]
    return "\n".join(lines)


def remove_duplicates(leads: List[Lead]) -> List[Lead]:
    """Remove duplicate leads based on email address."""
    seen_emails: Dict[str, bool] = {}
    unique_leads: List[Lead] = []
    for lead in leads:
        if lead.email and lead.email not in seen_emails:
            seen_emails[lead.email] = True
            unique_leads.append(lead)
    return unique_leads


def write_leads(leads: List[Lead], csv_path: str) -> None:
    """Write leads with scores and email templates to a CSV file."""
    fieldnames = [
        "first_name",
        "last_name",
        "company_name",
        "title",
        "revenue",
        "industry",
        "email",
        "score",
        "email_template",
    ]
    with open(csv_path, "w", newline="", encoding="utf-8") as outfile:
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        for lead in leads:
            writer.writerow({
                "first_name": lead.first_name,
                "last_name": lead.last_name,
                "company_name": lead.company_name,
                "title": lead.title,
                "revenue": lead.revenue,
                "industry": lead.industry,
                "email": lead.email,
                "score": lead.score,
                "email_template": lead.email_template,
            })


def print_summary(leads: List[Lead], duplicates_removed: int) -> None:
    """Print a summary of processed leads to the console."""
    print(f"Processed {len(leads)} unique leads (removed {duplicates_removed} duplicates).")
    # Show top 5 leads by score
    top_leads = sorted(leads, key=lambda l: l.score, reverse=True)[:5]
    print("Top leads:")
    for lead in top_leads:
        print(f"  {lead.first_name} {lead.last_name} at {lead.company_name} - Score: {lead.score}")


def main():
    args = parse_args()
    leads = read_leads(args.input)
    before_dedup = len(leads)
    unique_leads = remove_duplicates(leads)
    duplicates_removed = before_dedup - len(unique_leads)
    for lead in unique_leads:
        score_lead(lead)
    write_leads(unique_leads, args.output)
    print_summary(unique_leads, duplicates_removed)


if __name__ == "__main__":
    main()