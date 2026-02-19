"""Path constants and country mappings."""

from pathlib import Path

# Paths
SCRIPT_DIR = Path(__file__).parent.parent
PROJECT_DIR = SCRIPT_DIR.parent
RESEARCH_DIR = PROJECT_DIR / "Research"
LANGUAGES_DIR = RESEARCH_DIR / "Languages"
ACTORS_DIR = RESEARCH_DIR / "Actors"
OUTPUT_DIR = PROJECT_DIR / "output"
WCA_LANGUAGES_PATH = RESEARCH_DIR / "wca_all_languages.yaml"
FOCUSED_LANGUAGES_PATH = RESEARCH_DIR / "focused_languages.yaml"
SOURCE_DATA_DIR = PROJECT_DIR / "Source data"
SOURCES_PATH = SOURCE_DATA_DIR / "sources.yaml"

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
