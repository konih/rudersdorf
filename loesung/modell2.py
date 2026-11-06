"""Referenzlösung Teil 2: baut ausschließlich auf loesung.modell auf."""

from math import hypot

from loesung.modell import Dorf as GrundDorf
from loesung.modell import (
    Frostturm,
    Gegner,
    Kanonenturm,
    Pfeilturm,
    Turm,
    sammle_beute,
)
from welt import BAUPLAENE, BAUPLAETZE, GEBAEUDE, MAX_GLEICHE_GEBAEUDE, WELLEN

# Der Spielkern findet über dieses Modul auch alle Klassen aus Teil 1.
__all__ = [
    "Chronik",
    "Dorf",
    "Frostturm",
    "Gebaeude",
    "Gegner",
    "Kanonenturm",
    "Pfeilturm",
    "Schildork",
    "Troll",
    "Turm",
    "Wachtmeister",
    "erstelle_spielstand",
    "pruefe_spielstand",
    "sammle_beute",
    "spaeherbericht",
]


def spaeherbericht(welle):
    """Zählt Gegnerarten in der Reihenfolge ihres ersten Auftretens."""
    bericht = {}
    for art in welle:
        bericht[art] = bericht.get(art, 0) + 1
    return bericht


class Schildork(Gegner):
    def __init__(self, name, leben, tempo, belohnung):
        super().__init__(name, leben, tempo, belohnung)
        self.ruestung = 4

    def erleide_schaden(self, schaden):
        """Rüstung fängt ab, aber jeder echte Treffer kratzt mindestens 1 Punkt."""
        if schaden <= 0:
            return
        super().erleide_schaden(max(1, schaden - self.ruestung))


class Troll(Gegner):
    def __init__(self, name, leben, tempo, belohnung):
        super().__init__(name, leben, tempo, belohnung)
        self.heilung = 8

    def bewege(self, sekunden):
        """Gefroren zu Beginn des Schritts? Dann keine Heilung in diesem Schritt."""
        war_gefroren = self.frost_rest > 0
        super().bewege(sekunden)
        if sekunden > 0 and not war_gefroren and not self.ist_besiegt():
            self.leben = min(self.max_leben, self.leben + self.heilung * sekunden)


class Wachtmeister(Turm):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.schaden = 9
        self.reichweite = 160
        self.nachladezeit = 0.7

    def waehle_ziel(self, gegner):
        """Lebender Gegner mit den wenigsten Lebenspunkten; bei Gleichstand der erste."""
        ziel = None
        for kandidat in gegner:
            abstand = hypot(kandidat.x - self.x, kandidat.y - self.y)
            if not kandidat.ist_besiegt() and abstand <= self.reichweite:
                if ziel is None or kandidat.leben < ziel.leben:
                    ziel = kandidat
        return ziel


class Gebaeude:
    def __init__(self, art, name, ertrag):
        self.art = art
        self.name = name
        self.ertrag = dict(ertrag)

    def liefere(self, vorraete):
        for rohstoff, menge in self.ertrag.items():
            vorraete[rohstoff] = vorraete.get(rohstoff, 0) + menge


class Dorf(GrundDorf):
    def __init__(self):
        super().__init__()
        self.gebaeude = []

    def anzahl(self, art):
        return sum(1 for g in self.gebaeude if g.art == art)

    def baue_gebaeude(self, art):
        if art not in GEBAEUDE or self.anzahl(art) >= MAX_GLEICHE_GEBAEUDE:
            return False
        plan = GEBAEUDE[art]
        if not self.bezahle(plan["kosten"]):
            return False
        self.gebaeude.append(Gebaeude(art, plan["name"], plan["ertrag"]))
        return True

    def sammle_einkommen(self):
        super().sammle_einkommen()
        for gebaeude in self.gebaeude:
            gebaeude.liefere(self.vorraete)


class Chronik:
    """Das Kampfbuch von Rudersdorf: eine Liste besiegter Gegnernamen, älteste zuerst."""

    def __init__(self):
        self.eintraege = []

    def trage_ein(self, name):
        self.eintraege.append(name)

    def letzte(self, anzahl):
        if anzahl <= 0:
            return []
        return self.eintraege[-anzahl:][::-1]

    def zaehle(self, name):
        return self.eintraege.count(name)

    def ohne_doppelte(self):
        einmal = []
        for name in self.eintraege:
            if name not in einmal:
                einmal.append(name)
        return einmal


def erstelle_spielstand(dorf, tuerme, welle):
    """Nur einfache Werte, damit der Stand als JSON gespeichert werden kann."""
    return {
        "version": 1,
        "welle": welle,
        "dorf": {
            "vorraete": dict(dorf.vorraete),
            "leben": dorf.leben,
            "mauer": dorf.mauer,
            "max_mauer": dorf.max_mauer,
            "haeuser": dorf.haeuser,
            "bewohner": dorf.bewohner,
            "gebaeude": [g.art for g in dorf.gebaeude],
        },
        "tuerme": [
            {"platz": platz, "art": tuerme[platz].art, "stufe": tuerme[platz].stufe}
            for platz in sorted(tuerme)
        ],
    }


def _zahl(wert, kleinste, groesste=None):
    """Ganze Zahl im Bereich? Wahrheitswerte zählen nicht als Zahl."""
    if type(wert) is not int or wert < kleinste:
        return False
    return groesste is None or wert <= groesste


def pruefe_spielstand(daten):
    """Liste verständlicher Probleme; leer bedeutet: Dieser Stand darf geladen werden."""
    if not isinstance(daten, dict):
        return ["Der Spielstand ist kein Dictionary."]
    probleme = []
    if daten.get("version") != 1:
        probleme.append("Unbekannte Version des Spielstands.")
    if not _zahl(daten.get("welle"), 0, len(WELLEN) - 1):
        probleme.append(f"Die Welle muss eine ganze Zahl von 0 bis {len(WELLEN) - 1} sein.")

    dorf = daten.get("dorf")
    if not isinstance(dorf, dict):
        probleme.append("Die Dorfdaten fehlen.")
    else:
        vorraete = dorf.get("vorraete")
        if not isinstance(vorraete, dict):
            probleme.append("Die Vorräte fehlen.")
        else:
            for rohstoff in ("gold", "holz", "stein"):
                if not _zahl(vorraete.get(rohstoff), 0):
                    probleme.append(f"Vorrat {rohstoff} fehlt oder ist negativ.")
        if not _zahl(dorf.get("leben"), 1, 20):
            probleme.append("Das Dorf braucht 1 bis 20 Lebenspunkte.")
        for name in ("mauer", "max_mauer", "haeuser", "bewohner"):
            if not _zahl(dorf.get(name), 0):
                probleme.append(f"{name} fehlt oder ist negativ.")
        if _zahl(dorf.get("mauer"), 0) and _zahl(dorf.get("max_mauer"), 0):
            if dorf["mauer"] > dorf["max_mauer"]:
                probleme.append("Die Mauer ist stärker als ihr Maximum.")
        gebaeude = dorf.get("gebaeude")
        if not isinstance(gebaeude, list):
            probleme.append("Die Gebäudeliste fehlt.")
        else:
            for art in gebaeude:
                if art not in GEBAEUDE:
                    probleme.append(f"Unbekanntes Gebäude: {art!r}.")
                elif gebaeude.count(art) > MAX_GLEICHE_GEBAEUDE:
                    probleme.append(f"Zu viele Gebäude der Art {art}.")

    tuerme = daten.get("tuerme")
    if not isinstance(tuerme, list):
        probleme.append("Die Turmliste fehlt.")
    else:
        belegt = []
        for turm in tuerme:
            if not isinstance(turm, dict):
                probleme.append("Ein Turm ist kein Dictionary.")
                continue
            platz = turm.get("platz")
            if not _zahl(platz, 0, len(BAUPLAETZE) - 1):
                probleme.append(f"Ungültiger Bauplatz: {platz!r}.")
            elif platz in belegt:
                probleme.append(f"Bauplatz {platz} ist doppelt belegt.")
            else:
                belegt.append(platz)
            if turm.get("art") not in BAUPLAENE:
                probleme.append(f"Unbekannte Turmart: {turm.get('art')!r}.")
            if not _zahl(turm.get("stufe"), 1, 3):
                probleme.append("Eine Turmstufe muss 1, 2 oder 3 sein.")
    return probleme
