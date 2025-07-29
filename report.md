# Caprae Capital AI‑Readiness Pre‑Screening Report

## Project Rationale

Caprae Capital’s mission is to empower entrepreneurs and managers to close more deals and build enduring companies. To support that vision, this pre‑screening task builds a lightweight processing tool that takes raw leads from services like Apollo, LinkedIn, Crunchbase and Google Maps, cleans and deduplicates the data, applies a heuristic scoring model and produces personalised outreach templates. The goal is not to create a fully fledged product but to show a practical understanding of data hygiene and outreach segmentation—key competencies for Caprae’s operator‑first approach.

## Data Preprocessing

The input dataset (`dataset.csv`) contains fields for first name, last name, company, job title, revenue, industry and email. Duplicate records are common when scraping from multiple sources, so the first step is deduplication. The script removes leads with duplicate email addresses, assuming the email is the most reliable unique identifier. Additional fields could be used for deduplication (e.g. a combination of name and company) but using the email keeps the implementation clear and deterministic.

## Scoring Methodology

To prioritise outreach, each lead is assigned a numeric score that reflects their potential strategic value:

* **Title score**: Executives such as CEOs and CFOs receive the highest points because they typically hold purchasing authority. CTOs, vice presidents and directors get progressively fewer points, while managers and other roles receive the lowest score. Titles are matched using keyword patterns.
* **Revenue score**: Company size is approximated by annual revenue. Larger enterprises (≥ \$500 million) receive more points than medium (\$100–\$500 million) or small companies. Descriptive revenue categories (e.g. “small”) are converted to numeric values.
* **Industry score**: Certain industries align more closely with Caprae’s focus on technology and entrepreneurship. Technology and software companies receive more points, followed by healthcare and biotech, manufacturing, and all others.

The total score is simply the sum of these subscores. While rudimentary, this heuristic demonstrates the ability to combine multiple dimensions into a single ranking metric. In practice, Caprae could refine the weights based on historical outcomes or market intelligence.

## Email Generation

Beyond scoring, the script produces a personalised email template for each lead. The template references the lead’s name, title and company and introduces Caprae’s value proposition—streamlining operations, uncovering opportunities and helping entrepreneurs close more deals. In a real outreach campaign, the language would be customised further based on the lead’s industry, pain points and previous interactions.

## Alignment with Caprae’s Mission

This tool exemplifies Caprae’s operator‑first philosophy. Instead of building a monolithic solution, it focuses on delivering practical, incremental value: clean lead lists, prioritised prospects and tailored messaging. By keeping the pricing transparent and the technology accessible (no third‑party dependencies are required), the project encourages self‑service adoption. In the broader ETA and private equity context, such tools help small acquisition teams operate like larger organisations, enabling them to identify and convert targets more efficiently.

## Summary

The delivered lead‑processing pipeline is a concise example of how Caprae Capital empowers entrepreneurs through data‑driven workflows. It demonstrates the core steps—deduplication, scoring and messaging—that underpin effective outreach. With minimal modifications, the tool can be extended to handle larger datasets, more sophisticated scoring models and real‑time integrations with third‑party services. Ultimately, it shows that small improvements in data quality and prioritisation can have outsized impacts on deal flow and company growth.