
# Australian Migration Agents Scraper

A Python scraper that extracts first names, last names, and email addresses from the Australian migration agents register.

## Features

- Browser-based search using Playwright.
- Navigation through search-result pages.
- Extraction of contact details from agent profiles.
- CSV export using Scrapy.

## Tech Stack

- Python
- Scrapy
- scrapy-playwright

## Installation

```powershell
python -m venv venv 
.\venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m playwright install chromium
```

## Usage

Run from the directory containing scrapy.cfg:

```powershell
python -m scrapy crawl agents
```

The output filename is configured in the FEEDS setting in `agentsscraper/settings.py`.

## Search Mode

The current code selects "Non-commercial organisations".

To run without this filter, comment out the checkbox-checking `line 41` in `agentsscraper/spiders/agents.py`.

Remember to change the file output's name in `agentsscraper/settings.py` after comment out `line 41`in`agentsscraper/spiders/agents.py`.

```Python
FEEDS = {
    "scraped_non_commercial.csv": {"format": "csv", "overwrite": True},
    # "scraped.csv": {"format": "csv", "overwrite": True},
}
```

## Output Fields

- first_name
- last_name
- email_address

## Data Privacy

Scraped contact records are excluded from this repository.  
Any public demonstration will use fabricated sample data.

## Sample Output

See [sample output](sample/sample_output.csv).  
All sample names and email addresses are fabricated.
