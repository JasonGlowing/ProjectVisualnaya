from app.ai_service import parse_category, parse_minutes


def test_parse_category_valid():
    assert parse_category("работа") == "работа"


def test_parse_category_invalid():
    assert parse_category("спорт") == "другое"


def test_parse_minutes_valid():
    assert parse_minutes("45") == 45


def test_parse_minutes_with_text():
    assert parse_minutes("примерно 60 минут") == 60
