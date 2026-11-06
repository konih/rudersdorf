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
    "wache": {
        "name": "Wachtmeister",
        "klasse": "Wachtmeister",
        "kosten": {"gold": 55, "holz": 20},
        "farbe": "#c9a3e6",
        "kurz": "Erledigt die Schwächsten",
    },
}
# "klasse" nennt die Modellklasse, "dorfschaden" den Schaden beim Durchbruch.
MONSTER = {
    "ork": {
        "name": "Ork",
        "leben": 40,
        "tempo": 48,
        "belohnung": 9,
        "klasse": "Gegner",
        "dorfschaden": 1,
    },
    "wolf": {
        "name": "Wolfsreiter",
        "leben": 28,
        "tempo": 82,
        "belohnung": 10,
        "klasse": "Gegner",
        "dorfschaden": 1,
    },
    "oger": {
        "name": "Oger",
        "leben": 130,
        "tempo": 30,
        "belohnung": 22,
        "klasse": "Gegner",
        "dorfschaden": 3,
    },
    # Teil 2: Diese Gegner brauchen eigene Klassen aus modell2.py.
    "schildork": {
        "name": "Schildork",
        "leben": 60,
        "tempo": 40,
        "belohnung": 14,
        "klasse": "Schildork",
        "dorfschaden": 2,
    },
    "troll": {
        "name": "Troll",
        "leben": 170,
        "tempo": 25,
        "belohnung": 30,
        "klasse": "Troll",
        "dorfschaden": 4,
    },
}
# Teil 2, Aufgabe 14: Gebäude mit Baukosten und Ertrag pro Verschnaufpause.
GEBAEUDE = {
    "saegewerk": {"name": "Sägewerk", "kosten": {"gold": 40, "stein": 15}, "ertrag": {"holz": 15}},
    "steinbruch": {
        "name": "Steinbruch",
        "kosten": {"gold": 40, "holz": 25},
        "ertrag": {"stein": 12},
    },
    "markt": {"name": "Marktplatz", "kosten": {"holz": 40, "stein": 30}, "ertrag": {"gold": 20}},
}
MAX_GLEICHE_GEBAEUDE = 2
# Welle 1–5 bilden Teil 1. Ab Welle 6 erscheinen Schildorks und Trolle.
TEIL1_WELLEN = 5
# Der Orkkönig stärkt seine Truppen: Lebenspunkte jeder Welle mal diesen Faktor.
WELLEN_STAERKE = [1, 1, 1, 1, 1, 2.5, 4, 5.5, 7, 8.5]
WELLEN = [
    ["ork"] * 5,
    ["ork", "wolf", "ork", "wolf", "ork", "ork"],
    ["ork", "ork", "oger", "wolf", "wolf", "ork", "ork"],
    ["wolf", "wolf", "ork", "oger", "ork", "wolf", "oger", "ork"],
    ["oger", "ork", "wolf", "wolf", "oger", "ork", "oger", "wolf", "oger"],
    ["schildork", "ork", "ork", "schildork", "wolf", "wolf", "ork", "schildork"],
    ["wolf", "wolf", "schildork", "oger", "wolf", "schildork", "troll", "ork"],
    ["troll", "ork", "schildork", "schildork", "wolf", "oger", "wolf", "troll", "ork"],
    ["schildork", "schildork", "oger", "troll", "wolf", "wolf", "oger", "schildork", "troll"],
    [
        "troll",
        "oger",
        "schildork",
        "troll",
        "wolf",
        "wolf",
        "schildork",
        "oger",
        "troll",
        "schildork",
        "troll",
    ],
]
