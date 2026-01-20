#!/usr/bin/env python3
"""
Main script to populate Research/ directory with language and model data.

Uses the African Language Grid data as the primary source for language information.
Now uses a language-first structure (Research/Languages/{iso}/) instead of
country-first (Research/Countries/{country}/{lang}/).

Usage:
    python scripts/populate_research.py              # Process all focus languages
    python scripts/populate_research.py --lang hau   # Process single language
    python scripts/populate_research.py --force      # Force re-fetch HuggingFace data
    python scripts/populate_research.py --generate-wca-list  # Generate WCA languages list only
"""

import argparse
import json
import sys
from pathlib import Path

import yaml

# Add parent directory to path for imports
SCRIPT_DIR = Path(__file__).parent
PROJECT_DIR = SCRIPT_DIR.parent
sys.path.insert(0, str(SCRIPT_DIR))

from fetch_huggingface import fetch_models_for_language, fetch_datasets_for_language
from fetch_wikipedia import fetch_language_info
from fetch_common_voice import get_common_voice_stats

# Paths
RESEARCH_DIR = PROJECT_DIR / "Research"
LANGUAGES_DIR = RESEARCH_DIR / "Languages"
SOURCE_DATA_DIR = PROJECT_DIR / "Source data"
CACHE_DIR = PROJECT_DIR / "cache"
FOCUSED_LANGUAGES_PATH = RESEARCH_DIR / "focused_languages.yaml"

# African Language Grid data paths
AFRICAN_GRID_DIR = SOURCE_DATA_DIR / "African-language-grid"
ALL_AFRICA_PATH = AFRICAN_GRID_DIR / "all_africa.yaml"
COUNTRY_GRID_PATH = AFRICAN_GRID_DIR / "country_grid.yaml"
COLUMN_SOURCES_PATH = AFRICAN_GRID_DIR / "column_sources.yaml"

# Other reference data paths
CV_DATA_PATH = SOURCE_DATA_DIR / "cv-corpus-24.0-2025-12-05.json"

# WCA Countries mapping (name -> ISO 3166-1 alpha-2)
WCA_COUNTRIES = {
    'Benin': 'BJ',
    'Burkina Faso': 'BF',
    'Cameroon': 'CM',
    'Central African Republic': 'CF',
    'Chad': 'TD',
    'Republic of the Congo': 'CG',
    'Congo': 'CG',  # Alternative name
    'Côte d\'Ivoire': 'CI',
    'Cote d\'Ivoire': 'CI',  # Without accent
    'Ivory Coast': 'CI',  # Alternative name
    'Democratic Republic of the Congo': 'CD',
    'Democratic Republic of Congo': 'CD',  # Alternative name (without "the")
    'DR Congo': 'CD',  # Alternative name
    'DRC': 'CD',  # Alternative name
    'Equatorial Guinea': 'GQ',
    'Gabon': 'GA',
    'The Gambia': 'GM',
    'Gambia': 'GM',  # Alternative name
    'Ghana': 'GH',
    'Guinea': 'GN',
    'Guinea-Bissau': 'GW',
    'Liberia': 'LR',
    'Mali': 'ML',
    'Mauritania': 'MR',
    'Niger': 'NE',
    'Nigeria': 'NG',
    'Sao Tome and Principe': 'ST',
    'São Tomé and Príncipe': 'ST',  # Alternative name
    'Senegal': 'SN',
    'Sierra Leone': 'SL',
    'Togo': 'TG',
}

# Reverse mapping
WCA_ISO_TO_NAME = {v: k for k, v in WCA_COUNTRIES.items()}


def load_focused_languages():
    """Load the focused languages configuration (list of ISO codes)."""
    if not FOCUSED_LANGUAGES_PATH.exists():
        print(f"Warning: {FOCUSED_LANGUAGES_PATH} not found")
        return []

    with open(FOCUSED_LANGUAGES_PATH, 'r') as f:
        data = yaml.safe_load(f)

    # Handle both old format (dict with countries) and new format (list of ISO codes)
    if isinstance(data, list):
        return data
    elif isinstance(data, dict) and 'countries' in data:
        # Old format - extract ISO codes
        iso_codes = []
        for country_data in data.get('countries', {}).values():
            for lang in country_data.get('languages', []):
                iso = lang.get('iso_639_3')
                if iso:
                    iso_codes.append(iso)
        return iso_codes
    return []


def load_african_grid_data():
    """Load African Language Grid data from YAML files."""
    data = {
        'languages': [],
        'by_iso': {},
        'by_country': {},
        'column_sources': {},
    }

    if ALL_AFRICA_PATH.exists():
        with open(ALL_AFRICA_PATH, 'r', encoding='utf-8') as f:
            all_africa = yaml.safe_load(f)
            data['languages'] = all_africa.get('languages', [])
            # Create lookup by ISO code
            for lang in data['languages']:
                iso = lang.get('iso_639_3')
                if isinstance(iso, dict):
                    iso = iso.get('text')
                if iso:
                    data['by_iso'][iso] = lang
    else:
        print(f"Warning: African Grid data not found at {ALL_AFRICA_PATH}")
        print("Run: python scripts/convert_african_grid.py")

    if COUNTRY_GRID_PATH.exists():
        with open(COUNTRY_GRID_PATH, 'r', encoding='utf-8') as f:
            country_grid = yaml.safe_load(f)
            data['by_country'] = country_grid.get('countries', {})
    else:
        print(f"Warning: Country grid not found at {COUNTRY_GRID_PATH}")

    if COLUMN_SOURCES_PATH.exists():
        with open(COLUMN_SOURCES_PATH, 'r', encoding='utf-8') as f:
            col_sources = yaml.safe_load(f)
            data['column_sources'] = col_sources.get('columns', {})

    return data


def extract_text_and_url(value):
    """Extract text and URL from a value that may be a dict with text/url or just a string."""
    if isinstance(value, dict):
        return value.get('text', ''), value.get('url', '')
    return str(value) if value else '', ''


def get_language_info_from_grid(grid_data, iso_639_3):
    """Get comprehensive language info from African Grid by ISO code."""
    lang = grid_data['by_iso'].get(iso_639_3)
    if not lang:
        return None

    # Extract values, handling text/url dicts
    name, _ = extract_text_and_url(lang.get('name'))
    iso3, iso3_url = extract_text_and_url(lang.get('iso_639_3'))
    glottocode, glotto_url = extract_text_and_url(lang.get('glottocode'))
    wiki_text, wiki_url = extract_text_and_url(lang.get('wikipedia'))

    # Parse alternate names
    altnames_raw = lang.get('alternate_names', '')
    altnames = [n.strip() for n in altnames_raw.split(',') if n.strip()] if altnames_raw else []

    # Parse countries
    countries_str = lang.get('countries', '')
    countries = [c.strip() for c in countries_str.split(',') if c.strip()] if countries_str else []

    # Population
    population = lang.get('population')
    if isinstance(population, dict):
        population = population.get('text')
    population_order = lang.get('population_order', '')

    # Resource links (extract URLs where available)
    resource_links = {}

    resource_fields = [
        ('lanfrica', 'Lanfrica'),
        ('olac', 'OLAC'),
        ('grambank', 'Grambank'),
        ('wals', 'WALS'),
        ('elar', 'ELAR'),
        ('elp', 'Endangered Languages Project'),
        ('cldr', 'CLDR'),
        ('africarxiv', 'AfricArXiv'),
        ('webonary', 'Webonary'),
    ]

    for field_key, field_name in resource_fields:
        field_val = lang.get(field_key)
        if field_val:
            text, url = extract_text_and_url(field_val)
            if url:
                resource_links[field_name] = url
            elif text and text.startswith('http'):
                resource_links[field_name] = text

    # NLP/Tech resources (boolean indicators or URLs)
    tech_resources = {}
    tech_fields = [
        ('afrolid', 'AfroLID'),
        ('google_translate', 'Google Translate'),
        ('mbert', 'mBERT'),
        ('nllb_200', 'NLLB-200'),
        ('mbart_50', 'mBart-50'),
        ('m2m_100', 'M2M-100'),
        ('common_voice', 'Mozilla Common Voice'),
        ('madlad_400_docs', 'MADLAD-400 Docs'),
        ('madlad_400_sentences', 'MADLAD-400 Sentences'),
        ('aya_101', 'Aya-101'),
        ('fineweb2', 'Fineweb2'),
        ('fleurs', 'FLEURS'),
        ('afrihate', 'AfriHate'),
        ('cmu_wilderness', 'CMU Wilderness'),
        ('mafand', 'MAFAND'),
        ('naija_voices', 'NaijaVoices'),
    ]

    for field_key, field_name in tech_fields:
        field_val = lang.get(field_key)
        if field_val:
            text, url = extract_text_and_url(field_val)
            # Check if it's a checkmark, presence indicator, or actual data
            if text in ('✅', '√', '🆔', '🌻', '🤬', '🌳', '🇶🇦'):
                tech_resources[field_name] = True
            elif url:
                tech_resources[field_name] = url
            elif text:
                tech_resources[field_name] = text

    return {
        'name': name,
        'name_french': lang.get('name_french', ''),
        'iso_639_3': iso3,
        'iso_639_1': lang.get('iso_639_1', ''),
        'glottocode': glottocode,
        'glottocode_url': glotto_url,
        'altnames': altnames[:15],  # Limit to 15
        'countries': countries,
        'population': population,
        'population_order': population_order,
        'endangerment': lang.get('endangerment', ''),
        'official_status': lang.get('official_status', ''),
        'wikipedia_url': wiki_url if wiki_url else None,
        'scriptsource_url': iso3_url if iso3_url else None,
        'resource_page': extract_text_and_url(lang.get('resource_page'))[1] or None,
        'acalan_commission': extract_text_and_url(lang.get('acalan_commission'))[1] or None,
        'resource_links': resource_links if resource_links else None,
        'tech_resources': tech_resources if tech_resources else None,
        'note': lang.get('note', ''),
    }


def load_common_voice_data():
    """Load Common Voice dataset statistics."""
    if not CV_DATA_PATH.exists():
        print(f"Warning: Common Voice data not found at {CV_DATA_PATH}")
        return {}

    with open(CV_DATA_PATH, 'r') as f:
        data = json.load(f)
    return data.get('locales', {})


def ensure_directory(path):
    """Create directory if it doesn't exist."""
    path.mkdir(parents=True, exist_ok=True)


def save_yaml(data, path):
    """Save data to YAML file."""
    # Clean None values for cleaner output
    def clean_dict(d):
        if isinstance(d, dict):
            return {k: clean_dict(v) for k, v in d.items() if v is not None and v != '' and v != []}
        elif isinstance(d, list):
            return [clean_dict(i) for i in d if i is not None]
        return d

    cleaned = clean_dict(data)
    with open(path, 'w', encoding='utf-8') as f:
        yaml.dump(cleaned, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
    print(f"  Saved: {path}")


def save_markdown(content, path):
    """Save content to markdown file."""
    with open(path, 'w') as f:
        f.write(content)
    print(f"  Saved: {path}")


def process_language(iso_639_3, cv_data, grid_data, force_fetch=False):
    """Process a single language and create output files in Research/Languages/{iso}/.

    Args:
        iso_639_3: ISO 639-3 language code
        cv_data: Common Voice data dict
        grid_data: African Language Grid data
        force_fetch: If True, re-fetch HuggingFace data even if files exist
    """

    # Get language info from African Grid first
    grid_info = get_language_info_from_grid(grid_data, iso_639_3)

    if not grid_info:
        print(f"  Warning: Language {iso_639_3} not found in African Grid data")
        return False

    lang_name = grid_info.get('name', iso_639_3)
    iso_639_1 = grid_info.get('iso_639_1')

    # Create language directory using ISO 639-3 code only
    lang_dir = LANGUAGES_DIR / iso_639_3
    ensure_directory(lang_dir)

    print(f"\n  Processing language: {lang_name} ({iso_639_3})")

    # 1. Fetch Wikipedia info for additional data
    print("    Fetching Wikipedia info...")
    wiki_info = fetch_language_info(lang_name)

    # Build language_info with separate sections
    language_info = {
        # Core identification
        'name': lang_name,
        'iso_639_3': iso_639_3,
        'iso_639_1': iso_639_1 or (grid_info.get('iso_639_1') if grid_info else None),
        'name_french': grid_info.get('name_french') if grid_info else None,
        'altnames': grid_info.get('altnames') if grid_info else [],

        # Geographic and demographic info from African Grid
        'countries': grid_info.get('countries') if grid_info else [],
        'population': grid_info.get('population') if grid_info else None,
        'population_order': grid_info.get('population_order') if grid_info else None,
        'endangerment': grid_info.get('endangerment') if grid_info else None,
        'official_status': grid_info.get('official_status') if grid_info else None,

        # Glottolog reference
        'glottocode': grid_info.get('glottocode') if grid_info else (wiki_info.get('glottolog') if wiki_info else None),
        'glottocode_url': grid_info.get('glottocode_url') if grid_info else None,

        # Wikipedia info (separate section)
        'wikipedia': {
            'url': grid_info.get('wikipedia_url') if grid_info else (wiki_info.get('wiki_url') if wiki_info else None),
            'family': wiki_info.get('family') if wiki_info else None,
            'speakers_l1': wiki_info.get('speakers_l1') if wiki_info else None,
            'speakers_l2': wiki_info.get('speakers_l2') if wiki_info else None,
            'writing_system': wiki_info.get('writing_system') if wiki_info else None,
        } if wiki_info or (grid_info and grid_info.get('wikipedia_url')) else None,

        # External resource links
        'scriptsource_url': grid_info.get('scriptsource_url') if grid_info else None,
        'resource_page': grid_info.get('resource_page') if grid_info else None,
        'acalan_commission': grid_info.get('acalan_commission') if grid_info else None,
        'resource_links': grid_info.get('resource_links') if grid_info else None,

        # NLP/Tech resources from African Grid
        'tech_resources': grid_info.get('tech_resources') if grid_info else None,
    }
    save_yaml(language_info, lang_dir / "info.yaml")

    # 2. Fetch models from HuggingFace
    models_path = lang_dir / "models.yaml"
    if models_path.exists() and not force_fetch:
        print("    Skipping HuggingFace models (already exists, use --force to re-fetch)")
    else:
        print("    Fetching HuggingFace models...")

        # ASR models
        asr_result = fetch_models_for_language(iso_639_1, iso_639_3, 'automatic-speech-recognition')

        # TTS models
        tts_result = fetch_models_for_language(iso_639_1, iso_639_3, 'text-to-speech')

        # Translation models
        mt_result = fetch_models_for_language(iso_639_1, iso_639_3, 'translation')

        # LLM models (text-generation)
        llm_result = fetch_models_for_language(iso_639_1, iso_639_3, 'text-generation')

        models_data = {
            'asr': {
                'items': asr_result['items'],
                'total_count': asr_result['total_count'],
                'counts_by_code': asr_result.get('counts_by_code', {}),
            },
            'tts': {
                'items': tts_result['items'],
                'total_count': tts_result['total_count'],
                'counts_by_code': tts_result.get('counts_by_code', {}),
            },
            'translation': {
                'items': mt_result['items'],
                'total_count': mt_result['total_count'],
                'counts_by_code': mt_result.get('counts_by_code', {}),
            },
            'llm': {
                'items': llm_result['items'],
                'total_count': llm_result['total_count'],
                'counts_by_code': llm_result.get('counts_by_code', {}),
            },
        }

        save_yaml(models_data, models_path)

    # 3. Fetch datasets from HuggingFace
    datasets_path = lang_dir / "datasets.yaml"
    if datasets_path.exists() and not force_fetch:
        print("    Skipping HuggingFace datasets (already exists, use --force to re-fetch)")
    else:
        print("    Fetching HuggingFace datasets...")

        asr_result = fetch_datasets_for_language(iso_639_1, iso_639_3, 'automatic-speech-recognition')
        tts_result = fetch_datasets_for_language(iso_639_1, iso_639_3, 'text-to-speech')

        datasets_data = {
            'asr': {
                'items': asr_result['items'],
                'total_count': asr_result['total_count'],
                'counts_by_code': asr_result.get('counts_by_code', {}),
            },
            'tts': {
                'items': tts_result['items'],
                'total_count': tts_result['total_count'],
                'counts_by_code': tts_result.get('counts_by_code', {}),
            },
        }

        save_yaml(datasets_data, datasets_path)

    # 4. Get Common Voice stats
    print("    Checking Common Voice...")
    cv_stats = get_common_voice_stats(iso_639_3, iso_639_1, cv_data)

    benchmarks_data = {
        'common_voice': cv_stats,
        'flores': None,  # TODO: Add FLORES lookup
        'fleurs': None,  # TODO: Add FLEURS lookup
    }
    save_yaml(benchmarks_data, lang_dir / "benchmarks.yaml")

    # 5. Create notes.md stub
    notes_path = lang_dir / "notes.md"
    if not notes_path.exists():
        countries_str = ', '.join(grid_info.get('countries', [])[:5]) if grid_info else ''
        notes_content = f"""# {lang_name}

ISO 639-3: {iso_639_3}
Countries: {countries_str}

## Observations

(Add manual observations here)

## Gaps

(Note any gaps in available resources)

## Recommendations

(Add recommendations for UNICEF)
"""
        save_markdown(notes_content, notes_path)

    return True


def generate_wca_languages_data(grid_data):
    """Generate a comprehensive list of all WCA languages for the All Languages tab.

    Iterates through all languages in all_africa.yaml and includes any language
    that is spoken in at least one WCA country.
    """
    wca_langs = []

    # Iterate through all languages directly from all_africa.yaml
    for lang in grid_data['languages']:
        # Get language name and URL
        lang_name, lang_url = extract_text_and_url(lang.get('name'))
        if not lang_name:
            continue

        # Get ISO code
        iso_raw = lang.get('iso_639_3')
        iso_code, _ = extract_text_and_url(iso_raw)
        if not iso_code:
            continue

        # Parse countries from the language's countries field
        countries_str = lang.get('countries', '')
        all_countries = [c.strip() for c in countries_str.split(',') if c.strip()]

        # Check which are WCA countries
        wca_countries = [c for c in all_countries if c in WCA_COUNTRIES]

        # Only include if spoken in at least one WCA country
        if not wca_countries:
            continue

        # Population
        pop = lang.get('population')
        if isinstance(pop, dict):
            pop = pop.get('text')

        # Get Wikipedia URL if available
        _, wiki_url = extract_text_and_url(lang.get('wikipedia'))
        url = wiki_url or lang_url

        wca_langs.append({
            'name': lang_name,
            'iso_639_3': iso_code,
            'countries': all_countries,  # All countries where language is spoken
            'wca_countries': wca_countries,  # Only WCA countries (for filtering/highlighting)
            'population': pop,
            'population_order': lang.get('population_order', ''),
            'endangerment': lang.get('endangerment', ''),
            'url': url,
        })

    # Sort by name
    wca_langs.sort(key=lambda x: x['name'])
    return wca_langs


def main():
    parser = argparse.ArgumentParser(description='Populate Research/ with language and model data')
    parser.add_argument('--lang', help='Process only this language ISO code (e.g., hau)')
    parser.add_argument('--generate-wca-list', action='store_true',
                        help='Generate WCA languages list only (no HuggingFace fetching)')
    parser.add_argument('--force', action='store_true',
                        help='Force re-fetch HuggingFace data even if models.yaml/datasets.yaml exist')
    args = parser.parse_args()

    print("=" * 60)
    print("UNICEF WCARO NLP Research - Data Population Script")
    print("=" * 60)

    # Load African Grid data
    grid_data = load_african_grid_data()
    print(f"\nLoaded {len(grid_data['languages'])} languages from African Grid")
    print(f"Loaded {len(grid_data['by_country'])} countries from country grid")

    # Generate WCA languages list
    if args.generate_wca_list:
        print("\nGenerating WCA languages list...")
        wca_langs = generate_wca_languages_data(grid_data)
        output_path = RESEARCH_DIR / "wca_all_languages.yaml"
        save_yaml({'languages': wca_langs, 'total': len(wca_langs)}, output_path)
        print(f"\nGenerated {len(wca_langs)} WCA languages")
        return

    # Load other data
    focus_languages = load_focused_languages()
    cv_data = load_common_voice_data()

    print(f"Loaded {len(cv_data)} Common Voice locales")
    print(f"Found {len(focus_languages)} focus languages")

    # Ensure Languages directory exists
    ensure_directory(LANGUAGES_DIR)

    # Filter by language if specified
    if args.lang:
        if args.lang in focus_languages or args.lang in grid_data['by_iso']:
            languages_to_process = [args.lang]
        else:
            print(f"Error: Language '{args.lang}' not found")
            sys.exit(1)
    else:
        languages_to_process = focus_languages

    # Process each language
    processed = 0
    for iso_code in languages_to_process:
        if process_language(iso_code, cv_data, grid_data, force_fetch=args.force):
            processed += 1

    # Also generate/update the WCA languages list
    print("\nGenerating WCA languages list...")
    wca_langs = generate_wca_languages_data(grid_data)
    output_path = RESEARCH_DIR / "wca_all_languages.yaml"
    save_yaml({'languages': wca_langs, 'total': len(wca_langs)}, output_path)
    print(f"Generated {len(wca_langs)} WCA languages")

    print("\n" + "=" * 60)
    print(f"Done! Processed {processed} languages.")
    print("=" * 60)


if __name__ == "__main__":
    main()
