"""
Common Voice data extraction.
Adapted from speech-resource-finder/data_loaders.py
"""


def get_common_voice_stats(iso_639_3, iso_639_1, cv_data):
    """
    Get Common Voice statistics for a language.

    Args:
        iso_639_3: 3-letter code
        iso_639_1: 2-letter code (can be None)
        cv_data: Common Voice dataset dictionary (from JSON)

    Returns:
        dict with stats or None if not found
    """
    if not cv_data:
        return None

    cv_locale = None
    locale_data = None

    # 1. Try ISO 639-3 code directly
    if iso_639_3 and iso_639_3 in cv_data:
        cv_locale = iso_639_3
        locale_data = cv_data[iso_639_3]

    # 2. Try ISO 639-1 code
    elif iso_639_1 and iso_639_1 in cv_data:
        cv_locale = iso_639_1
        locale_data = cv_data[iso_639_1]

    # 3. Try locale with region suffix (e.g., "ha-NG" for Hausa-Nigeria)
    elif iso_639_1:
        matching = [loc for loc in cv_data.keys() if loc.startswith(iso_639_1 + '-')]
        if matching:
            cv_locale = matching[0]
            locale_data = cv_data[cv_locale]

    if not locale_data:
        return None

    # Extract statistics
    duration_ms = locale_data.get('duration', 0)
    duration_hrs = duration_ms / (1000 * 60 * 60)  # ms to hours

    buckets = locale_data.get('buckets', {})
    validated = buckets.get('validated', 0)
    total_clips = locale_data.get('clips', 0)

    # Gender balance
    gender_splits = locale_data.get('splits', {}).get('gender', {})
    male_pct = gender_splits.get('male_masculine', 0) * 100
    female_pct = gender_splits.get('female_feminine', 0) * 100

    return {
        'locale': cv_locale,
        'total_hours': round(duration_hrs, 1),
        'validated_clips': validated,
        'total_clips': total_clips,
        'train_clips': buckets.get('train', 0),
        'dev_clips': buckets.get('dev', 0),
        'test_clips': buckets.get('test', 0),
        'male_percent': round(male_pct, 1),
        'female_percent': round(female_pct, 1),
    }
