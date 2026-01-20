"""
Wikipedia language info fetching.
Adapted from speech-resource-finder/wikipedia_info.py
"""

import re
import requests
from bs4 import BeautifulSoup


def construct_wiki_url(language_name):
    """Construct Wikipedia URL from language name."""
    clean_name = language_name.split('(')[0].strip()
    url_name = clean_name.replace(' ', '_')
    return f"https://en.wikipedia.org/wiki/{url_name}_language"


def check_url_exists(url):
    """Quick check if URL exists."""
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.head(url, headers=headers, timeout=5, allow_redirects=True)
        return response.status_code == 200
    except:
        return False


def fetch_language_info(language_name):
    """
    Fetch language info from Wikipedia.

    Returns dict with: speakers_l1, speakers_l2, family, writing_system, glottolog, wiki_url
    """
    wiki_url = construct_wiki_url(language_name)

    if not check_url_exists(wiki_url):
        print(f"      No Wikipedia page found for {language_name}")
        return None

    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        }
        response = requests.get(wiki_url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        infobox = soup.find('table', {'class': 'infobox'})

        if not infobox:
            return {'wiki_url': wiki_url}

        info = {
            'wiki_url': wiki_url,
            'speakers_l1': None,
            'speakers_l2': None,
            'family': None,
            'writing_system': None,
            'glottolog': None
        }

        rows = infobox.find_all('tr')

        for row in rows:
            th = row.find('th')
            if not th:
                continue

            header_text = th.get_text(strip=True).lower()
            td = row.find('td')
            if not td:
                continue

            # Speakers
            if 'native speakers' in header_text or header_text == 'speakers':
                speakers_text = td.get_text(strip=True)
                speakers_text = re.sub(r'\[\d+\]', '', speakers_text)

                l1_match = re.search(r'L1[:\s]*([\d,\.]+)\s*(million|billion)', speakers_text, re.IGNORECASE)
                if l1_match:
                    info['speakers_l1'] = f"{l1_match.group(1)} {l1_match.group(2).lower()}"
                else:
                    match = re.search(r'([\d,\.]+)\s*(million|billion)', speakers_text, re.IGNORECASE)
                    if match:
                        info['speakers_l1'] = f"{match.group(1)} {match.group(2).lower()}"
                    else:
                        match = re.search(r'([\d,]+)', speakers_text)
                        if match:
                            info['speakers_l1'] = match.group(1)

                l2_match = re.search(r'L2[:\s]*([\d,\.]+)\s*(million|billion)', speakers_text, re.IGNORECASE)
                if l2_match:
                    info['speakers_l2'] = f"{l2_match.group(1)} {l2_match.group(2).lower()}"

            # Language family
            elif 'language family' in header_text or 'family' in header_text:
                family_link = td.find('a')
                if family_link:
                    info['family'] = family_link.get_text(strip=True)
                else:
                    info['family'] = td.get_text(strip=True)[:100]

            # Writing system
            elif 'writing system' in header_text:
                ws_text = td.get_text(separator=' ', strip=True)
                ws_text = re.sub(r'\[\d+\]', '', ws_text)
                ws_text = ' '.join(ws_text.split())
                if ws_text and ws_text.lower() not in ['none', 'unwritten']:
                    info['writing_system'] = ws_text[:150]

            # Glottolog
            elif 'glottolog' in header_text:
                glottolog_link = td.find('a')
                if glottolog_link:
                    info['glottolog'] = glottolog_link.get_text(strip=True)
                else:
                    glottolog_text = td.get_text(strip=True)
                    if glottolog_text and glottolog_text.lower() not in ['none', '—']:
                        info['glottolog'] = glottolog_text

        return info

    except Exception as e:
        print(f"      Error fetching Wikipedia for {language_name}: {e}")
        return None
