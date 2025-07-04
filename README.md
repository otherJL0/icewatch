# ICE Detention Statistics Downloader

A Python project for downloading ICE (U.S. Immigration and Customs Enforcement) detention statistics Excel files from the official ICE website.

## Overview

This project provides a Python script for downloading ICE detention statistics:

**`ice_detention_scraper.py`** - Downloads ICE detention statistics Excel files with automatic link discovery

## Installation

1. Clone this repository:
```bash
git clone <repository-url>
cd icewatch
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

Download the latest detention statistics (auto-finds the latest link):

```bash
python ice_detention_scraper.py
```

### Advanced Usage

Use a specific URL instead of auto-finding:

```bash
python ice_detention_scraper.py --url "https://custom-url.xlsx"
```

### Command Line Options

The script supports the following options:

- `--url`: Direct URL to the Excel file (optional, auto-finds by default)
- `--output-dir`: Directory to save the downloaded file (default: data)
- `--verify`: Verify the downloaded file by attempting to read it
- `--no-auto-find`: Disable auto-finding the latest link (use default URL instead)
- `--extract-json`: Extract facilities data to JSON file after downloading
- `--extract-from-file`: Extract facilities data to JSON from an existing Excel file

### Examples

```bash
# Download to a custom directory
python ice_detention_scraper.py --output-dir ./data

# Download and verify the file
python ice_detention_scraper.py --verify

# Use a specific URL instead of auto-finding
python ice_detention_scraper.py --url "https://custom-url.xlsx"

# Download to current directory
python ice_detention_scraper.py --output-dir .

# Disable auto-find and use default URL
python ice_detention_scraper.py --no-auto-find

# Download and extract facilities data to JSON
python ice_detention_scraper.py --extract-json

# Extract JSON from an existing Excel file
python ice_detention_scraper.py --extract-from-file "path/to/existing/file.xlsx"
```

## File Structure

```
icewatch/
├── ice_detention_scraper.py       # ICE detention statistics downloader
├── requirements.txt               # Python dependencies
├── README.md                     # This file
└── data/                    # Default download directory (created automatically)
    └── ice_detention_stats_YYYYMMDD_HHMMSS.xlsx
```

## Data Source

The scripts download detention data from the [ICE Detention Management page](https://www.ice.gov/detain/detention-management).

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Disclaimer

This tool is for educational and research purposes. Please ensure compliance with the ICE website's terms of service and respect rate limiting when using this tool.