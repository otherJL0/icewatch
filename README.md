# ICE Detention Map

A Python-based dashboard for ICE detention statistics. This project downloads and renders publically available detention data from the [ICE Detention Management page](https://www.ice.gov/detain/detention-management).

## Overview

This project consists of three Python scripts:

1. **`ice_detention_scraper.py`** - Downloads ICE detention Excel files and parses the facilities data, outputting a JSON file
2. **`geocode_facilities.py`** - Geocodes the facilities data using the JSON file from the previous step
3. **`render_facilties_map.py`** - Simple script that renders a single page static site

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

### Step 1: ICE Detention Scraper

Download the latest detention statistics (this should auto-find the latest link):

```bash
python ice_detention_scraper.py
```

Then, extract the data about facilities to a JSON file (you can also do this in one step, see options below):

```bash
python ice_detention_scraper.py --extract-from-file data/YOUR_FILE_HERE.xlsx
```

#### Command Line Options

The script supports the following options:

- `--url`: Direct URL to the Excel file (optional, auto-finds by default)
- `--output-dir`: Directory to save the downloaded file (default: data)
- `--verify`: Verify the downloaded file by attempting to read it
- `--no-auto-find`: Disable auto-finding the latest link (use default URL instead)
- `--extract-json`: Extract facilities data to JSON file after downloading
- `--extract-from-file`: Extract facilities data to JSON from an existing Excel file

#### Examples

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

### Step 2: Geocode ICE facilities

You can geocode the facilities in your JSON file using OpenStreetMap Nominatim API. This will add latitude and longitude to each facility and stores address lookups in a cache file to avoid unnecessary API requests. If the OpenStreetMap API doesn't provide a result for a specific facility, you can enter it in the cache file manually once you locate the latitude and longitude.

### Usage

```bash
python geocode_facilities.py --input data/ice_facilities_YYYYMMDD.json
```

- By default, this will create a new file like `data/facilities_geocoded_YYYYMMDD_HHMMSS.json` and update (or create) `data/geocode_cache.json` in the same directory.
- You can specify custom output or cache files with `--output` and `--cache`.
- You can adjust the delay between API requests (default: 2 seconds) with `--delay`.

### Example

```bash
python geocode_facilities.py --input data/ice_facilities_YYYYMMDD.json --output data/facilities_geocoded_YYYYMMDD.json --cache data/geocode_cache.json
```

### User-Agent Requirement

**You must set a valid User-Agent string in the script before running it.**

Edit the `USER_AGENT` variable in `geocode_facilities.py`:

```python
USER_AGENT = "icewatch/1.0 (your_email@example.com)"
```

Replace `your_email@example.com` with your actual email or project contact. This is required by the [Nominatim Usage Policy](https://operations.osmfoundation.org/policies/nominatim/).

### Step 3: Rendering and Viewing the Facilities Map

You can create a static interactive map of all geocoded facilities using the provided script. The map will show each facility as a marker, with popups displaying the name, address, and rounded counts of criminal and non-criminal detainees.

#### Usage

```bash
python render_facilities_map.py --input data/facilities_geocoded_YYYYMMDD.json
```

- By default, this will create `docs/index.html` (and the `docs` directory if it doesn't exist).
- You can specify a custom output path with `--output` if desired.

## Disclaimer

This tool is for educational and research purposes. Please ensure compliance with the ICE website's terms of service and respect rate limiting.
