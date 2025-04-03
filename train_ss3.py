from ss3_classifier import ClassifierSS3

examples = {
    "Wyrok": [
        "Wyrok w imieniu Rzeczypospolitej Polskiej.",
        "Sąd orzekł karę pozbawienia wolności.",
        "Na podstawie art. 66 k.k. sąd warunkowo umarza postępowanie."
    ],
    "Postanowienie": [
        "Postanawia: odmówić wszczęcia postępowania.",
        "Na podstawie art. 429 § 1 k.p.k. sprawę przekazuje.",
        "Sąd postanowił oddalić wniosek."
    ],
    "Skarga": [
        "Wnoszę skargę na decyzję organu.",
        "Zaskarżam w całości postanowienie.",
        "Na podstawie art. 52 k.p.a. składam skargę."
    ],
    "Pełnomocnictwo": [
        "Udzielam pełnomocnictwa do reprezentowania mnie.",
        "Pełnomocnikiem będzie radca prawny.",
        "Niniejszym ustanawiam pełnomocnika."
    ],
    "Faktura": [
        "Numer faktury: FV/12/2023.",
        "Kwota netto: 1500 PLN, VAT: 23%.",
        "Nabywca: Jan Kowalski, Sprzedawca: X Sp. z o.o."
    ],
    "Wezwanie": [
        "Wzywa się do stawiennictwa w dniu...",
        "Należy zgłosić się na komisariat.",
        "Termin rozprawy wyznaczono na 12 kwietnia."
    ],
    "Pismo": [
        "W odpowiedzi na pismo z dnia...",
        "Zwracam się z uprzejmą prośbą o...",
        "Informuję, że sprawa została rozpatrzona."
    ]
}

if __name__ == "__main__":
    clf = ClassifierSS3()
    clf.train(examples)
    print("Model został wytrenowany i zapisany jako 'asystent_model.pyss3'")
