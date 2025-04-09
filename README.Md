# Stretch Lab Scraper

## Overview

**Stretch Lab Scraper** is a Python-based tool(robot) that leverages [ScrapeGraphAI](https://github.com/ScrapeGraphAI/Scrapegraph-ai) to extract data from a target website using AI-driven scraping. The scraped data is analysed and stored in an Airtable base, making it ideal for automating data collection for the `stretchlab-server` project. This tool is designed to be flexible, robust, and easy to extend.

### Key Features
- **AI-Powered Scraping**: Uses ScrapeGraphAI with customizable prompts to extract structured data using GPT-4o model.
- **Airtable Integration**: Stores data in a specified Airtable table for easy access and analysis.
- **Environment**: Runs in a Python virtual environment (`venv`) for dependency management.

### Use Case
This scraper targets websites related to Stretch Lab (clubready) to carry out some processes and get some data. It feeds this data into Airtable for downstream processing, such as generating quality scores, tracking client activity, checking flexologist schedules and note, status, first timers conversation and bookings, etc. within the `stretchlab-server` ecosystem.

---

## Prerequisites

- **Python 3.9+**: Installed on your system (Windows assumed based on `C:\Users\Awe`).
- **Airtable Account**: With a base, table, and Personal Access Token (PAT).
- **Target Website**: A URL to scrape (clubReady).

---

## Installation

### 1. Project Setup
Navigate to your project directory:
```bash
cd C:\Users\yourusername\deskop\project

git init

python -m venv venv

venv\Scripts\activate

python scrapper.py

```