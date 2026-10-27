"""Languages sharing the current templates and the public APKG pipeline."""

LANGUAGES = ("RU", "EN", "ES", "DE", "FR", "JA", "PT-BR")
MODEL_IDS = {
    "RU": 1574587964637,
    "EN": 1600000000001,
    "ES": 1600000000002,
    "DE": 1600000000003,
    "FR": 1600000000004,
    "JA": 1600000000005,
    "PT-BR": 1600000000006,
}
RELEASE = "2026.10.27"
SOURCE_EPOCH = 1793102400
CARD_COUNT = 996
FLAG_COUNT = 235
MEDIA_COUNT = 564


def field_column(name, language):
    return name if language == "EN" else f"{name}:{language.lower()}"
