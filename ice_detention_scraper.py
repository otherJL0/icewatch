#!/usr/bin/env python3
"""
ICE Detention Statistics Scraper and Downloader

This script scrapes the ICE detention management page to find the latest
detention statistics Excel file and downloads it. It can handle dynamic
links that may change over time.

Author: Your Name
Date: 2024
"""

import requests
import os
import sys
import re
from datetime import datetime
from pathlib import Path
import logging
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def find_detention_stats_link(base_url="https://www.ice.gov/detain/detention-management"):
    """
    Scrape the ICE detention management page to find the latest statistics download link.

    Args:
        base_url (str): URL of the ICE detention management page.

    Returns:
        str: URL of the detention statistics Excel file, or None if not found.
    """

    try:
        logger.info(f"Scraping page: {base_url}")

        # Set up headers to mimic a browser request
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }

        # Get the page content
        response = requests.get(base_url, headers=headers, timeout=30)
        response.raise_for_status()

        # Parse the HTML
        soup = BeautifulSoup(response.content, 'html.parser')

        # Look for links containing detention statistics keywords
        keywords = [
            'detention', 'statistics', 'FY25', 'YTD', 'xlsx', 'excel',
            'detentionStats', 'FY2025'
        ]

        found_links = []

        # Search for all links on the page
        for link in soup.find_all('a', href=True):
            href = link.get('href', '').lower()
            text = link.get_text().lower()

            # Check if link text or href contains relevant keywords
            is_relevant = any(keyword.lower() in href or keyword.lower() in text
                            for keyword in keywords)

            if is_relevant:
                full_url = urljoin(base_url, link['href'])
                link_text = link.get_text().strip()
                found_links.append({
                    'url': full_url,
                    'text': link_text,
                    'relevance_score': sum(1 for keyword in keywords
                                         if keyword.lower() in href or keyword.lower() in text)
                })
                logger.info(f"Found potential link: {link_text} -> {full_url}")

        if not found_links:
            logger.warning("No relevant links found on the page")
            return None

        # Sort by relevance score and prefer .xlsx files
        found_links.sort(key=lambda x: (x['relevance_score'], '.xlsx' in x['url'].lower()), reverse=True)

        # Return the most relevant link
        best_match = found_links[0]
        logger.info(f"Selected best match: {best_match['text']} -> {best_match['url']}")

        return best_match['url']

    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to scrape page: {e}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error while scraping: {e}")
        return None


def download_ice_detention_stats(url=None, output_dir="data", auto_find_link=True):
    """
    Download ICE detention statistics Excel file.

    Args:
        url (str, optional): Direct URL to the Excel file. If None, auto-finds the latest link.
        output_dir (str): Directory to save the downloaded file.
        auto_find_link (bool): Whether to automatically find the latest link from the website (default: True).

    Returns:
        str: Path to the downloaded file, or None if download failed.
    """

    # Auto-find the latest link by default
    if auto_find_link:
        logger.info("Auto-finding latest detention statistics link...")
        found_url = find_detention_stats_link()
        if found_url:
            url = found_url
            logger.info(f"Found latest URL: {url}")
        else:
            logger.warning("Could not find latest link, using default URL")
            if url is None:
                url = "https://www.ice.gov/doclib/detention/FY25_detentionStats06202025.xlsx"
    elif url is None:
        # Fallback to default URL if auto-find is disabled and no URL provided
        url = "https://www.ice.gov/doclib/detention/FY25_detentionStats06202025.xlsx"

    # Create output directory if it doesn't exist
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    # Generate filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"ice_detention_stats_{timestamp}.xlsx"
    filepath = os.path.join(output_dir, filename)

    try:
        logger.info(f"Starting download from: {url}")

        # Set up headers to mimic a browser request
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet,application/vnd.ms-excel,application/octet-stream',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }

        # Download the file
        response = requests.get(url, headers=headers, stream=True, timeout=30)
        response.raise_for_status()

        # Check if the response contains Excel content
        content_type = response.headers.get('content-type', '').lower()
        if 'excel' not in content_type and 'spreadsheet' not in content_type and 'octet-stream' not in content_type:
            logger.warning(f"Unexpected content type: {content_type}")

        # Get file size
        file_size = int(response.headers.get('content-length', 0))
        logger.info(f"File size: {file_size / 1024:.1f} KB")

        # Save the file
        with open(filepath, 'wb') as f:
            downloaded_size = 0
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
                    downloaded_size += len(chunk)

                    # Log progress for large files
                    if file_size > 0 and downloaded_size % (1024 * 1024) == 0:  # Every MB
                        progress = (downloaded_size / file_size) * 100
                        logger.info(f"Download progress: {progress:.1f}%")

        logger.info(f"Download completed successfully!")
        logger.info(f"File saved to: {filepath}")
        logger.info(f"File size: {os.path.getsize(filepath) / 1024:.1f} KB")

        return filepath

    except requests.exceptions.RequestException as e:
        logger.error(f"Download failed: {e}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return None


def verify_download(filepath):
    """
    Verify that the downloaded file is a valid Excel file.

    Args:
        filepath (str): Path to the downloaded file.

    Returns:
        bool: True if file is valid, False otherwise.
    """
    try:
        import pandas as pd

        # Try to read the Excel file
        df = pd.read_excel(filepath, sheet_name=None)

        # Log information about the sheets
        logger.info(f"Excel file contains {len(df)} sheets:")
        for sheet_name in df.keys():
            sheet_info = df[sheet_name]
            logger.info(f"  - {sheet_name}: {len(sheet_info)} rows, {len(sheet_info.columns)} columns")

        return True

    except Exception as e:
        logger.error(f"File verification failed: {e}")
        return False


def main():
    """Main function to run the scraper and downloader."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Download ICE detention statistics Excel file",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python ice_detention_scraper.py
  python ice_detention_scraper.py --output-dir ./data --verify
  python ice_detention_scraper.py --url "https://custom-url.xlsx"
  python ice_detention_scraper.py --no-auto-find
        """
    )

    parser.add_argument(
        '--url',
        help='Direct URL to the Excel file (optional)',
        default=None
    )

    parser.add_argument(
        '--output-dir',
        help='Directory to save the downloaded file (default: data)',
        default='data'
    )

    parser.add_argument(
        '--no-auto-find',
        action='store_true',
        help='Disable auto-finding the latest link (use default URL instead)'
    )

    parser.add_argument(
        '--verify',
        action='store_true',
        help='Verify the downloaded file by attempting to read it'
    )

    args = parser.parse_args()

    logger.info("ICE Detention Statistics Scraper and Downloader")
    logger.info("=" * 50)

    # Download the file
    filepath = download_ice_detention_stats(
        url=args.url,
        output_dir=args.output_dir,
        auto_find_link=not args.no_auto_find
    )

    if filepath:
        logger.info("Download completed successfully!")

        # Verify the file if requested
        if args.verify:
            logger.info("Verifying downloaded file...")
            if verify_download(filepath):
                logger.info("File verification successful!")
            else:
                logger.error("File verification failed!")
                sys.exit(1)
    else:
        logger.error("Download failed!")
        sys.exit(1)


if __name__ == "__main__":
    main()