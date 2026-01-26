"""
MMS (Massively Multilingual Speech) language coverage data.
Source: Source data/mms_language_coverage.yaml
(originally from https://dl.fbaipublicfiles.com/mms/misc/language_coverage_mms.html)
"""

from pathlib import Path
import yaml


SCRIPT_DIR = Path(__file__).parent
PROJECT_DIR = SCRIPT_DIR.parent.parent
MMS_DATA_PATH = PROJECT_DIR / "Source data" / "mms_language_coverage.yaml"


def load_mms_data():
    """Load MMS coverage data from YAML.

    Returns:
        dict: Mapping of ISO 639-3 code -> {name, asr, tts, lid}, or empty dict if not found
    """
    if not MMS_DATA_PATH.exists():
        print(f"  Warning: MMS data not found at {MMS_DATA_PATH}")
        return {}

    with open(MMS_DATA_PATH, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)

    return data.get('languages', {})


def get_mms_support(iso_639_3, mms_data):
    """Get MMS support info for a language.

    Args:
        iso_639_3: ISO 639-3 language code
        mms_data: MMS data dict from load_mms_data()

    Returns:
        dict with asr, tts, lid booleans, or None if language not in MMS
    """
    entry = mms_data.get(iso_639_3)
    if not entry:
        return None

    return {
        'asr': entry.get('asr', False),
        'tts': entry.get('tts', False),
        'lid': entry.get('lid', False),
    }
