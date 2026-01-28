"""Formatting utilities and HuggingFace rendering helpers."""

import re

from .constants import COUNTRY_NAMES


# --- General utilities ---

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
    return actor_type.replace('_', ' ').title()


def format_huggingface_link(url):
    """Extract HuggingFace handle and return as link."""
    if not url:
        return '—'
    handle = url.rstrip('/').split('/')[-1]
    return f'<a href="{url}" target="_blank">{handle}</a>'


# --- HuggingFace rendering ---

def get_huggingface_search_url(iso_639_1, iso_639_3, pipeline_tag):
    """Generate HuggingFace search URL for a language and task."""
    code = iso_639_1 if iso_639_1 else iso_639_3
    if not code:
        return None
    return f"https://huggingface.co/models?pipeline_tag={pipeline_tag}&language={code}&sort=trending"


def generate_models_table(models_data, task_name, limit=15, iso_639_1=None, iso_639_3=None, pipeline_tag=None):
    """Generate HTML table for models.

    Args:
        models_data: Either a list of models (old format) or dict with 'items', 'total_count', and 'counts_by_code' (new format)
    """
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


# --- Benchmark rendering ---

TASK_LABELS = {
    'asr': 'ASR (Speech-to-Text)',
    'tts': 'TTS (Text-to-Speech)',
    'mt': 'MT (Machine Translation)',
    'llm': 'LLM (Large Language Models)',
}


def generate_benchmarks_section(evaluations):
    """Generate the full Benchmarks HTML section from merged evaluation data.

    Args:
        evaluations: dict like {'asr': [entries], 'translation': [entries], ...}

    Returns:
        HTML string for the benchmarks section, or empty string if no data.
    """
    if not evaluations:
        return ""

    subsections = []
    for task in ['asr', 'tts', 'translation', 'llm']:
        entries = evaluations.get(task, [])
        if not entries:
            continue
        label = TASK_LABELS.get(task, task.upper())
        table_html = _render_benchmark_table(entries)
        if table_html:
            subsections.append(f"<h3>{label}</h3>\n{table_html}")

    # Also render any tasks not in the standard list
    for task, entries in evaluations.items():
        if task in TASK_LABELS or not entries:
            continue
        table_html = _render_benchmark_table(entries)
        if table_html:
            subsections.append(f"<h3>{task.upper()}</h3>\n{table_html}")

    if not subsections:
        return ""

    return f"""
        <div class="detail-section">
            <h2>Benchmarks</h2>
            {''.join(subsections)}
        </div>
    """


def _render_benchmark_table(entries):
    """Render a benchmark table for a single task.

    Each entry has model, model_url, and results (list of test_set results).
    Each result has test_set, source, source_url, and metrics (list of name/value).
    """
    # First pass: collect all unique metric names across all results
    metric_names = []
    seen_metrics = set()
    for entry in entries:
        for result in entry.get('results', []):
            for m in result.get('metrics', []):
                name = m.get('name', '')
                if name and name not in seen_metrics:
                    metric_names.append(name)
                    seen_metrics.add(name)

    # Build header
    metric_headers = ''.join(f'<th class="num">{name}</th>' for name in metric_names)
    header = f"<tr><th>Model</th><th>Test Set</th>{metric_headers}<th>Source</th></tr>"

    # Build rows: one row per (model, test_set)
    rows = []
    for entry in entries:
        model = entry.get('model', '')
        model_url = entry.get('model_url', '')
        model_html = f'<a href="{model_url}" target="_blank">{model}</a>' if model_url else model

        results = entry.get('results', [])
        if not results:
            # Model listed without evaluation results
            metric_cells = ''.join('<td class="num">—</td>' for _ in metric_names)
            rows.append(
                f"<tr>"
                f"<td>{model_html}</td>"
                f"<td>—</td>"
                f"{metric_cells}"
                f"<td>—</td>"
                f"</tr>"
            )
            continue

        for result in results:
            test_set = result.get('test_set', '')
            source = result.get('source', '')
            source_url = result.get('source_url', '')

            # Source column: "reported" links to source_url
            if source_url:
                source_html = f'<a href="{source_url}" target="_blank">{source}</a>'
            else:
                source_html = source

            # Build metric cells
            metrics_by_name = {m['name']: m['value'] for m in result.get('metrics', []) if 'name' in m}
            metric_cells = []
            for name in metric_names:
                val = metrics_by_name.get(name)
                if val is not None:
                    metric_cells.append(f'<td class="num">{val}</td>')
                else:
                    metric_cells.append('<td class="num">—</td>')

            rows.append(
                f"<tr>"
                f"<td>{model_html}</td>"
                f"<td>{test_set}</td>"
                f"{''.join(metric_cells)}"
                f"<td>{source_html}</td>"
                f"</tr>"
            )

    if not rows:
        return ""

    return f"""
        <table class="data-table benchmark-table">
            <thead>{header}</thead>
            <tbody>{''.join(rows)}</tbody>
        </table>
    """


TASK_SHORT_LABELS = {
    'asr': 'ASR',
    'tts': 'TTS',
    'translation': 'MT',
    'llm': 'LLM',
}


def generate_unbenchmarked_models_section(models):
    """Generate HTML section for unbenchmarked models.

    Args:
        models: list of dicts with model, model_url, task, and optional notes.

    Returns:
        HTML string, or empty string if no models.
    """
    if not models:
        return ""

    rows = []
    for entry in models:
        model = entry.get('model', '')
        model_url = entry.get('model_url', '')
        task = entry.get('task', '')
        notes = entry.get('notes', '')

        model_html = f'<a href="{model_url}" target="_blank">{model}</a>' if model_url else model
        task_label = TASK_SHORT_LABELS.get(task, task.upper())

        rows.append(
            f"<tr>"
            f"<td>{model_html}</td>"
            f"<td>{task_label}</td>"
            f"<td>{notes}</td>"
            f"</tr>"
        )

    return f"""
        <div class="detail-section">
            <h2>Noteworthy models without benchmark</h2>
            <table class="data-table benchmark-table">
                <thead><tr><th>Model</th><th>Task</th><th>Notes</th></tr></thead>
                <tbody>{''.join(rows)}</tbody>
            </table>
        </div>
    """
