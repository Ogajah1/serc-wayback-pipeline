# Multilingual SERC Harvest Pipeline 🕸️

## 📌 Overview
This repository contains a specialized data engineering pipeline designed for large-scale econometric research. It automates the collection of **Search Engine Result Counts (SERC)** across multiple languages (Spanish, Catalan, Basque, Galician) to measure corporate privacy transparency prior to GDPR enforcement. SERC is a methodology commonly used to measure online privacy disclosure and transparency in applied econometrics research.

This tool was developed as part of my ongoing PhD research on **Privacy Regulations and Constraint-Induced Innovation**.

---

## 🛠️ Engineering Features
- **Multilingual Query Logic:** Dynamically constructs Boolean search strings across four Spanish regional languages (Spanish, Catalan, Basque, Galician) plus universal legal terminology to maximize coverage.
- **API Rate Management:** Implements automated "Quota Exceeded" detection and execution pauses to respect Google Custom Search API limits.
- **Robust Resume Logic:** Built-in checkpointing allows the pipeline to resume from the last processed anonymized firm ID. This helps to prevent redundant API cost and data duplication.
- **Domain Extraction Engine:** Parses complex Wayback Machine URLs to isolate root domains for clean search queries.

---

## 🏗️ Data Architecture & Governance


1. **Anonymization Layer:** Real NIFs are processed locally via `anonymize_data.py` to generate synthetic firm IDs for the de-identified research sample used in this project. The private re-identification key is stored outside the repository.
2. **Input:** A mapping of anonymized firm IDs and their historical archived URLs.
3. **Processing:** - Domain parsing via `urllib.parse`.
    - Boolean query construction using a specialized linguistic dictionary.
    - Synchronous API calls with automated error handling and quota management.
4. **Output:** A structured `serc_multilingual_results.csv` ready for merged analysis with firm-level financial data.

---

## 🔒 Data Privacy & Security
To comply with data protection standards (GDPR) and professional security practices:
- **No PII (Personally Identifiable Information):** All firm identifiers in this repository are synthetic. The master mapping key remains in a secure, local-only environment.
- **Secret Management:** API keys are managed via environment variables and GitHub Secrets. No credentials are ever committed to version control.

---

## 🚀 Tech Stack
- **Language:** Python 3.x
- **Libraries:** Pandas, Requests, python-dotenv
- **Infrastructure:** GitHub Actions (Manual Workflow Dispatch)
- **API:** Google Custom Search JSON API

---

## 📋 Setup & Usage

## 📋 Setup & Usage

### 1. Environment Variables & API Credentials
To run this pipeline locally, create a `.env` file in the root directory:
```bash
GOOGLE_API_KEY='your_key'
SEARCH_ENGINE_ID='your_cx_id'
INPUT_PATH='data/sample_data.csv'  # Optional: Default for local testing
OUTPUT_PATH='serc_multilingual_results.csv'
```

To obtain Google API credentials:
- Create a project in the Google Cloud Console.
- Enable the Custom Search JSON API.
- Generate an API key and create a Programmable Search Engine (formerly Custom Search Engine) ID
---
### 2. Installation 
# Clone the repository
git clone [https://github.com/Ogajah1/serc-wayback-pipeline.git](https://github.com/Ogajah1/serc-wayback-pipeline.git)
cd serc-wayback-pipeline

# Install dependencies
pip install -r requirements.txt
---
### 3. Running the Pipeline
- First, ensure you've run the anonymization script `anonymize_data.py` if using real data. Then, execute the main harvest script `SERC_harvest_ml.py`
The pipeline will process the input, handle API calls, and append results to the output CSV. It supports resuming if interrupted. 
---
### 4. For Reproducibility & Testing
First, Navigate to the Actions tab in this repository.Next, Select Manual SERC Harvest (Safe Mode) from the sidebar. Click Run workflow and download the serc-results.zip. under the artifact section. 
### 5. Limitations
- **API Quotas:** The free tier of Google Custom Search API is limited to ~100 queries per day. For larger datasets, consider the paid tier, multiple API keys, or alternative search APIs like Bing.
- **Scalability:** Currently synchronous; for very large inputs (>1,000 firms), implement asynchronous calls (e.g., via asyncio) to improve performance.
- **Data Accuracy:** SERC counts are estimates and may vary; results depend on Google's indexing of historical sites. This limitation is standard in SERC-based empirical research and are addressed through robustness checks at the analysis stage.
- **Multilingual Coverage:** Keywords are tailored to Spanish regions but may miss niche dialects or evolving terminology.
---

## 🎓 How to Cite
If you use this pipeline or methodology in your research, please cite it as follows:

**APA Style:**
Tawiah, T. O. (2026). *Multilingual SERC Harvest Pipeline: A de-identified data engineering approach for privacy innovation research* (Version 1.0.0) [Software]. Available from https://github.com/Ogajah1/serc-wayback-pipeline

**BibTeX:**
@software{tawiah2026serc,
  author = {Thompson Ogajah Tawiah},
  title = {Multilingual SERC Harvest Pipeline: A de-identified data engineering approach for privacy innovation research},
  url = {https://github.com/Ogajah1/serc-wayback-pipeline},
  version = {1.0.0},
  year = {2026}
}
