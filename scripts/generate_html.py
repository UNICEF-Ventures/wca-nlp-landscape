#!/usr/bin/env python3
"""
Generate a browsable HTML website from Research/ data.

Now uses language-first structure (Research/Languages/{iso}/).

Usage:
    python scripts/generate_html.py

Output:
    output/index.html
    output/lang/{iso}.html
    output/actor/{id}.html
"""

from datetime import datetime

from htmlgen.constants import OUTPUT_DIR
from htmlgen.data import load_all_languages, load_all_actors, load_wca_languages, load_sources, load_focused_languages
from htmlgen.styles import get_css
from htmlgen.tabs import (
    generate_focus_languages_tab, generate_all_languages_tab,
    generate_countries_tab, generate_actors_tab, generate_sources_tab,
)
from htmlgen.pages import generate_language_detail_page, generate_actor_detail_page


def generate_main_html(languages, actors, wca_languages, sources, priority_isos, extended_isos):
    """Generate the main index.html page."""

    focus_tab = generate_focus_languages_tab(languages, actors, priority_isos, extended_isos)
    all_tab = generate_all_languages_tab(wca_languages, languages, priority_isos, extended_isos)
    actors_tab = generate_actors_tab(actors)
    countries_tab = generate_countries_tab(wca_languages)
    sources_tab = generate_sources_tab(sources)

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
        <button class="tab" data-tab="sources">Sources</button>
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

    <div id="sources" class="tab-content">
        {sources_tab}
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

        // All Languages table search
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

        // Focus Languages card search
        const focusSearch = document.getElementById('focusLangSearch');
        if (focusSearch) {{
            focusSearch.addEventListener('input', (e) => {{
                const query = e.target.value.toLowerCase();
                document.querySelectorAll('#focus .language-card').forEach(card => {{
                    const match = (card.dataset.search || '').includes(query);
                    card.style.display = match ? '' : 'none';
                }});
            }});
        }}

        // Actors card search
        const actorSearch = document.getElementById('actorSearch');
        if (actorSearch) {{
            actorSearch.addEventListener('input', (e) => {{
                const query = e.target.value.toLowerCase();
                document.querySelectorAll('#actors .actor-card').forEach(card => {{
                    const match = (card.dataset.search || '').includes(query);
                    card.style.display = match ? '' : 'none';
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
    sources = load_sources()
    focused = load_focused_languages()
    priority_isos = set(focused['priority'])
    extended_isos = set(focused['extended'])

    print(f"\nLoaded {len(languages)} focus languages ({len(priority_isos)} priority, {len(extended_isos)} extended)")
    print(f"Loaded {len(wca_languages)} WCA languages")
    print(f"Loaded {len(actors)} actors")
    included = sum(1 for s in sources if s.get('status') == 'included')
    print(f"Loaded {len(sources)} sources ({included} benchmark scores included)")

    # Create output directories
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUTPUT_DIR / "lang").mkdir(parents=True, exist_ok=True)
    (OUTPUT_DIR / "actor").mkdir(parents=True, exist_ok=True)

    # Generate main index.html
    main_html = generate_main_html(languages, actors, wca_languages, sources, priority_isos, extended_isos)
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
        actor_html = generate_actor_detail_page(actor_key, actor_data, languages)
        actor_id = actor_data.get('id', actor_key)
        actor_path = OUTPUT_DIR / "actor" / f"{actor_id}.html"
        with open(actor_path, 'w') as f:
            f.write(actor_html)
        print(f"Generated: {actor_path}")

    print(f"\nOpen in browser: file://{index_path.absolute()}")
    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()
