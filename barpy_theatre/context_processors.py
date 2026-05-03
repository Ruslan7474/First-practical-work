from barpy_theatre.i18n import get_catalog, normalize_lang


def site_i18n(request):
    lang = normalize_lang(getattr(request, "site_lang", None) or request.session.get("site_lang") or request.COOKIES.get("site_lang"))
    labels = {"ru": "Русский", "ky": "Кыргызча", "en": "English"}
    short_labels = {"ru": "RU", "ky": "KY", "en": "EN"}
    return {
        "site_lang": lang,
        "site_lang_label": short_labels.get(lang, "RU"),
        "site_languages": [
            ("ru", labels["ru"]),
            ("ky", labels["ky"]),
            ("en", labels["en"]),
        ],
        "i18n": get_catalog(lang),
    }
