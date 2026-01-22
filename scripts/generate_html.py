#!/usr/bin/env python3
"""
Generate a browsable HTML website from Research/ data.

Now uses language-first structure (Research/Languages/{iso}/).

Usage:
    python scripts/generate_html.py

Output:
    output/index.html
    output/lang/{iso}.html
"""

import json
import re
from pathlib import Path
from datetime import datetime

import yaml

# Paths
SCRIPT_DIR = Path(__file__).parent
PROJECT_DIR = SCRIPT_DIR.parent
RESEARCH_DIR = PROJECT_DIR / "Research"
LANGUAGES_DIR = RESEARCH_DIR / "Languages"
ACTORS_DIR = RESEARCH_DIR / "Actors"
OUTPUT_DIR = PROJECT_DIR / "output"
WCA_LANGUAGES_PATH = RESEARCH_DIR / "wca_all_languages.yaml"
FOCUSED_LANGUAGES_PATH = RESEARCH_DIR / "focused_languages.yaml"

# WCA Countries for grouping (includes alternative spellings from source data)
WCA_COUNTRIES = {
    'Benin': 'BJ', 'Burkina Faso': 'BF', 'Cameroon': 'CM',
    'Central African Republic': 'CF', 'Chad': 'TD',
    'Republic of the Congo': 'CG', 'Congo': 'CG',
    'Côte d\'Ivoire': 'CI', 'Cote d\'Ivoire': 'CI', 'Ivory Coast': 'CI',
    'Democratic Republic of the Congo': 'CD', 'Democratic Republic of Congo': 'CD',
    'DR Congo': 'CD', 'DRC': 'CD',
    'Equatorial Guinea': 'GQ', 'Gabon': 'GA',
    'The Gambia': 'GM', 'Gambia': 'GM',
    'Ghana': 'GH', 'Guinea': 'GN', 'Guinea-Bissau': 'GW', 'Liberia': 'LR',
    'Mali': 'ML', 'Mauritania': 'MR', 'Niger': 'NE', 'Nigeria': 'NG',
    'Sao Tome and Principe': 'ST', 'São Tomé and Príncipe': 'ST',
    'Senegal': 'SN', 'Sierra Leone': 'SL', 'Togo': 'TG',
}

# Country code to name mapping (ISO 3166-1 alpha-2)
COUNTRY_NAMES = {
    'BJ': 'Benin', 'BF': 'Burkina Faso', 'CM': 'Cameroon', 'CF': 'Central African Republic',
    'TD': 'Chad', 'CG': 'Republic of the Congo', 'CI': "Côte d'Ivoire",
    'CD': 'DR Congo', 'GQ': 'Equatorial Guinea', 'GA': 'Gabon',
    'GM': 'The Gambia', 'GH': 'Ghana', 'GN': 'Guinea', 'GW': 'Guinea-Bissau',
    'LR': 'Liberia', 'ML': 'Mali', 'MR': 'Mauritania', 'NE': 'Niger', 'NG': 'Nigeria',
    'ST': 'São Tomé and Príncipe', 'SN': 'Senegal', 'SL': 'Sierra Leone', 'TG': 'Togo',
    # Non-WCA African countries that may appear
    'KE': 'Kenya', 'ZA': 'South Africa', 'ET': 'Ethiopia', 'TZ': 'Tanzania',
    'UG': 'Uganda', 'RW': 'Rwanda', 'ZW': 'Zimbabwe', 'ZM': 'Zambia',
    'MW': 'Malawi', 'MZ': 'Mozambique', 'AO': 'Angola', 'NA': 'Namibia',
    'BW': 'Botswana', 'EG': 'Egypt', 'MA': 'Morocco', 'DZ': 'Algeria',
    'TN': 'Tunisia', 'LY': 'Libya', 'SD': 'Sudan', 'SS': 'South Sudan',
    'ER': 'Eritrea', 'DJ': 'Djibouti', 'SO': 'Somalia', 'MG': 'Madagascar',
    'MU': 'Mauritius', 'SC': 'Seychelles', 'CV': 'Cape Verde', 'KM': 'Comoros',
}


def load_yaml(path):
    """Load YAML file, return empty dict if not found."""
    if not path.exists():
        return {}
    with open(path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f) or {}


def load_markdown(path):
    """Load markdown file, return empty string if not found."""
    if not path.exists():
        return ""
    with open(path, 'r') as f:
        return f.read()


def load_focused_languages():
    """Load focused languages list (ISO codes)."""
    if not FOCUSED_LANGUAGES_PATH.exists():
        return []
    data = load_yaml(FOCUSED_LANGUAGES_PATH)
    if isinstance(data, list):
        return data
    return []


def markdown_to_html(md_text):
    """Simple markdown to HTML conversion."""
    if not md_text:
        return ""

    html = md_text

    # Headers
    html = re.sub(r'^### (.+)$', r'<h4>\1</h4>', html, flags=re.MULTILINE)
    html = re.sub(r'^## (.+)$', r'<h3>\1</h3>', html, flags=re.MULTILINE)
    html = re.sub(r'^# (.+)$', r'<h2>\1</h2>', html, flags=re.MULTILINE)

    # Bold and italic
    html = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html)
    html = re.sub(r'\*(.+?)\*', r'<em>\1</em>', html)

    # Links
    html = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2" target="_blank">\1</a>', html)

    # Line breaks to paragraphs
    paragraphs = html.split('\n\n')
    html = ''.join(f'<p>{p.strip()}</p>' for p in paragraphs if p.strip() and not p.strip().startswith('<h'))

    return html


def load_all_languages():
    """Load all language data from Research/Languages/."""
    languages = {}

    if not LANGUAGES_DIR.exists():
        return languages

    for lang_dir in sorted(LANGUAGES_DIR.iterdir()):
        if not lang_dir.is_dir() or lang_dir.name.startswith('.'):
            continue

        iso_code = lang_dir.name
        languages[iso_code] = {
            'info': load_yaml(lang_dir / "info.yaml"),
            'models': load_yaml(lang_dir / "models.yaml"),
            'datasets': load_yaml(lang_dir / "datasets.yaml"),
            'benchmarks': load_yaml(lang_dir / "benchmarks.yaml"),
            'notes': load_markdown(lang_dir / "notes.md"),
        }

    return languages


def load_all_actors():
    """Load all actor data from Research/Actors/."""
    actors = {}

    if not ACTORS_DIR.exists():
        return actors

    for actor_file in sorted(ACTORS_DIR.glob("*.yaml")):
        actor_key = actor_file.stem
        actors[actor_key] = load_yaml(actor_file)

    return actors


def load_wca_languages():
    """Load all WCA languages from wca_all_languages.yaml."""
    if not WCA_LANGUAGES_PATH.exists():
        return []
    data = load_yaml(WCA_LANGUAGES_PATH)
    return data.get('languages', [])


def get_actors_for_language(iso_639_3, actors):
    """Get list of actors that work on a specific language."""
    matching = []
    for actor_key, actor_data in actors.items():
        actor_langs = actor_data.get('languages', [])
        if iso_639_3 in actor_langs:
            matching.append(actor_data)
    return matching


def format_number(n):
    """Format large numbers with K/M suffix."""
    if n >= 1_000_000:
        return f"{n/1_000_000:.1f}M"
    elif n >= 1_000:
        return f"{n/1_000:.1f}K"
    return str(n)


def country_code_to_name(code):
    """Convert ISO 3166-1 alpha-2 country code to name."""
    return COUNTRY_NAMES.get(code, code)


def country_codes_to_names(codes):
    """Convert list of country codes to list of names."""
    if not codes:
        return []
    return [country_code_to_name(c) for c in codes]


def format_actor_type(actor_type):
    """Convert actor type from snake_case to readable format."""
    if not actor_type:
        return '—'
    # Replace underscores with spaces and title case
    return actor_type.replace('_', ' ').title()


def format_huggingface_link(url):
    """Extract HuggingFace handle and return as link."""
    if not url:
        return '—'
    # Extract handle from URL like https://huggingface.co/masakhane
    handle = url.rstrip('/').split('/')[-1]
    return f'<a href="{url}" target="_blank">{handle}</a>'


def get_css():
    """Return the CSS styles."""
    return """
        :root {
            --primary: #0077b6;
            --primary-dark: #023e8a;
            --secondary: #00b4d8;
            --bg: #f8f9fa;
            --card-bg: #ffffff;
            --text: #212529;
            --text-muted: #6c757d;
            --border: #dee2e6;
            --success: #198754;
            --warning: #fd7e14;
        }

        * { box-sizing: border-box; margin: 0; padding: 0; }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
            background: var(--bg);
            color: var(--text);
            line-height: 1.5;
        }

        header {
            background: var(--primary-dark);
            color: white;
            padding: 1.5rem 2rem;
            position: sticky;
            top: 0;
            z-index: 100;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        header h1 { font-size: 1.5rem; font-weight: 600; }
        header .subtitle { opacity: 0.8; font-size: 0.9rem; }
        header .updated { opacity: 0.7; font-size: 0.8rem; text-align: right; }
        header a { color: white; text-decoration: none; }
        header a:hover { text-decoration: underline; }

        .disclaimer {
            background: #fff3cd;
            border-bottom: 1px solid #ffc107;
            padding: 0.5rem 2rem;
            font-size: 0.85rem;
            color: #856404;
        }
        .disclaimer a { color: #664d03; }

        .tabs {
            display: flex;
            background: var(--card-bg);
            border-bottom: 1px solid var(--border);
            padding: 0 2rem;
        }

        .tab {
            padding: 1rem 1.5rem;
            cursor: pointer;
            border: none;
            background: none;
            font-size: 1rem;
            color: var(--text-muted);
            border-bottom: 3px solid transparent;
            transition: all 0.2s;
        }

        .tab:hover { color: var(--primary); }

        .tab.active {
            color: var(--primary);
            border-bottom-color: var(--primary);
            font-weight: 500;
        }

        .tab-content {
            display: none;
            padding: 2rem;
            max-width: 1400px;
            margin: 0 auto;
        }

        .tab-content.active { display: block; }

        .languages-grid {
            display: grid;
            gap: 1.5rem;
            grid-template-columns: repeat(auto-fill, minmax(400px, 1fr));
        }

        .language-card {
            background: var(--card-bg);
            border-radius: 8px;
            padding: 1.25rem;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
            border: 1px solid var(--border);
        }

        .lang-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 0.75rem;
            flex-wrap: wrap;
            gap: 0.5rem;
        }

        .lang-header h3 { font-size: 1.25rem; }
        .lang-header h3 a { color: var(--primary-dark); text-decoration: none; }
        .lang-header h3 a:hover { text-decoration: underline; }

        .lang-codes {
            font-family: monospace;
            background: var(--bg);
            padding: 0.2rem 0.5rem;
            border-radius: 4px;
            font-size: 0.85rem;
        }

        .country-tags {
            display: flex;
            flex-wrap: wrap;
            gap: 0.3rem;
            margin-bottom: 0.5rem;
        }

        .country-tag {
            background: #e7f5ff;
            color: #1971c2;
            padding: 0.1rem 0.4rem;
            border-radius: 3px;
            font-size: 0.75rem;
        }

        .altnames {
            font-size: 0.8rem;
            color: var(--text-muted);
            margin-bottom: 0.5rem;
        }

        .lang-meta {
            font-size: 0.9rem;
            color: var(--text-muted);
            margin-bottom: 0.75rem;
        }

        .lang-meta div { margin-bottom: 0.25rem; }

        .cv-stats {
            background: #e7f5ff;
            padding: 0.5rem 0.75rem;
            border-radius: 4px;
            font-size: 0.85rem;
            margin-bottom: 0.75rem;
        }

        .model-summary {
            display: flex;
            gap: 0.5rem;
            margin-bottom: 0.75rem;
            flex-wrap: wrap;
        }

        .badge {
            padding: 0.25rem 0.6rem;
            border-radius: 4px;
            font-size: 0.8rem;
            font-weight: 500;
        }

        .badge.asr { background: #d0ebff; color: #1971c2; }
        .badge.tts { background: #d3f9d8; color: #2f9e44; }
        .badge.mt { background: #fff3bf; color: #e67700; }
        .badge.llm { background: #f3d9fa; color: #9c36b5; }

        .models-section {
            margin-top: 0.5rem;
            border: 1px solid var(--border);
            border-radius: 4px;
        }

        .models-section summary {
            padding: 0.5rem 0.75rem;
            cursor: pointer;
            background: var(--bg);
            font-weight: 500;
            font-size: 0.9rem;
        }

        .models-section summary:hover { background: #e9ecef; }
        .models-section[open] summary { border-bottom: 1px solid var(--border); }
        .models-section > *:not(summary) { padding: 0.75rem; }

        .data-table {
            width: 100%;
            font-size: 0.85rem;
            border-collapse: collapse;
        }

        .data-table th {
            text-align: left;
            padding: 0.4rem;
            border-bottom: 1px solid var(--border);
            font-weight: 500;
            color: var(--text-muted);
        }

        .data-table td { padding: 0.4rem; border-bottom: 1px solid #f1f3f4; }
        .data-table td.num { text-align: right; font-family: monospace; }
        .data-table a { color: var(--primary); text-decoration: none; }
        .data-table a:hover { text-decoration: underline; }

        .more { font-size: 0.8rem; color: var(--text-muted); margin-top: 0.5rem; }
        .more a { color: var(--primary); text-decoration: none; }
        .more a:hover { text-decoration: underline; }
        .empty { color: var(--text-muted); font-style: italic; font-size: 0.9rem; }

        .empty-state {
            text-align: center;
            padding: 4rem 2rem;
            color: var(--text-muted);
        }

        .empty-state h3 { margin-bottom: 0.5rem; }

        /* Language detail page */
        .lang-detail-container {
            max-width: 1000px;
            margin: 0 auto;
            padding: 2rem;
        }

        .lang-detail-header {
            margin-bottom: 2rem;
            padding-bottom: 1rem;
            border-bottom: 2px solid var(--primary);
        }

        .lang-detail-header h1 { font-size: 2rem; color: var(--primary-dark); }

        .breadcrumb {
            font-size: 0.9rem;
            margin-bottom: 0.5rem;
            color: var(--text-muted);
        }

        .breadcrumb a { color: var(--primary); text-decoration: none; }
        .breadcrumb a:hover { text-decoration: underline; }

        .detail-section {
            background: var(--card-bg);
            border-radius: 8px;
            padding: 1.5rem;
            margin-bottom: 1.5rem;
            border: 1px solid var(--border);
        }

        .detail-section h2 {
            font-size: 1.25rem;
            margin-bottom: 1rem;
            color: var(--primary-dark);
        }

        .info-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
            gap: 1rem;
        }

        .info-item label {
            font-size: 0.8rem;
            color: var(--text-muted);
            display: block;
        }

        .info-item .value { font-weight: 500; }

        .tech-grid {
            display: flex;
            flex-wrap: wrap;
            gap: 0.5rem;
        }

        .tech-item {
            background: #f8f9fa;
            padding: 0.4rem 0.8rem;
            border-radius: 4px;
            font-size: 0.9rem;
            border: 1px solid var(--border);
        }

        .tech-item a { color: var(--primary); text-decoration: none; }
        .tech-item a:hover { text-decoration: underline; }
        .tech-item.tech-available {
            background: #d3f9d8;
            border-color: #8ce99a;
            color: #2b8a3e;
        }

        /* All Languages table */
        .all-langs-container {
            background: var(--card-bg);
            border-radius: 8px;
            padding: 1.5rem;
            border: 1px solid var(--border);
        }

        .all-langs-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 1rem;
            flex-wrap: wrap;
            gap: 1rem;
        }

        .all-langs-header h2 { margin: 0; color: var(--primary-dark); }

        .all-langs-search {
            width: 100%;
            max-width: 400px;
            padding: 0.5rem 1rem;
            border: 1px solid var(--border);
            border-radius: 4px;
            font-size: 0.9rem;
            margin-bottom: 1rem;
        }

        .all-langs-search:focus {
            outline: none;
            border-color: var(--primary);
        }

        .all-langs-table {
            width: 100%;
            border-collapse: collapse;
            font-size: 0.9rem;
        }

        .all-langs-table th {
            text-align: left;
            padding: 0.75rem;
            border-bottom: 2px solid var(--border);
            font-weight: 600;
            color: var(--text-muted);
            cursor: pointer;
        }

        .all-langs-table th:hover { color: var(--primary); }

        .all-langs-table td {
            padding: 0.6rem 0.75rem;
            border-bottom: 1px solid #f1f3f4;
            vertical-align: top;
        }

        .all-langs-table tr:hover { background: #f8f9fa; }
        .all-langs-table a { color: var(--primary); text-decoration: none; }
        .all-langs-table a:hover { text-decoration: underline; }

        .all-langs-table .iso-code {
            font-family: monospace;
            background: var(--bg);
            padding: 0.15rem 0.4rem;
            border-radius: 3px;
            font-size: 0.85rem;
        }

        .all-langs-table .focus-row { background: #fff9db; }
        .all-langs-table .focus-row:hover { background: #fff3bf; }
        .focus-star { color: #f59f00; font-size: 1.1em; }

        .all-langs-table th.sortable { cursor: pointer; user-select: none; }
        .all-langs-table th.sortable::after { content: ' ↕'; opacity: 0.3; }
        .all-langs-table th.sorted-asc::after { content: ' ↑'; opacity: 1; }
        .all-langs-table th.sorted-desc::after { content: ' ↓'; opacity: 1; }

        .table-scroll { max-height: 70vh; overflow-y: auto; }

        /* Actors */
        .actors-grid {
            display: grid;
            gap: 1.5rem;
            grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
        }

        .actor-card {
            background: var(--card-bg);
            border-radius: 8px;
            padding: 1.25rem;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
            border: 1px solid var(--border);
        }

        .actor-card h3 { margin-bottom: 0.5rem; }
        .actor-card h3 a { color: var(--primary-dark); text-decoration: none; }
        .actor-card h3 a:hover { text-decoration: underline; }

        .actor-meta { display: flex; gap: 0.5rem; margin-bottom: 0.75rem; }

        .actor-type {
            background: var(--bg);
            padding: 0.2rem 0.5rem;
            border-radius: 4px;
            font-size: 0.8rem;
        }

        .actor-maturity {
            background: #d3f9d8;
            color: #2f9e44;
            padding: 0.2rem 0.5rem;
            border-radius: 4px;
            font-size: 0.8rem;
        }

        footer {
            text-align: center;
            padding: 2rem;
            color: var(--text-muted);
            font-size: 0.85rem;
        }

        /* Countries tab */
        .countries-container {
            background: var(--card-bg);
            border-radius: 8px;
            padding: 1.5rem;
            border: 1px solid var(--border);
        }

        .countries-header h2 {
            margin: 0 0 0.5rem 0;
            color: var(--primary-dark);
        }

        .country-select {
            padding: 0.5rem 1rem;
            font-size: 1rem;
            border: 1px solid var(--border);
            border-radius: 4px;
            background: white;
            min-width: 250px;
        }

        .country-select:focus {
            outline: none;
            border-color: var(--primary);
        }

        .tableau-container {
            width: 100%;
            min-height: 200px;
            border: 1px solid var(--border);
            border-radius: 4px;
            background: #fafafa;
        }

        .language-list-container {
            background: var(--bg);
            border-radius: 4px;
            padding: 1rem;
            border: 1px solid var(--border);
        }
    """


def get_huggingface_search_url(iso_639_1, iso_639_3, pipeline_tag):
    """Generate HuggingFace search URL for a language and task."""
    # Prefer ISO 639-1 if available, otherwise use ISO 639-3
    code = iso_639_1 if iso_639_1 else iso_639_3
    if not code:
        return None
    return f"https://huggingface.co/models?pipeline_tag={pipeline_tag}&language={code}&sort=trending"


def generate_models_table(models_data, task_name, limit=15, iso_639_1=None, iso_639_3=None, pipeline_tag=None):
    """Generate HTML table for models.

    Args:
        models_data: Either a list of models (old format) or dict with 'items', 'total_count', and 'counts_by_code' (new format)
    """
    # Handle both old format (list) and new format (dict with items/total_count)
    if isinstance(models_data, dict):
        models = models_data.get('items', [])
        total_count = models_data.get('total_count', len(models))
        counts_by_code = models_data.get('counts_by_code', {})
    else:
        models = models_data or []
        total_count = len(models)
        counts_by_code = {}

    if not models:
        return f"<p class='empty'>No {task_name} models found.</p>"

    rows = []
    for m in models[:limit]:
        name = m.get('name', 'Unknown')
        url = m.get('url', '#')
        downloads = format_number(m.get('downloads', 0))
        likes = format_number(m.get('likes', 0))

        rows.append(f"""
            <tr>
                <td><a href="{url}" target="_blank">{name}</a></td>
                <td class="num">{downloads}</td>
                <td class="num">{likes}</td>
            </tr>
        """)

    # Generate "more" links - one for each language code that has results
    more_html = ""
    if counts_by_code:
        links = []
        for code, count in sorted(counts_by_code.items(), key=lambda x: -x[1]):
            remaining = count - limit if count > limit else 0
            if remaining > 0 or count > 0:
                hf_url = f"https://huggingface.co/models?pipeline_tag={pipeline_tag}&language={code}&sort=trending"
                links.append(f'<a href="{hf_url}" target="_blank">{code}: {count}</a>')
        if links:
            more_html = f'<p class="more">View on HuggingFace: {" | ".join(links)}</p>'
    elif total_count > limit:
        # Fallback for old data format
        more = total_count - limit
        hf_url = get_huggingface_search_url(iso_639_1, iso_639_3, pipeline_tag)
        if hf_url:
            more_html = f'<p class="more"><a href="{hf_url}" target="_blank">+ {more} more on HuggingFace →</a></p>'
        else:
            more_html = f"<p class='more'>+ {more} more</p>"

    return f"""
        <table class="data-table">
            <thead>
                <tr><th>Model</th><th>Downloads</th><th>Likes</th></tr>
            </thead>
            <tbody>{''.join(rows)}</tbody>
        </table>
        {more_html}
    """


def get_huggingface_datasets_url(iso_639_1, iso_639_3, task_category):
    """Generate HuggingFace datasets search URL for a language and task."""
    code = iso_639_1 if iso_639_1 else iso_639_3
    if not code:
        return None
    return f"https://huggingface.co/datasets?task_categories=task_categories:{task_category}&language=language:{code}&sort=trending"


def generate_datasets_table(datasets_data, limit=10, iso_639_1=None, iso_639_3=None, task_category=None):
    """Generate HTML table for datasets.

    Args:
        datasets_data: Either a list of datasets (old format) or dict with 'items', 'total_count', and 'counts_by_code' (new format)
    """
    # Handle both old format (list) and new format (dict with items/total_count)
    if isinstance(datasets_data, dict):
        datasets = datasets_data.get('items', [])
        total_count = datasets_data.get('total_count', len(datasets))
        counts_by_code = datasets_data.get('counts_by_code', {})
    else:
        datasets = datasets_data or []
        total_count = len(datasets)
        counts_by_code = {}

    if not datasets:
        return "<p class='empty'>No datasets found.</p>"

    rows = []
    for d in datasets[:limit]:
        name = d.get('name', 'Unknown')
        url = d.get('url', '#')
        downloads = format_number(d.get('downloads', 0))

        rows.append(f"""
            <tr>
                <td><a href="{url}" target="_blank">{name}</a></td>
                <td class="num">{downloads}</td>
            </tr>
        """)

    # Generate "more" links - one for each language code that has results
    more_html = ""
    if counts_by_code:
        links = []
        for code, count in sorted(counts_by_code.items(), key=lambda x: -x[1]):
            if count > 0:
                hf_url = f"https://huggingface.co/datasets?task_categories=task_categories:{task_category}&language=language:{code}&sort=trending"
                links.append(f'<a href="{hf_url}" target="_blank">{code}: {count}</a>')
        if links:
            more_html = f'<p class="more">View on HuggingFace: {" | ".join(links)}</p>'
    elif total_count > limit:
        # Fallback for old data format
        more = total_count - limit
        hf_url = get_huggingface_datasets_url(iso_639_1, iso_639_3, task_category)
        if hf_url:
            more_html = f'<p class="more"><a href="{hf_url}" target="_blank">+ {more} more on HuggingFace →</a></p>'
        else:
            more_html = f"<p class='more'>+ {more} more</p>"

    return f"""
        <table class="data-table">
            <thead>
                <tr><th>Dataset</th><th>Downloads</th></tr>
            </thead>
            <tbody>{''.join(rows)}</tbody>
        </table>
        {more_html}
    """


def get_model_count(models_data):
    """Get total count from models data (handles both old list format and new dict format)."""
    if isinstance(models_data, dict):
        return models_data.get('total_count', len(models_data.get('items', [])))
    return len(models_data) if models_data else 0


def generate_language_card(iso_code, lang_data, actors):
    """Generate HTML card for a language."""
    info = lang_data.get('info', {})
    models = lang_data.get('models', {})
    benchmarks = lang_data.get('benchmarks', {})

    name = info.get('name', iso_code)
    iso3 = info.get('iso_639_3', iso_code)
    iso1 = info.get('iso_639_1', '')
    altnames = info.get('altnames', [])
    countries = info.get('countries', [])

    # Wikipedia info
    wiki_data = info.get('wikipedia', {}) or {}
    family = wiki_data.get('family', '') or info.get('family', '')
    speakers_l1 = wiki_data.get('speakers_l1', '') or info.get('speakers_l1', '')

    detail_url = f"lang/{iso_code}.html"

    # Countries tags
    countries_html = ""
    if countries:
        wca_countries = [c for c in countries if c in WCA_COUNTRIES][:5]
        if wca_countries:
            tags = ''.join(f'<span class="country-tag">{c}</span>' for c in wca_countries)
            countries_html = f'<div class="country-tags">{tags}</div>'

    # Altnames
    altnames_html = ""
    if altnames:
        display = altnames[:4]
        more = len(altnames) - 4
        s = ', '.join(display) + (f' (+{more})' if more > 0 else '')
        altnames_html = f'<div class="altnames"><em>Also:</em> {s}</div>'

    # Common Voice
    cv = benchmarks.get('common_voice') or {}
    cv_html = ""
    if cv:
        cv_html = f"""
            <div class="cv-stats">
                <strong>Common Voice:</strong> {cv.get('total_hours', 0)} hours,
                {cv.get('total_clips', 0)} clips
            </div>
        """

    # Model counts (use total_count from HuggingFace, not just fetched items)
    asr_data = models.get('asr', {})
    tts_data = models.get('tts', {})
    mt_data = models.get('translation', {})
    llm_data = models.get('llm', {})

    asr_count = get_model_count(asr_data)
    tts_count = get_model_count(tts_data)
    mt_count = get_model_count(mt_data)
    llm_count = get_model_count(llm_data)

    # Actors working on this language
    lang_actors = get_actors_for_language(iso_code, actors)
    actor_count = len(lang_actors)

    return f"""
        <div class="language-card" id="lang-{iso_code}">
            <div class="lang-header">
                <h3><a href="{detail_url}">{name}</a></h3>
                <span class="lang-codes">{iso3}{f' / {iso1}' if iso1 else ''}</span>
            </div>

            {countries_html}
            {altnames_html}

            <div class="lang-meta">
                {f'<div><strong>Family:</strong> {family}</div>' if family else ''}
                {f'<div><strong>Speakers:</strong> {speakers_l1}</div>' if speakers_l1 else ''}
            </div>

            {cv_html}

            {f'<div class="model-summary"><span class="badge" style="background: #ffe8cc; color: #d9480f;">{actor_count} Actor{"s" if actor_count != 1 else ""} working on this language</span></div>' if actor_count > 0 else ''}

            <details class="models-section">
                <summary>ASR Models ({asr_count})</summary>
                {generate_models_table(asr_data, 'ASR', limit=5, iso_639_1=iso1, iso_639_3=iso3, pipeline_tag='automatic-speech-recognition')}
            </details>

            <details class="models-section">
                <summary>TTS Models ({tts_count})</summary>
                {generate_models_table(tts_data, 'TTS', limit=5, iso_639_1=iso1, iso_639_3=iso3, pipeline_tag='text-to-speech')}
            </details>

            <details class="models-section">
                <summary>MT Models ({mt_count})</summary>
                {generate_models_table(mt_data, 'translation', limit=5, iso_639_1=iso1, iso_639_3=iso3, pipeline_tag='translation')}
            </details>

            <details class="models-section">
                <summary>LLM Models ({llm_count})</summary>
                {generate_models_table(llm_data, 'LLM', limit=5, iso_639_1=iso1, iso_639_3=iso3, pipeline_tag='text-generation')}
            </details>
        </div>
    """


def generate_language_detail_page(iso_code, lang_data, actors):
    """Generate a full detail page for a language."""
    info = lang_data.get('info', {})
    models = lang_data.get('models', {})
    datasets = lang_data.get('datasets', {})
    benchmarks = lang_data.get('benchmarks', {})
    notes = lang_data.get('notes', '')

    name = info.get('name', iso_code)
    iso3 = info.get('iso_639_3', iso_code)
    iso1 = info.get('iso_639_1', '')
    name_french = info.get('name_french', '')
    altnames = info.get('altnames', [])
    glottocode = info.get('glottocode', '')
    glottocode_url = info.get('glottocode_url', '')

    countries = info.get('countries', [])
    population = info.get('population', '')
    population_order = info.get('population_order', '')
    endangerment = info.get('endangerment', '')

    wiki_data = info.get('wikipedia', {}) or {}
    wiki_url = wiki_data.get('url', '')
    wiki_family = wiki_data.get('family', '')
    wiki_speakers_l1 = wiki_data.get('speakers_l1', '')
    wiki_speakers_l2 = wiki_data.get('speakers_l2', '')
    wiki_writing = wiki_data.get('writing_system', '')

    tech_resources = info.get('tech_resources', {}) or {}
    resource_links = info.get('resource_links', {}) or {}

    # Glottocode with link
    glotto_html = '—'
    if glottocode:
        if glottocode_url:
            glotto_html = f'<a href="{glottocode_url}" target="_blank">{glottocode}</a>'
        else:
            glotto_html = glottocode

    # Wikipedia section
    wiki_section = ""
    if wiki_url or wiki_family:
        wiki_link = f'<a href="{wiki_url}" target="_blank">{name} on Wikipedia</a>' if wiki_url else '—'
        wiki_section = f"""
            <div class="detail-section">
                <h2>📖 Wikipedia</h2>
                <div class="info-grid">
                    <div class="info-item"><label>Wikipedia</label><span class="value">{wiki_link}</span></div>
                    <div class="info-item"><label>Language Family</label><span class="value">{wiki_family or '—'}</span></div>
                    <div class="info-item"><label>L1 Speakers</label><span class="value">{wiki_speakers_l1 or '—'}</span></div>
                    <div class="info-item"><label>L2 Speakers</label><span class="value">{wiki_speakers_l2 or '—'}</span></div>
                    <div class="info-item" style="grid-column: 1 / -1;"><label>Writing System</label><span class="value">{wiki_writing or '—'}</span></div>
                </div>
            </div>
        """

    # Tech resources
    tech_section = ""
    if tech_resources or resource_links:
        items = []
        for k, url in resource_links.items():
            if url:
                items.append(f'<div class="tech-item"><a href="{url}" target="_blank">{k}</a></div>')
        for k, v in tech_resources.items():
            if v is True:
                items.append(f'<div class="tech-item tech-available">✓ {k}</div>')
            elif isinstance(v, str) and v.startswith('http'):
                items.append(f'<div class="tech-item"><a href="{v}" target="_blank">{k}</a></div>')
            elif v:
                items.append(f'<div class="tech-item tech-available">✓ {k}: {v}</div>')
        if items:
            tech_section = f"""
                <div class="detail-section">
                    <h2>🤖 NLP & Tech Resources</h2>
                    <div class="tech-grid">{''.join(items)}</div>
                </div>
            """

    # Common Voice
    cv = benchmarks.get('common_voice') or {}
    cv_section = ""
    if cv:
        cv_section = f"""
            <div class="detail-section">
                <h2>🎙️ Common Voice</h2>
                <div class="info-grid">
                    <div class="info-item"><label>Total Hours</label><span class="value">{cv.get('total_hours', 0)}</span></div>
                    <div class="info-item"><label>Total Clips</label><span class="value">{cv.get('total_clips', 0)}</span></div>
                    <div class="info-item"><label>Validated</label><span class="value">{cv.get('validated_clips', 0)}</span></div>
                    <div class="info-item"><label>Gender</label><span class="value">♂ {cv.get('male_percent', 0)}% / ♀ {cv.get('female_percent', 0)}%</span></div>
                </div>
            </div>
        """

    # Notes
    notes_section = ""
    if notes and notes.strip() and '(Add' not in notes:
        notes_section = f"""
            <div class="detail-section">
                <h2>📝 Notes</h2>
                <div>{markdown_to_html(notes)}</div>
            </div>
        """

    # Actors working on this language
    lang_actors = get_actors_for_language(iso_code, actors)
    actors_section = ""
    if lang_actors:
        actor_items = []
        for actor in lang_actors:
            actor_name = actor.get('name', '')
            actor_id = actor.get('id', '')
            actor_type = format_actor_type(actor.get('type', ''))
            actor_desc = actor.get('description', '')
            # Truncate description
            if actor_desc and len(actor_desc) > 150:
                actor_desc = actor_desc[:150] + '...'
            actor_items.append(f'''
                <div style="background: var(--bg); padding: 0.75rem; border-radius: 4px; margin-bottom: 0.5rem;">
                    <strong><a href="../actor/{actor_id}.html">{actor_name}</a></strong>
                    <span style="color: var(--text-muted); font-size: 0.85rem;">({actor_type})</span>
                    {f'<p style="margin: 0.25rem 0 0 0; font-size: 0.9rem;">{actor_desc}</p>' if actor_desc else ''}
                </div>
            ''')
        actors_section = f"""
            <div class="detail-section">
                <h2>👥 Actors ({len(lang_actors)})</h2>
                {''.join(actor_items)}
            </div>
        """

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{name} - UNICEF WCARO NLP</title>
    <link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>🌍</text></svg>">
    <style>{get_css()}</style>
</head>
<body>
    <header>
        <div>
            <h1><a href="../index.html">UNICEF WCARO NLP Landscape</a></h1>
            <div class="subtitle">West and Central Africa Language Technology</div>
        </div>
        <div class="updated">Last updated: {datetime.now().strftime("%Y-%m-%d")}</div>
    </header>

    <div class="disclaimer">
        Work in progress. Some data may contain inaccuracies.
        <a href="https://github.com/translatorswb/wca-nlp-landscape" target="_blank">Contribute on GitHub</a>
    </div>

    <div class="lang-detail-container">
        <div class="breadcrumb">
            <a href="../index.html">Home</a> &gt; {name}
        </div>

        <div class="lang-detail-header">
            <h1>{name}</h1>
            <div class="lang-codes">{iso3}{f' / {iso1}' if iso1 else ''}</div>
        </div>

        <div class="detail-section">
            <h2>🌍 General Information</h2>
            <div class="info-grid">
                <div class="info-item"><label>ISO 639-3</label><span class="value">{iso3}</span></div>
                <div class="info-item"><label>ISO 639-1</label><span class="value">{iso1 or '—'}</span></div>
                <div class="info-item"><label>French Name</label><span class="value">{name_french or '—'}</span></div>
                <div class="info-item"><label>Glottocode</label><span class="value">{glotto_html}</span></div>
                <div class="info-item"><label>Population</label><span class="value">{population or '—'} {f'({population_order})' if population_order else ''}</span></div>
                <div class="info-item"><label>Endangerment</label><span class="value">{endangerment or '—'}</span></div>
                <div class="info-item" style="grid-column: 1 / -1;"><label>Countries</label><span class="value">{', '.join(countries) if countries else '—'}</span></div>
                {f'<div class="info-item" style="grid-column: 1 / -1;"><label>Also Known As</label><span class="value">{", ".join(altnames[:10])}</span></div>' if altnames else ''}
            </div>
        </div>

        {wiki_section}
        {tech_section}
        {cv_section}
        {actors_section}
        {notes_section}

        <div class="detail-section">
            <h2>ASR Models ({get_model_count(models.get('asr', {}))})</h2>
            {generate_models_table(models.get('asr', {}), 'ASR', limit=20, iso_639_1=iso1, iso_639_3=iso3, pipeline_tag='automatic-speech-recognition')}
        </div>

        <div class="detail-section">
            <h2>TTS Models ({get_model_count(models.get('tts', {}))})</h2>
            {generate_models_table(models.get('tts', {}), 'TTS', limit=20, iso_639_1=iso1, iso_639_3=iso3, pipeline_tag='text-to-speech')}
        </div>

        <div class="detail-section">
            <h2>MT Models ({get_model_count(models.get('translation', {}))})</h2>
            {generate_models_table(models.get('translation', {}), 'translation', limit=20, iso_639_1=iso1, iso_639_3=iso3, pipeline_tag='translation')}
        </div>

        <div class="detail-section">
            <h2>LLM Models ({get_model_count(models.get('llm', {}))})</h2>
            {generate_models_table(models.get('llm', {}), 'LLM', limit=20, iso_639_1=iso1, iso_639_3=iso3, pipeline_tag='text-generation')}
        </div>

        <div class="detail-section">
            <h2>Datasets</h2>
            <h3>ASR Datasets ({get_model_count(datasets.get('asr', {}))})</h3>
            {generate_datasets_table(datasets.get('asr', {}), limit=20, iso_639_1=iso1, iso_639_3=iso3, task_category='automatic-speech-recognition')}
            <h3 style="margin-top: 1rem;">TTS Datasets ({get_model_count(datasets.get('tts', {}))})</h3>
            {generate_datasets_table(datasets.get('tts', {}), limit=20, iso_639_1=iso1, iso_639_3=iso3, task_category='text-to-speech')}
        </div>
    </div>

    <footer>
        Generated: {datetime.now().strftime("%Y-%m-%d %H:%M")} | CLEAR Global for UNICEF WCARO
    </footer>
</body>
</html>
"""


def generate_focus_languages_tab(languages, actors):
    """Generate the Focus Languages tab content."""
    if not languages:
        return """
            <div class="empty-state">
                <h3>No focus languages yet</h3>
                <p>Add ISO codes to Research/focused_languages.yaml and run populate_research.py</p>
            </div>
        """

    cards = []
    for iso_code, lang_data in sorted(languages.items(), key=lambda x: x[1].get('info', {}).get('name', '')):
        cards.append(generate_language_card(iso_code, lang_data, actors))

    return f"""
        <div class="languages-grid">
            {''.join(cards)}
        </div>
    """


def generate_all_languages_tab(wca_languages, focus_languages):
    """Generate the All Languages tab - table of all WCA languages."""
    if not wca_languages:
        return """
            <div class="empty-state">
                <h3>No WCA languages data</h3>
                <p>Run: python scripts/populate_research.py --generate-wca-list</p>
            </div>
        """

    focus_iso_set = set(focus_languages.keys())

    rows = []
    for lang in wca_languages:
        name = lang.get('name', '')
        iso3 = lang.get('iso_639_3', '')
        countries = lang.get('countries', [])
        wca_countries = set(lang.get('wca_countries', countries))  # Fallback to all if not present
        population = lang.get('population', '')
        endangerment = lang.get('endangerment', '')

        is_focus = iso3 in focus_iso_set
        focus_html = '<span class="focus-star">★</span>' if is_focus else ''

        if is_focus:
            name_html = f'<a href="lang/{iso3}.html">{name}</a>'
        else:
            name_html = name

        # Format countries: WCA countries normal, others in gray
        country_parts = []
        for c in countries[:6]:
            if c in wca_countries:
                country_parts.append(c)
            else:
                country_parts.append(f'<span style="color:#999">{c}</span>')
        countries_html = ', '.join(country_parts) + (f' <span style="color:#999">+{len(countries)-6}</span>' if len(countries) > 6 else '')

        # Parse population for sorting
        pop_numeric = 0
        if population:
            import re
            pop_str = str(population).replace(',', '').replace(' ', '')
            match = re.search(r'\d+', pop_str)
            if match:
                pop_numeric = int(match.group())

        row_class = 'focus-row' if is_focus else ''
        rows.append(f"""
            <tr class="{row_class}" data-name="{name.lower()}" data-iso="{iso3.lower()}" data-countries="{' '.join(countries).lower()}" data-focus="{1 if is_focus else 0}" data-pop="{pop_numeric}">
                <td>{focus_html}</td>
                <td>{name_html}</td>
                <td><span class="iso-code">{iso3}</span></td>
                <td>{countries_html}</td>
                <td>{population or '—'}</td>
                <td>{endangerment or '—'}</td>
            </tr>
        """)

    return f"""
        <div class="all-langs-container">
            <div class="all-langs-header">
                <h2>All WCA Languages</h2>
                <span>{len(wca_languages)} languages | {len(focus_iso_set)} focus</span>
            </div>

            <input type="text" class="all-langs-search" id="langSearch"
                   placeholder="Search by name, ISO code, or country...">

            <div class="table-scroll">
                <table class="all-langs-table" id="allLangsTable">
                    <thead>
                        <tr>
                            <th class="sortable" data-sort="focus" style="width:30px">★</th>
                            <th class="sortable" data-sort="name">Language</th>
                            <th class="sortable" data-sort="iso">ISO</th>
                            <th>Countries</th>
                            <th class="sortable sorted-desc" data-sort="pop">Population</th>
                            <th class="sortable" data-sort="status">Status</th>
                        </tr>
                    </thead>
                    <tbody>
                        {''.join(rows)}
                    </tbody>
                </table>
            </div>
        </div>
    """


def generate_countries_tab(wca_languages):
    """Generate the Countries tab with Tableau embeds."""
    # WCA countries with LUDP data: (display_name, tableau_share_code, url_country_name, admin_level)
    # Countries without LUDP data have tableau_share_code = None
    wca_countries_list = [
        ('Benin', '7QXX3JMG4', 'Benin', 2),
        ('Burkina Faso', 'QWRMKWW69', 'Burkina+Faso', 1),
        ('Cameroon', None, None, None),  # Not in LUDP
        ('Central African Republic', None, None, None),  # Not in LUDP
        ('Chad', None, None, None),  # Not in LUDP
        ('Republic of the Congo', 'JJ6B67N2W', 'Congo', 1),
        ("Côte d'Ivoire", None, None, None),  # Not in LUDP
        ('DR Congo', 'GHSXDN7GS', 'Congo+%28Democratic+Republic+of+the%29', 2),
        ('Equatorial Guinea', None, None, None),  # Not in LUDP
        ('Gabon', None, None, None),  # Not in LUDP
        ('The Gambia', '4JPTWTM9D', 'Gambia', 2),
        ('Ghana', 'Q2RSMMJ6H', 'Ghana', 2),
        ('Guinea', 'BNK8HNX6W', 'Guinea', 2),
        ('Guinea-Bissau', None, None, None),  # Not in LUDP
        ('Liberia', None, None, None),  # Not in LUDP
        ('Mali', 'ZHP6RGQFP', 'Mali', 2),
        ('Mauritania', None, None, None),  # Not in LUDP
        ('Niger', 'JTCYDTKNT', 'Niger', 2),
        ('Nigeria', 'QDH9D9KQK', 'Nigeria', 2),
        ('São Tomé and Príncipe', None, None, None),  # Not in LUDP
        ('Senegal', 'JRKYP5P3P', 'Senegal', 2),
        ('Sierra Leone', 'SRC996MM2', 'Sierra+Leone', 2),
        ('Togo', None, None, None),  # Not in LUDP
    ]

    # Build country data as JSON for JavaScript
    import json
    countries_data = []
    for display_name, share_code, url_name, level in wca_countries_list:
        countries_data.append({
            'name': display_name,
            'shareCode': share_code,
            'urlName': url_name,
            'level': level
        })
    countries_json = json.dumps(countries_data)

    # Build language data by country for the language lists
    # Group languages by country
    langs_by_country = {}
    for lang in wca_languages:
        for country in lang.get('countries', []):
            if country not in langs_by_country:
                langs_by_country[country] = []
            langs_by_country[country].append(lang)

    # Sort languages by population within each country
    for country in langs_by_country:
        langs_by_country[country].sort(
            key=lambda x: int(str(x.get('population', '0')).replace(',', '').split()[0] or 0) if x.get('population') else 0,
            reverse=True
        )

    langs_by_country_json = json.dumps(langs_by_country)

    # Load focus languages for highlighting
    focus_languages_path = RESEARCH_DIR / "focused_languages.yaml"
    focus_langs = []
    if focus_languages_path.exists():
        with open(focus_languages_path, 'r') as f:
            focus_langs = yaml.safe_load(f) or []
    focus_langs_json = json.dumps(focus_langs)

    # Build country options for dropdown (with empty default)
    options_html = '<option value="">— Select a country —</option>\n' + '\n'.join(
        f'<option value="{display_name}">{display_name}</option>'
        for display_name, _, _, _ in wca_countries_list
    )

    return f"""
        <div class="countries-container">
            <div class="countries-header">
                <h2>Language Use by Country</h2>
                <p style="color: var(--text-muted); margin-bottom: 1rem;">
                    Data from <a href="https://clearglobal.org/language-use-data-platform/" target="_blank">CLEAR Global's Language Use Data Platform</a>.
                    Shows main languages spoken at home by proportion of population.
                </p>
                <div style="margin-bottom: 1rem;">
                    <label for="countrySelect" style="font-weight: 500; margin-right: 0.5rem;">Select Country:</label>
                    <select id="countrySelect" class="country-select">
                        {options_html}
                    </select>
                </div>
            </div>

            <div id="tableauContainer" class="tableau-container" style="display: flex; align-items: center; justify-content: center; color: var(--text-muted);">
                <p>Select a country to view language data</p>
            </div>

            <p id="platformLinkContainer" style="margin-top: 1rem; font-size: 0.85rem; color: var(--text-muted); display: none;">
                <a id="platformLink" href="#" target="_blank">Open full interactive platform for <span id="platformCountryName"></span> →</a>
            </p>

            <div id="languageListContainer" class="language-list-container" style="margin-top: 1.5rem; display: none;">
                <h3 style="margin-bottom: 0.5rem; color: var(--primary-dark);">Languages spoken in <span id="langListCountryName"></span></h3>
                <p style="font-size: 0.85rem; color: var(--text-muted); margin-bottom: 1rem;">
                    Note: Population figures represent total global speakers of each language, not speakers within this country specifically.
                </p>
                <div id="languageList" class="table-scroll" style="max-height: 400px;">
                    <!-- Language list will be inserted here -->
                </div>
            </div>
        </div>

        <script type='text/javascript'>
            // Country data with LUDP share codes
            const countriesData = {countries_json};
            const langsByCountry = {langs_by_country_json};
            const focusLanguages = {focus_langs_json};

            // Mapping from display names to data names (for language lookup)
            const countryNameMapping = {{
                "DR Congo": "Democratic Republic of Congo",
                "Republic of the Congo": "Republic of Congo",
                "The Gambia": "Gambia",
                "Côte d'Ivoire": "Cote d'Ivoire",
                "São Tomé and Príncipe": "São Tomé e Príncipe"
            }};

            function getDataCountryName(displayName) {{
                return countryNameMapping[displayName] || displayName;
            }}

            function getCountryData(countryName) {{
                return countriesData.find(c => c.name === countryName);
            }}

            function loadTableauViz(shareCode, urlName, level) {{
                const container = document.getElementById('tableauContainer');
                const vizId = 'viz_' + Date.now();

                container.innerHTML = `
                    <div class='tableauPlaceholder' id='${{vizId}}' style='position: relative'>
                        <noscript>
                            <a href='https://clearglobal.org/'>
                                <img alt='Location Dashboard' src='https://public.tableau.com/static/images/${{shareCode.substring(0,2)}}/${{shareCode}}/1_rss.png' style='border: none' />
                            </a>
                        </noscript>
                        <object class='tableauViz' style='display:none;'>
                            <param name='host_url' value='https%3A%2F%2Fpublic.tableau.com%2F' />
                            <param name='embed_code_version' value='3' />
                            <param name='path' value='shared/${{shareCode}}' />
                            <param name='toolbar' value='yes' />
                            <param name='device' value='default' />
                            <param name='static_image' value='https://public.tableau.com/static/images/${{shareCode.substring(0,2)}}/${{shareCode}}/1.png' />
                            <param name='animate_transition' value='yes' />
                            <param name='display_static_image' value='yes' />
                            <param name='display_spinner' value='yes' />
                            <param name='display_overlay' value='yes' />
                            <param name='display_count' value='yes' />
                            <param name='tabs' value='n' />
                            <param name='filter' value='Country=${{urlName}}' />
                            <param name='filter' value='Select+View=Map' />
                            <param name='filter' value='Location+Level+Parameter=${{level}}' />
                        </object>
                    </div>
                `;

                // Set dimensions like the original embed code
                const divElement = document.getElementById(vizId);
                const vizElement = divElement.getElementsByTagName('object')[0];
                if (divElement.offsetWidth > 800) {{
                    vizElement.style.width = '100%';
                    vizElement.style.height = (divElement.offsetWidth * 0.75) + 'px';
                }} else if (divElement.offsetWidth > 500) {{
                    vizElement.style.width = '100%';
                    vizElement.style.height = (divElement.offsetWidth * 0.75) + 'px';
                }} else {{
                    vizElement.style.width = '100%';
                    vizElement.style.height = '727px';
                }}

                // Load Tableau JS API
                const scriptElement = document.createElement('script');
                scriptElement.src = 'https://public.tableau.com/javascripts/api/viz_v1.js';
                vizElement.parentNode.insertBefore(scriptElement, vizElement);
            }}

            function showNoLudpMessage(countryName) {{
                const container = document.getElementById('tableauContainer');
                container.innerHTML = `
                    <div style="padding: 2.5rem; text-align: center;">
                        <div style="font-size: 2rem; margin-bottom: 1rem; opacity: 0.3;">🗺️</div>
                        <p style="font-size: 1rem; color: var(--text-muted); margin-bottom: 0.5rem;">
                            Language use data not yet available for <strong>${{countryName}}</strong> in CLEAR Global's platform.
                        </p>
                        <p style="font-size: 0.9rem; color: var(--text-muted);">
                            See the language list below based on other sources.
                        </p>
                    </div>
                `;
            }}

            function updatePlatformLink(countryData) {{
                const linkContainer = document.getElementById('platformLinkContainer');
                const link = document.getElementById('platformLink');
                const nameSpan = document.getElementById('platformCountryName');

                if (countryData.shareCode) {{
                    linkContainer.style.display = 'block';
                    const urlCountry = countryData.urlName.replace(/\+/g, '%20');
                    link.href = 'https://clearglobal.org/language-use-data-platform/?dash=LocationDashboard&country=' + urlCountry + '&view=Map&level=' + countryData.level;
                    nameSpan.textContent = countryData.name;
                }} else {{
                    linkContainer.style.display = 'none';
                }}
            }}

            function updateLanguageList(countryName) {{
                const container = document.getElementById('languageList');
                const listContainer = document.getElementById('languageListContainer');
                const nameSpan = document.getElementById('langListCountryName');
                nameSpan.textContent = countryName;
                listContainer.style.display = 'block';

                // Use mapped name for data lookup
                const dataCountryName = getDataCountryName(countryName);
                const langs = langsByCountry[dataCountryName] || [];

                if (langs.length === 0) {{
                    container.innerHTML = '<p class="empty">No language data available for this country.</p>';
                    return;
                }}

                // Build table
                let rows = langs.slice(0, 50).map(lang => {{
                    const iso = lang.iso_639_3 || '';
                    const name = lang.name || '';
                    const pop = lang.population || '—';
                    const status = lang.endangerment || '—';
                    const isFocus = focusLanguages.includes(iso);

                    // Name with link if focus language
                    const nameHtml = isFocus
                        ? `<a href="lang/${{iso}}.html">${{name}}</a>`
                        : name;

                    // Focus star
                    const focusHtml = isFocus
                        ? '<span class="focus-star">★</span>'
                        : '';

                    const rowClass = isFocus ? 'focus-row' : '';

                    return `<tr class="${{rowClass}}">
                        <td>${{focusHtml}}</td>
                        <td>${{nameHtml}}</td>
                        <td><span class="iso-code">${{iso}}</span></td>
                        <td>${{pop}}</td>
                        <td>${{status}}</td>
                    </tr>`;
                }}).join('');

                const moreCount = langs.length > 50 ? langs.length - 50 : 0;
                const moreHtml = moreCount > 0 ? `<p class="more">+ ${{moreCount}} more languages</p>` : '';

                container.innerHTML = `
                    <table class="all-langs-table">
                        <thead>
                            <tr>
                                <th style="width:30px">★</th>
                                <th>Language</th>
                                <th>ISO</th>
                                <th>Population</th>
                                <th>Status</th>
                            </tr>
                        </thead>
                        <tbody>${{rows}}</tbody>
                    </table>
                    ${{moreHtml}}
                `;
            }}

            function loadCountry(countryName) {{
                const countryData = getCountryData(countryName);
                if (!countryData) return;

                if (countryData.shareCode) {{
                    loadTableauViz(countryData.shareCode, countryData.urlName, countryData.level);
                }} else {{
                    showNoLudpMessage(countryName);
                }}

                updatePlatformLink(countryData);
                updateLanguageList(countryName);
            }}

            // Country selector change handler
            document.getElementById('countrySelect').addEventListener('change', function() {{
                if (this.value) {{
                    loadCountry(this.value);
                }}
            }});
        </script>
    """


def generate_actors_tab(actors):
    """Generate the Actors tab content."""
    if not actors:
        return """
            <div class="empty-state">
                <h3>No actors added yet</h3>
                <p>Add actor YAML files to Research/Actors/</p>
            </div>
        """

    cards = []
    for actor_key, actor_data in actors.items():
        # Skip template
        if actor_key == 'actor-template':
            continue

        name = actor_data.get('name', actor_key)
        actor_id = actor_data.get('id', actor_key)
        actor_type = actor_data.get('type', '')
        website = actor_data.get('website', '')
        languages = actor_data.get('languages', [])
        actor_countries = actor_data.get('countries', [])
        maturity = actor_data.get('maturity', '')
        location = actor_data.get('location', '')
        founded = actor_data.get('founded', '')
        description = actor_data.get('description', '')
        github = actor_data.get('github', '')
        huggingface = actor_data.get('huggingface', '')
        engagement_status = actor_data.get('engagement_status', '')

        detail_url = f"actor/{actor_id}.html"

        # Truncate description
        desc_short = (description[:150] + '...') if description and len(description) > 150 else description

        # Links row
        links = []
        if website:
            links.append(f'<a href="{website}" target="_blank">🌐 Website</a>')
        if github:
            links.append(f'<a href="{github}" target="_blank">📦 GitHub</a>')
        if huggingface:
            links.append(f'<a href="{huggingface}" target="_blank">🤗 HuggingFace</a>')
        links_html = ' · '.join(links) if links else ''

        # Engagement status badge - only show if not "none"
        status_colors = {
            'contacted': '#fab005',
            'in_discussion': '#15aabf',
            'active_partner': '#40c057'
        }
        status_badge = ''
        if engagement_status and engagement_status != 'none':
            status_color = status_colors.get(engagement_status, '#868e96')
            status_badge = f'<span style="background: {status_color}; color: white; padding: 0.2rem 0.5rem; border-radius: 4px; font-size: 0.8rem;">{engagement_status}</span>'

        # Convert country codes to names
        country_names = country_codes_to_names(actor_countries)
        actor_type_display = format_actor_type(actor_type)

        cards.append(f"""
            <div class="actor-card">
                <h3><a href="{detail_url}">{name}</a></h3>
                <div class="actor-meta">
                    <span class="actor-type">{actor_type_display}</span>
                    {f'<span class="actor-maturity">{maturity}</span>' if maturity else ''}
                    {status_badge}
                </div>
                {f'<div style="font-size: 0.85rem; color: var(--text-muted); margin-bottom: 0.5rem;">{location} · Est. {founded}</div>' if location or founded else ''}
                {f'<div style="font-size: 0.9rem; margin-bottom: 0.75rem;">{desc_short}</div>' if desc_short else ''}
                <div style="font-size: 0.85rem; margin-bottom: 0.5rem;">{links_html}</div>
                <div style="font-size: 0.85rem;"><strong>Countries:</strong> {', '.join(country_names[:5]) if country_names else '—'}{f' +{len(country_names)-5}' if len(country_names) > 5 else ''}</div>
                <div style="font-size: 0.85rem;"><strong>Languages:</strong> {', '.join(str(l) for l in languages[:5]) if languages else '—'}{f' +{len(languages)-5}' if len(languages) > 5 else ''}</div>
            </div>
        """)

    return f"""
        <div class="actors-grid">
            {''.join(cards)}
        </div>
    """


def generate_actor_detail_page(actor_key, actor_data):
    """Generate a full detail page for an actor."""
    name = actor_data.get('name', actor_key)
    actor_id = actor_data.get('id', actor_key)
    actor_type = actor_data.get('type', '')
    website = actor_data.get('website', '')
    location = actor_data.get('location', '')
    languages = actor_data.get('languages', [])
    actor_countries = actor_data.get('countries', [])
    maturity = actor_data.get('maturity', '')
    description = actor_data.get('description', '')
    notes = actor_data.get('notes', '')
    projects = actor_data.get('projects', [])

    # New fields
    founded = actor_data.get('founded', '')
    organization_size = actor_data.get('organization_size', '')
    funding = actor_data.get('funding', '')
    github = actor_data.get('github', '')
    huggingface = actor_data.get('huggingface', '')
    publications = actor_data.get('publications', [])
    partnerships = actor_data.get('partnerships', [])
    unicef_relevance = actor_data.get('unicef_relevance', '')
    engagement_status = actor_data.get('engagement_status', '')
    last_updated = actor_data.get('last_updated', '')

    # Contact can be string or dict
    contact = actor_data.get('contact', '')
    if isinstance(contact, dict):
        contact_parts = []
        if contact.get('email'):
            contact_parts.append(f'<a href="mailto:{contact["email"]}">{contact["email"]}</a>')
        if contact.get('mailing_list'):
            contact_parts.append(f'<a href="{contact["mailing_list"]}" target="_blank">Mailing list</a>')
        if contact.get('slack'):
            contact_parts.append(f'<a href="{contact["slack"]}" target="_blank">Slack</a>')
        contact_html = ' · '.join(contact_parts) if contact_parts else '—'
    else:
        contact_html = f'<a href="mailto:{contact}">{contact}</a>' if contact and '@' in str(contact) else (contact or '—')

    website_html = f'<a href="{website}" target="_blank">{website}</a>' if website else '—'
    github_html = f'<a href="{github}" target="_blank">{github}</a>' if github else '—'
    huggingface_html = format_huggingface_link(huggingface)
    actor_type_display = format_actor_type(actor_type)

    # Projects section - handle both list of strings and list of dicts with URLs
    projects_url = actor_data.get('projects_url', '')
    projects_html = ""
    if projects:
        if isinstance(projects, list):
            items = []
            for p in projects:
                if isinstance(p, dict):
                    pname = p.get("name", "")
                    purl = p.get("url", "")
                    pdesc = p.get("description", "")
                    if purl:
                        items.append(f'<li><strong><a href="{purl}" target="_blank">{pname}</a></strong>: {pdesc}</li>')
                    else:
                        items.append(f'<li><strong>{pname}</strong>: {pdesc}</li>')
                else:
                    items.append(f'<li>{p}</li>')
            more_link = f'<p style="margin-top: 1rem;"><a href="{projects_url}" target="_blank">View all projects →</a></p>' if projects_url else ''
            projects_html = f"""
                <div class="detail-section">
                    <h2>Projects</h2>
                    <ul>{''.join(items)}</ul>
                    {more_link}
                </div>
            """

    # Publications section - handle both list of strings and list of dicts with URLs
    publications = actor_data.get('publications', [])
    publications_url = actor_data.get('publications_url', '')
    publications_html = ""
    if publications:
        items = []
        for p in publications:
            if isinstance(p, dict):
                ptitle = p.get("title", "")
                purl = p.get("url", "")
                pvenue = p.get("venue", "")
                venue_str = f' <span style="color: var(--text-muted);">({pvenue})</span>' if pvenue else ''
                if purl:
                    items.append(f'<li><a href="{purl}" target="_blank">{ptitle}</a>{venue_str}</li>')
                else:
                    items.append(f'<li>{ptitle}{venue_str}</li>')
            else:
                items.append(f'<li>{p}</li>')

        more_link = f'<p style="margin-top: 1rem;"><a href="{publications_url}" target="_blank">View all publications →</a></p>' if publications_url else ''
        publications_html = f"""
            <div class="detail-section">
                <h2>Publications</h2>
                <ul>{''.join(items)}</ul>
                {more_link}
            </div>
        """

    # Key people section
    key_people = actor_data.get('key_people', [])
    people_html = ""
    if key_people:
        items = []
        for m in key_people:
            if isinstance(m, dict):
                mname = m.get("name", "")
                mrole = m.get("role", "")
                maffil = m.get("affiliation", "")
                mnote = m.get("note", "")
                affil_str = f' ({maffil})' if maffil else ''
                items.append(f'<li><strong>{mname}</strong> - {mrole}{affil_str}<br><span style="font-size: 0.85rem; color: var(--text-muted);">{mnote}</span></li>')
            else:
                items.append(f'<li>{m}</li>')
        people_html = f"""
            <div class="detail-section">
                <h2>Key People</h2>
                <ul>{''.join(items)}</ul>
            </div>
        """

    # Partnerships section
    partnerships_html = ""
    if partnerships:
        items = ''.join(f'<li>{p}</li>' for p in partnerships)
        partnerships_html = f"""
            <div class="detail-section">
                <h2>Partnerships</h2>
                <ul>{items}</ul>
            </div>
        """

    # UNICEF relevance section
    unicef_html = ""
    if unicef_relevance:
        unicef_html = f"""
            <div class="detail-section" style="background: #fff9db; border-color: #ffd43b;">
                <h2>🦄 UNICEF Relevance</h2>
                <p>{unicef_relevance}</p>
            </div>
        """

    # Engagement status badge - only show if not "none"
    status_colors = {
        'contacted': '#fab005',
        'in_discussion': '#15aabf',
        'active_partner': '#40c057'
    }
    status_badge = ''
    if engagement_status and engagement_status != 'none':
        status_color = status_colors.get(engagement_status, '#868e96')
        status_badge = f'<span style="background: {status_color}; color: white; padding: 0.2rem 0.5rem; border-radius: 4px; font-size: 0.8rem;">{engagement_status}</span>'

    # Convert country codes to names
    country_names = country_codes_to_names(actor_countries)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{name} - UNICEF WCARO NLP</title>
    <link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>🌍</text></svg>">
    <style>{get_css()}</style>
</head>
<body>
    <header>
        <div>
            <h1><a href="../index.html">UNICEF WCARO NLP Landscape</a></h1>
            <div class="subtitle">West and Central Africa Language Technology</div>
        </div>
        <div class="updated">Last updated: {datetime.now().strftime("%Y-%m-%d")}</div>
    </header>

    <div class="disclaimer">
        Work in progress. Some data may contain inaccuracies.
        <a href="https://github.com/translatorswb/wca-nlp-landscape" target="_blank">Contribute on GitHub</a>
    </div>

    <div class="lang-detail-container">
        <div class="breadcrumb">
            <a href="../index.html">Home</a> &gt; Actors &gt; {name}
        </div>

        <div class="lang-detail-header">
            <h1>{name}</h1>
            <div class="actor-meta" style="margin-top: 0.5rem;">
                <span class="actor-type">{actor_type_display}</span>
                {f'<span class="actor-maturity">{maturity}</span>' if maturity else ''}
                {status_badge}
            </div>
        </div>

        <div class="detail-section">
            <h2>Organization Information</h2>
            <div class="info-grid">
                <div class="info-item"><label>Type</label><span class="value">{actor_type_display}</span></div>
                <div class="info-item"><label>Founded</label><span class="value">{founded or '—'}</span></div>
                <div class="info-item"><label>Size</label><span class="value">{organization_size or '—'}</span></div>
                <div class="info-item"><label>Maturity</label><span class="value">{maturity or '—'}</span></div>
                <div class="info-item"><label>Location</label><span class="value">{location or '—'}</span></div>
                <div class="info-item"><label>Funding</label><span class="value">{funding or '—'}</span></div>
                <div class="info-item"><label>Website</label><span class="value">{website_html}</span></div>
                <div class="info-item"><label>GitHub</label><span class="value">{github_html}</span></div>
                <div class="info-item"><label>HuggingFace</label><span class="value">{huggingface_html}</span></div>
                <div class="info-item" style="grid-column: 1 / -1;"><label>Contact</label><span class="value">{contact_html}</span></div>
            </div>
        </div>

        <div class="detail-section">
            <h2>Coverage</h2>
            <div class="info-grid">
                <div class="info-item" style="grid-column: 1 / -1;"><label>Countries</label><span class="value">{', '.join(country_names) if country_names else '—'}</span></div>
                <div class="info-item" style="grid-column: 1 / -1;"><label>Languages</label><span class="value">{', '.join(str(l) for l in languages) if languages else '—'}</span></div>
            </div>
        </div>

        {f'<div class="detail-section"><h2>Description</h2><p>{description}</p></div>' if description else ''}
        {unicef_html}
        {people_html}
        {projects_html}
        {publications_html}
        {partnerships_html}
        {f'<div class="detail-section"><h2>Notes</h2><p>{notes}</p></div>' if notes else ''}

        <div style="margin-top: 2rem; font-size: 0.85rem; color: var(--text-muted);">
            Last updated: {last_updated or '—'}
        </div>
    </div>

    <footer>
        Generated: {datetime.now().strftime("%Y-%m-%d %H:%M")} | CLEAR Global for UNICEF WCARO
    </footer>
</body>
</html>
"""


def generate_main_html(languages, actors, wca_languages):
    """Generate the main index.html page."""

    focus_tab = generate_focus_languages_tab(languages, actors)
    all_tab = generate_all_languages_tab(wca_languages, languages)
    actors_tab = generate_actors_tab(actors)
    countries_tab = generate_countries_tab(wca_languages)

    total_focus = len(languages)
    total_wca = len(wca_languages)
    total_actors = len([k for k in actors.keys() if k != 'actor-template'])
    total_countries = 23  # WCA countries

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>UNICEF WCARO NLP Landscape</title>
    <link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>🌍</text></svg>">
    <style>{get_css()}</style>
</head>
<body>
    <header>
        <div>
            <h1>UNICEF WCARO NLP Landscape</h1>
            <div class="subtitle">West and Central Africa Language Technology</div>
        </div>
        <div class="updated">Last updated: {datetime.now().strftime("%Y-%m-%d")}</div>
    </header>

    <div class="disclaimer">
        Work in progress. Some data may contain inaccuracies.
        <a href="https://github.com/translatorswb/wca-nlp-landscape" target="_blank">Contribute on GitHub</a>
    </div>

    <div class="tabs">
        <button class="tab active" data-tab="focus">Focus Languages ({total_focus})</button>
        <button class="tab" data-tab="all">All Languages ({total_wca})</button>
        <button class="tab" data-tab="countries">Countries ({total_countries})</button>
        <button class="tab" data-tab="actors">Actors ({total_actors})</button>
    </div>

    <div id="focus" class="tab-content active">
        {focus_tab}
    </div>

    <div id="all" class="tab-content">
        {all_tab}
    </div>

    <div id="countries" class="tab-content">
        {countries_tab}
    </div>

    <div id="actors" class="tab-content">
        {actors_tab}
    </div>

    <footer>
        Generated: {datetime.now().strftime("%Y-%m-%d %H:%M")} | CLEAR Global for UNICEF WCARO
    </footer>

    <script>
        // Tab switching
        document.querySelectorAll('.tab').forEach(tab => {{
            tab.addEventListener('click', () => {{
                document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
                document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
                tab.classList.add('active');
                document.getElementById(tab.dataset.tab).classList.add('active');
            }});
        }});

        // Search
        const searchInput = document.getElementById('langSearch');
        if (searchInput) {{
            searchInput.addEventListener('input', (e) => {{
                const query = e.target.value.toLowerCase();
                document.querySelectorAll('#allLangsTable tbody tr').forEach(row => {{
                    const match = (row.dataset.name || '').includes(query) ||
                                  (row.dataset.iso || '').includes(query) ||
                                  (row.dataset.countries || '').includes(query);
                    row.style.display = match ? '' : 'none';
                }});
            }});
        }}

        // Sorting
        function sortTable(sortKey) {{
            const table = document.getElementById('allLangsTable');
            if (!table) return;

            const tbody = table.querySelector('tbody');
            const rows = Array.from(tbody.querySelectorAll('tr'));
            const th = table.querySelector(`th[data-sort="${{sortKey}}"]`);
            const isAsc = th.classList.contains('sorted-asc');

            // Remove sort classes from all headers
            table.querySelectorAll('th').forEach(h => {{
                h.classList.remove('sorted-asc', 'sorted-desc');
            }});

            function getValue(row, key) {{
                if (key === 'focus') return parseInt(row.dataset.focus) || 0;
                if (key === 'name') return row.dataset.name || '';
                if (key === 'iso') return row.dataset.iso || '';
                if (key === 'pop') return parseInt(row.dataset.pop) || 0;
                if (key === 'status') return row.cells[5].textContent || '';
                return '';
            }}

            rows.sort((a, b) => {{
                let aVal = getValue(a, sortKey);
                let bVal = getValue(b, sortKey);
                let cmp = 0;
                if (typeof aVal === 'number') {{
                    cmp = isAsc ? aVal - bVal : bVal - aVal;
                }} else {{
                    cmp = isAsc ? aVal.localeCompare(bVal) : bVal.localeCompare(aVal);
                }}
                // Secondary sort by population if equal
                if (cmp === 0 && sortKey !== 'pop') {{
                    cmp = (parseInt(b.dataset.pop) || 0) - (parseInt(a.dataset.pop) || 0);
                }}
                return cmp;
            }});

            th.classList.add(isAsc ? 'sorted-desc' : 'sorted-asc');
            rows.forEach(row => tbody.appendChild(row));
        }}

        // Add click handlers to sortable headers
        document.querySelectorAll('.all-langs-table th.sortable').forEach(th => {{
            th.addEventListener('click', () => sortTable(th.dataset.sort));
        }});

        // Initial sort by population
        sortTable('pop');
    </script>
</body>
</html>
"""


def main():
    print("=" * 60)
    print("Generating HTML report...")
    print("=" * 60)

    # Load data
    languages = load_all_languages()
    actors = load_all_actors()
    wca_languages = load_wca_languages()

    print(f"\nLoaded {len(languages)} focus languages")
    print(f"Loaded {len(wca_languages)} WCA languages")
    print(f"Loaded {len(actors)} actors")

    # Create output directories
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUTPUT_DIR / "lang").mkdir(parents=True, exist_ok=True)
    (OUTPUT_DIR / "actor").mkdir(parents=True, exist_ok=True)

    # Generate main index.html
    main_html = generate_main_html(languages, actors, wca_languages)
    index_path = OUTPUT_DIR / "index.html"
    with open(index_path, 'w') as f:
        f.write(main_html)
    print(f"\nGenerated: {index_path}")

    # Generate language detail pages
    for iso_code, lang_data in languages.items():
        lang_html = generate_language_detail_page(iso_code, lang_data, actors)
        lang_path = OUTPUT_DIR / "lang" / f"{iso_code}.html"
        with open(lang_path, 'w') as f:
            f.write(lang_html)
        print(f"Generated: {lang_path}")

    # Generate actor detail pages
    for actor_key, actor_data in actors.items():
        actor_html = generate_actor_detail_page(actor_key, actor_data)
        actor_id = actor_data.get('id', actor_key)
        actor_path = OUTPUT_DIR / "actor" / f"{actor_id}.html"
        with open(actor_path, 'w') as f:
            f.write(actor_html)
        print(f"Generated: {actor_path}")

    print(f"\nOpen in browser: file://{index_path.absolute()}")
    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()
