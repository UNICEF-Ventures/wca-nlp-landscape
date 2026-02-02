"""CSS styles for the generated HTML."""


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

        .lang-tags {
            display: flex;
            flex-wrap: wrap;
            gap: 0.25rem;
            margin-top: 0.4rem;
        }

        .lang-tag {
            background: #e7f5ff;
            color: #1971c2;
            padding: 0.1rem 0.45rem;
            border-radius: 3px;
            font-size: 0.75rem;
            text-decoration: none;
            white-space: nowrap;
        }

        a.lang-tag:hover {
            background: #d0ebff;
            text-decoration: none;
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

        .card-search, .all-langs-search {
            width: 100%;
            max-width: 400px;
            padding: 0.5rem 1rem;
            border: 1px solid var(--border);
            border-radius: 4px;
            font-size: 0.9rem;
            margin-bottom: 1rem;
        }

        .card-search:focus, .all-langs-search:focus {
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
            padding: 0.2rem 0.5rem;
            border-radius: 4px;
            font-size: 0.8rem;
            background: #40c057;
            color: white;
        }

        .actor-maturity.emerging {
            background: #fff9db;
            color: #e67700;
        }

        .actor-maturity.early {
            background: #fff3bf;
            color: #e67700;
        }

        /* Openness indicators */
        .openness-open {
            background: #d3f9d8;
            color: #2b8a3e;
            padding: 0.15rem 0.5rem;
            border-radius: 4px;
            font-size: 0.9rem;
        }

        .openness-partial {
            background: #fff3bf;
            color: #e67700;
            padding: 0.15rem 0.5rem;
            border-radius: 4px;
            font-size: 0.9rem;
        }

        .openness-closed {
            background: #ffe3e3;
            color: #c92a2a;
            padding: 0.15rem 0.5rem;
            border-radius: 4px;
            font-size: 0.9rem;
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

        /* Benchmark tables */
        .benchmark-table { margin-bottom: 1.5rem; }
        .benchmark-table th.num { text-align: right; }

        .detail-section h3 {
            font-size: 1.05rem;
            color: var(--text);
            margin: 1.25rem 0 0.5rem 0;
        }

        .detail-section h3:first-child { margin-top: 0; }
    """
