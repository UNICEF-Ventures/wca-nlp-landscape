"""
HuggingFace model and dataset fetching.
Adapted from speech-resource-finder/huggingface_search.py

Fetches only the first page (30 items) but extracts the total count from
the page to show accurate "X more on HuggingFace" links.
"""

import re
import requests
from bs4 import BeautifulSoup


def parse_stat_number(stat_text):
    """Parse HuggingFace stat numbers like '4.07M', '23.4k' into integers."""
    if not stat_text:
        return 0

    stat_text = stat_text.strip().upper()

    try:
        if 'M' in stat_text:
            return int(float(stat_text.replace('M', '')) * 1_000_000)
        elif 'K' in stat_text:
            return int(float(stat_text.replace('K', '')) * 1_000)
        else:
            return int(stat_text.replace(',', ''))
    except (ValueError, AttributeError):
        return 0


def extract_total_count(html_content):
    """Extract the total count from HuggingFace page.

    Looks for: window.__hf_deferred = {"numTotalItems":303}
    Also tries alternative patterns for datasets pages.
    """
    # Primary pattern (works for both models and datasets)
    match = re.search(r'"numTotalItems"\s*:\s*(\d+)', html_content)
    if match:
        return int(match.group(1))

    # Alternative pattern that may appear on datasets pages
    match = re.search(r'"numItemsFound"\s*:\s*(\d+)', html_content)
    if match:
        return int(match.group(1))

    # Another alternative pattern
    match = re.search(r'"totalNumItems"\s*:\s*(\d+)', html_content)
    if match:
        return int(match.group(1))

    return None


def search_huggingface(iso_639_1, iso_639_3, search_type, pipeline_tag):
    """
    Search HuggingFace for models or datasets.

    Fetches first page for each language code and extracts total counts.
    Since HuggingFace has inconsistent language tagging (some models use ISO 639-1,
    others use ISO 639-3), we search both and sum the totals.

    Args:
        iso_639_1: 2-letter code (can be None)
        iso_639_3: 3-letter code
        search_type: 'models' or 'datasets'
        pipeline_tag: e.g., 'automatic-speech-recognition', 'text-to-speech', 'translation'

    Returns:
        dict with:
            'items': list of models/datasets (deduplicated)
            'total_count': sum of totals from all language codes
            'counts_by_code': dict mapping each code to its count (for display)
    """
    codes_to_try = []
    if iso_639_1:
        codes_to_try.append(iso_639_1)
    if iso_639_3:
        codes_to_try.append(iso_639_3)

    if not codes_to_try:
        return {'items': [], 'total_count': 0, 'counts_by_code': {}}

    items = []
    seen = set()
    counts_by_code = {}  # Track count for each language code
    items_by_code = {}  # Track actual items found for each code (fallback for datasets)

    for code in codes_to_try:
        try:
            if search_type == 'models':
                url = f"https://huggingface.co/models?pipeline_tag={pipeline_tag}&language={code}&sort=trending"
            else:
                url = f"https://huggingface.co/datasets?task_categories=task_categories:{pipeline_tag}&language=language:{code}&sort=trending"

            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
            }

            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()

            html_content = response.text

            # Extract total count for this specific code
            page_total = extract_total_count(html_content)
            if page_total:
                counts_by_code[code] = page_total

            soup = BeautifulSoup(html_content, 'html.parser')
            cards = soup.find_all('article', class_='overview-card-wrapper')

            if not cards:
                continue

            # Track items found for this specific code (before deduplication)
            items_for_code = []

            for card in cards:
                try:
                    link = card.find('a', href=True)
                    if not link:
                        continue

                    href = link.get('href', '').lstrip('/')

                    # For datasets, remove 'datasets/' prefix
                    if search_type == 'datasets' and href.startswith('datasets/'):
                        href = href[9:]

                    if not href or href == '#':
                        continue

                    # Track if this item is new (not seen before)
                    is_new = href not in seen

                    if is_new:
                        seen.add(href)

                    # Parse stats from SVG icons
                    downloads = 0
                    likes = 0

                    svgs = card.find_all('svg')
                    for svg in svgs:
                        next_elem = svg.find_next_sibling(string=True)
                        stat_text = ""

                        if next_elem and next_elem.strip():
                            stat_text = next_elem.strip()
                        else:
                            next_tag = svg.find_next_sibling()
                            if next_tag:
                                stat_text = next_tag.get_text(strip=True)

                        if not stat_text:
                            continue

                        svg_str = str(svg)

                        # Download icon
                        if 'M26 24v4H6v-4' in svg_str:
                            downloads = parse_stat_number(stat_text)
                        # Like icon
                        elif 'M22.45,6a5.47' in svg_str:
                            likes = parse_stat_number(stat_text)

                    base_url = "https://huggingface.co"
                    if search_type == 'datasets':
                        base_url += "/datasets"

                    item = {
                        'name': href,
                        'url': f"{base_url}/{href}",
                        'downloads': downloads,
                        'likes': likes,
                    }

                    # Add to global items list if new
                    if is_new:
                        items.append(item)

                    # Also track for this specific code
                    items_for_code.append(item)

                except Exception:
                    continue

            # Store count of items found for this code
            items_by_code[code] = len(items_for_code)

        except Exception as e:
            print(f"      Warning: Error fetching {search_type} for {code}: {e}")
            continue

    # Sort by downloads
    items.sort(key=lambda x: x['downloads'], reverse=True)

    # If we couldn't extract total counts from HTML (common for datasets pages),
    # use the actual item counts we found as a fallback
    if not counts_by_code and items_by_code:
        counts_by_code = items_by_code

    # Sum all counts (since ha and hau are different searches on HuggingFace)
    total_count = sum(counts_by_code.values()) if counts_by_code else len(items)

    return {
        'items': items,
        'total_count': total_count,
        'counts_by_code': counts_by_code
    }


def fetch_models_for_language(iso_639_1, iso_639_3, pipeline_tag):
    """Fetch models for a language and task type.

    Returns:
        dict with 'items' (list of models) and 'total_count' (int)
    """
    print(f"      Searching {pipeline_tag} models...")
    return search_huggingface(iso_639_1, iso_639_3, 'models', pipeline_tag)


def fetch_datasets_for_language(iso_639_1, iso_639_3, task_category):
    """Fetch datasets for a language and task type.

    Returns:
        dict with 'items' (list of datasets) and 'total_count' (int)
    """
    print(f"      Searching {task_category} datasets...")
    return search_huggingface(iso_639_1, iso_639_3, 'datasets', task_category)
