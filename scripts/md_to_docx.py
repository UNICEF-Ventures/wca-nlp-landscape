#!/usr/bin/env python3
"""Convert Markdown files to DOCX using pandoc."""

import argparse
import subprocess
import sys
from pathlib import Path


def check_pandoc():
    """Check if pandoc is installed."""
    try:
        subprocess.run(['pandoc', '--version'], capture_output=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def convert_md_to_docx(input_path: str, output_path: str = None):
    """Convert a markdown file to docx using pandoc."""
    input_file = Path(input_path)

    if not input_file.exists():
        print(f"Error: Input file not found: {input_path}")
        sys.exit(1)

    if not input_file.suffix.lower() == '.md':
        print(f"Warning: Input file doesn't have .md extension: {input_path}")

    # Default output path: same name with .docx extension
    if output_path is None:
        output_file = input_file.with_suffix('.docx')
    else:
        output_file = Path(output_path)

    # Ensure output directory exists
    output_file.parent.mkdir(parents=True, exist_ok=True)

    print(f"Converting: {input_file}")
    print(f"Output: {output_file}")

    # Preprocess: ensure blank lines before list items that follow non-list lines.
    # Pandoc requires a blank line before a list block; without it, items get merged
    # into the preceding paragraph (e.g. "**Bold header**\n- item" becomes one paragraph).
    raw = input_file.read_text(encoding='utf-8')
    lines = raw.splitlines(keepends=True)
    processed: list[str] = []
    for i, line in enumerate(lines):
        if i > 0 and line.lstrip().startswith('- '):
            prev = lines[i - 1]
            if prev.strip() and not prev.lstrip().startswith('- ') and prev.strip() != '':
                processed.append('\n')
        processed.append(line)
    preprocessed = ''.join(processed)

    # Run pandoc with preprocessed input via stdin
    cmd = [
        'pandoc',
        '-o', str(output_file),
        '--from', 'markdown',
        '--to', 'docx',
    ]

    try:
        result = subprocess.run(cmd, input=preprocessed, capture_output=True, text=True, check=True)
        print(f"Success: {output_file}")
        return str(output_file)
    except subprocess.CalledProcessError as e:
        print(f"Error running pandoc: {e.stderr}")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description='Convert Markdown to DOCX using pandoc',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python scripts/md_to_docx.py Event/actor_rankings.md
  python scripts/md_to_docx.py Event/actor_rankings.md -o output/rankings.docx
  python scripts/md_to_docx.py README.md --output docs/README.docx
        """
    )
    parser.add_argument('input', help='Input markdown file')
    parser.add_argument('-o', '--output', help='Output docx file (default: same name with .docx)')

    args = parser.parse_args()

    # Check pandoc is installed
    if not check_pandoc():
        print("Error: pandoc is not installed.")
        print("Install it with:")
        print("  macOS: brew install pandoc")
        print("  Ubuntu: sudo apt install pandoc")
        print("  Windows: choco install pandoc")
        sys.exit(1)

    convert_md_to_docx(args.input, args.output)


if __name__ == '__main__':
    main()
