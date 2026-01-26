"""Full detail page generators (language and actor)."""

from datetime import datetime

from .constants import WCA_COUNTRIES
from .styles import get_css
from .utils import (
    markdown_to_html, get_actors_for_language, format_actor_type,
    format_huggingface_link, country_codes_to_names,
    get_model_count, generate_models_table, generate_datasets_table,
)


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
