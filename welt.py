"""Vorbereitete Karte und Baupläne. Hier kannst du später eigene Inhalte erfinden."""

BREITE, HOEHE = 1100, 740
WEG = [
    (-25, 300),
    (160, 300),
    (220, 190),
    (395, 190),
    (450, 365),
    (310, 460),
    (340, 575),
    (560, 575),
    (645, 435),
    (770, 435),
    (845, 360),
]
BAUPLAETZE = [
    (120, 220),
    (265, 270),
    (430, 115),
    (500, 285),
    (375, 380),
    (245, 535),
    (450, 650),
    (580, 475),
    (690, 350),
]
BAUPLAENE = {
    "pfeil": {
        "name": "Pfeilturm",
        "klasse": "Pfeilturm",
        "kosten": {"gold": 45},
        "farbe": "#edc879",
        "kurz": "Schnell & verlässlich",
    },
    "frost": {
        "name": "Frostturm",
        "klasse": "Frostturm",
        "kosten": {"gold": 60},
        "farbe": "#83ddd9",
        "kurz": "Bremst einzelne Orks",
    },
    "kanone": {
        "name": "Kanonenturm",
        "klasse": "Kanonenturm",
        "kosten": {"gold": 75},
        "farbe": "#f39268",
        "kurz": "Trifft eine ganze Gruppe",
    },
}
MONSTER = {
    "ork": {"name": "Ork", "leben": 40, "tempo": 48, "belohnung": 9},
    "wolf": {"name": "Wolfsreiter", "leben": 28, "tempo": 82, "belohnung": 10},
    "oger": {"name": "Oger", "leben": 130, "tempo": 30, "belohnung": 22},
}
WELLEN = [
    ["ork"] * 5,
    ["ork", "wolf", "ork", "wolf", "ork", "ork"],
    ["ork", "ork", "oger", "wolf", "wolf", "ork", "ork"],
    ["wolf", "wolf", "ork", "oger", "ork", "wolf", "oger", "ork"],
    ["oger", "ork", "wolf", "wolf", "oger", "ork", "oger", "wolf", "oger"],
]
