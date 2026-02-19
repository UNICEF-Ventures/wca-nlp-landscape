"""Tab content generators for the main index page."""

import json
import re
from pathlib import Path

import yaml

from .constants import WCA_COUNTRIES, RESEARCH_DIR
from .utils import (
    get_actors_for_language, get_model_count, generate_models_table,
    format_actor_type, country_codes_to_names,
)


# Load LUDP configuration
def _load_ludp_config():
    """Load LUDP configuration from YAML file."""
    config_path = Path(__file__).parent.parent.parent / 'Source data' / 'ludp_config.yaml'
    with open(config_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

LUDP_CONFIG = _load_ludp_config()


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

    # Build search text for client-side filtering
    search_parts = [name, iso3]
    if iso1:
        search_parts.append(iso1)
    search_parts.extend(countries)
    search_parts.extend(altnames[:6])
    if family:
        search_parts.append(family)
    search_text = ' '.join(str(s) for s in search_parts).lower()

    return f"""
        <div class="language-card" id="lang-{iso_code}" data-search="{search_text}">
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
        <input type="text" class="card-search" id="focusLangSearch"
               placeholder="Search languages by name, ISO code, country...">
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
    # Load countries from LUDP config
    countries_from_config = LUDP_CONFIG.get('countries', [])

    # Build country data as JSON for JavaScript
    countries_data = []
    for country in countries_from_config:
        countries_data.append({
            'name': country['name'],
            'shareCode': country['share_code'],
            'urlName': country['url_name'],
            'level': country['admin_level']
        })
    countries_json = json.dumps(countries_data)

    # Build language data by country for the language lists
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
        f'<option value="{country["name"]}">{country["name"]}</option>'
        for country in countries_from_config
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
                    const urlCountry = countryData.urlName.replace(/\\+/g, '%20');
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
            'active_partner': '#023e8a'
        }
        status_badge = ''
        if engagement_status and engagement_status != 'none':
            status_color = status_colors.get(engagement_status, '#868e96')
            status_badge = f'<span style="background: {status_color}; color: white; padding: 0.2rem 0.5rem; border-radius: 4px; font-size: 0.8rem;">{engagement_status}</span>'

        # Convert country codes to names
        country_names = country_codes_to_names(actor_countries)
        actor_type_display = format_actor_type(actor_type)

        # Build search text for client-side filtering
        search_parts = [name, actor_type_display, location or '']
        search_parts.extend(country_names)
        search_parts.extend(str(l) for l in languages)
        if description:
            search_parts.append(description[:300])
        search_text = ' '.join(search_parts).lower()

        cards.append(f"""
            <div class="actor-card" data-search="{search_text}">
                <h3><a href="{detail_url}">{name}</a></h3>
                <div class="actor-meta">
                    <span class="actor-type">{actor_type_display}</span>
                    {f'<span class="actor-maturity {maturity}">{maturity}</span>' if maturity else ''}
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
        <input type="text" class="card-search" id="actorSearch"
               placeholder="Search actors by name, type, country, language...">
        <div class="actors-grid">
            {''.join(cards)}
        </div>
    """


def generate_sources_tab(sources):
    """Generate the Sources tab content."""
    data_sources = sources.get('data_sources', [])
    benchmark_sources = sources.get('benchmark_sources', [])

    # --- Section 1: Data Sources ---
    ds_rows = []
    for ds in data_sources:
        name = ds.get('name', '')
        url = ds.get('url', '')
        description = ds.get('description', '')
        ds_type = ds.get('type', '')

        name_html = f'<a href="{url}" target="_blank">{name}</a>' if url else name

        type_labels = {
            'reference': ('Reference', '#e3f2fd', '#1565c0'),
            'speech_data': ('Speech Data', '#fff3e0', '#e65100'),
            'model_hub': ('Model Hub', '#f3e5f5', '#7b1fa2'),
            'model_coverage': ('Model Coverage', '#e8f5e9', '#2e7d32'),
        }
        label, bg, color = type_labels.get(ds_type, (ds_type, '#f5f5f5', '#616161'))
        type_badge = f'<span style="background:{bg}; color:{color}; padding:0.15rem 0.5rem; border-radius:4px; font-size:0.8rem;">{label}</span>'

        ds_rows.append(f"""
            <tr>
                <td>{name_html}</td>
                <td>{type_badge}</td>
                <td>{description}</td>
            </tr>
        """)

    # --- Section 2: Benchmark Sources ---
    status_styles = {
        'included': ('INCLUDED', '#d4edda', '#155724'),
        'placeholder': ('PLACEHOLDER', '#fff3cd', '#856404'),
        'to_extract': ('TO EXTRACT', '#fff3cd', '#856404'),
        'noted': ('NOTED', '#e2e3e5', '#383d41'),
        'blocked': ('BLOCKED', '#f8d7da', '#721c24'),
    }

    bs_rows = []
    for bs in benchmark_sources:
        name = bs.get('name', '')
        url = bs.get('url', '')
        bs_type = bs.get('type', '')
        langs = bs.get('languages_covered', [])
        status = bs.get('status', '')
        description = bs.get('description', '')

        name_html = f'<a href="{url}" target="_blank">{name}</a>' if url else name

        # Status badge
        label, bg, color = status_styles.get(status, (status.upper(), '#e2e3e5', '#383d41'))
        status_badge = f'<span style="background:{bg}; color:{color}; padding:0.15rem 0.5rem; border-radius:4px; font-size:0.8rem; font-weight:500;">{label}</span>'

        # Languages
        langs_html = ', '.join(f'<span class="iso-code">{l}</span>' for l in langs) if langs else '<span style="color:#999;">—</span>'

        bs_rows.append(f"""
            <tr>
                <td>{name_html}</td>
                <td>{bs_type}</td>
                <td>{langs_html}</td>
                <td>{status_badge}</td>
                <td style="font-size:0.85rem;">{description}</td>
            </tr>
        """)

    # Count stats
    included_count = sum(1 for bs in benchmark_sources if bs.get('status') == 'included')
    total_count = len(benchmark_sources)

    return f"""
        <div class="sources-container">
            <h2>Data Sources</h2>
            <p style="color: var(--text-muted); margin-bottom: 1rem;">
                General data sources used to populate language profiles, actor information, and technology coverage.
            </p>
            <div class="table-scroll">
                <table class="all-langs-table">
                    <thead>
                        <tr>
                            <th>Source</th>
                            <th>Type</th>
                            <th>Description</th>
                        </tr>
                    </thead>
                    <tbody>
                        {''.join(ds_rows)}
                    </tbody>
                </table>
            </div>

            <h2 style="margin-top: 2.5rem;">Benchmark Sources</h2>
            <p style="color: var(--text-muted); margin-bottom: 1rem;">
                Benchmark and evaluation sources tracked for this study.
                <strong>{included_count}</strong> of {total_count} sources have scores extracted and included.
            </p>
            <div class="table-scroll">
                <table class="all-langs-table">
                    <thead>
                        <tr>
                            <th>Source</th>
                            <th>Type</th>
                            <th>Focus Languages</th>
                            <th>Status</th>
                            <th>Description</th>
                        </tr>
                    </thead>
                    <tbody>
                        {''.join(bs_rows)}
                    </tbody>
                </table>
            </div>
        </div>
    """
