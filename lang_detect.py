from lingua import Language, LanguageDetectorBuilder

detector = LanguageDetectorBuilder.from_languages(
    Language.HINDI,
    Language.MARATHI,
    Language.PUNJABI,
    Language.ENGLISH
).build()

def detect_language(text: str) -> str:
    lang = detector.detect_language_of(text)
    return lang.name if lang else "UNKNOWN"

if __name__ == "__main__":
    tests = [
        "मुझे पढ़ाई में मदद चाहिए",
        "I need help with studies",
        "मला मदत हवी आहे"
    ]
    for t in tests:
        print(f"{t} → {detect_language(t)}")