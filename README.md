# MLB History Web Scraping & Dashboard

## Overview
This project scrapes historical Major League Baseball (MLB) data from [Baseball Almanac](https://www.baseball-almanac.com/yearmenu.shtml) using **Selenium** and stores it in a **SQLite database**. The project also includes an interactive dashboard built with **Streamlit** for exploring player statistics, team data, and historical trends.

---

## Features
- **Web Scraping**
  - Extracts tables for each MLB season.
  - Handles missing or incomplete data.
  - Cleans data: skips rows with too many nulls, replaces missing numeric values with `0` or `0.0`, and missing text with `"N/A"`.

- **Database Integration**
  - Imports CSVs or scraped data into SQLite.
  - Creates tables dynamically based on CSV filenames or table headers.
  - Infers proper column types (`INTEGER`, `REAL`, `TEXT`).

- **Interactive Dashboard**
  - Built using Streamlit.
  - Displays tables, charts, and statistics.
  - Dropdowns and sliders for filtering by year, team, or statistic.
  - Dynamic updates based on user input.

---

## Installation

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/mlb-history-dashboard.git
cd mlb-history-dashboard
2. Install Dependencies
bash
Copy code
pip install -r requirements.txt
Required packages:

pandas

selenium

webdriver-manager

sqlite3 (built-in)

streamlit

matplotlib

3. Set Up WebDriver
Ensure Chrome or another supported browser is installed. The script uses webdriver-manager to automatically install the correct ChromeDriver.

Usage
1. Scrape MLB Data
bash
Copy code
python scrape_mlb.py
Scrapes tables from Baseball Almanac.

Cleans the data.

Saves as CSV files in the tables/ directory.

2. Import CSVs into SQLite
bash
Copy code
python import_to_db.py
Imports all CSVs in tables/ into mlb_history.db.

Handles numeric/text columns and missing data.

3. Run Dashboard
bash
Copy code
streamlit run dashboard.py
Opens the interactive dashboard in your browser.

Explore stats, filter by year, and visualize data.

Folder Structure
bash
Copy code
mlb-history-dashboard/
│
├── tables/                 # Scraped CSV files
├── db/
│   └── mlb_history.db      # SQLite database
├── scrape_mlb.py           # Selenium scraper
├── import_to_db.py         # CSV → SQLite import script
├── dashboard.py            # Streamlit dashboard
├── requirements.txt        # Python dependencies
└── README.md               # Project overview
Data Cleaning Rules
Rows with >3 empty cells are skipped.

Numeric columns: missing values → 0 (int) or 0.0 (float).

Text columns: missing values → "N/A".

Column names and table names sanitized for SQLite compatibility.

Visualization
Interactive histograms, line charts, and summary statistics.

Filter data by year, team, or statistic using sliders and dropdowns.

Updates dynamically when user selections change.
