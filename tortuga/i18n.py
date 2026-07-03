import locale

class I18N:
    def __init__(self):
        # Extremely basic locale detection
        self.lang = "en"
        try:
            loc, _ = locale.getdefaultlocale()
            if loc and loc.startswith("es"):
                self.lang = "es"
        except:
            pass

    def get(self, strings_obj) -> tuple[str, str]:
        if not strings_obj:
            return "No title", "No explanation"
        if self.lang == "es":
            return strings_obj.title_es, strings_obj.explain_es
        return strings_obj.title_en, strings_obj.explain_en

i18n = I18N()
