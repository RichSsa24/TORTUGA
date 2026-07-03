import pytest
from tortuga.i18n import i18n
from tortuga.action import ActionStrings

def test_i18n_strings():
    strings = ActionStrings(
        title_en="Hello",
        title_es="Hola",
        explain_en="World",
        explain_es="Mundo"
    )
    
    # Default is English
    i18n.lang = "en"
    title, explain = i18n.get(strings)
    assert title == "Hello"
    assert explain == "World"
    
    # Switch to Spanish
    i18n.lang = "es"
    title, explain = i18n.get(strings)
    assert title == "Hola"
    assert explain == "Mundo"

def test_i18n_fallback():
    strings = ActionStrings(
        title_en="English Only",
        explain_en="Missing ES",
        title_es="",
        explain_es=""
    )
    
    i18n.lang = "es"
    # Should fallback to EN gracefully if we had implemented fallback logic,
    # but the current logic just returns title_es which defaults to title_en
    title, explain = i18n.get(strings)
    assert title == "English Only"
    assert explain == "Missing ES"
