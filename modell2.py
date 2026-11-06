"""Lukis Werkstatt, Teil 2: Hier löst du die Aufgaben aus AUFGABEN-TEIL2.md.

Diese Datei baut auf DEINEM modell.py aus Teil 1 auf. Ändere modell.py dafür nicht:
Neue Gegner, Türme und das größere Dorf entstehen hier als Unterklassen.
"""

from math import hypot

from modell import Dorf as GrundDorf
from modell import (
    Frostturm,
    Gegner,
    Kanonenturm,
    Pfeilturm,
    Turm,
    sammle_beute,
)
from welt import BAUPLAENE, BAUPLAETZE, GEBAEUDE, MAX_GLEICHE_GEBAEUDE, WELLEN

# Vorbereitet: Der Spielkern findet über dieses Modul auch alle Klassen aus Teil 1.
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
    # TODO Aufgabe 10: Zähle die Gegnerarten einer Welle in einem neuen Dictionary.
    raise NotImplementedError("Aufgabe 10: Der Späher wartet auf seinen Zählauftrag.")


class Schildork(Gegner):
    """Ein Gegner mit Rüstung. Alles andere erbt er von Gegner."""

    def __init__(self, name, leben, tempo, belohnung):
        # TODO Aufgabe 11: Erst super().__init__(...), dann self.ruestung.
        raise NotImplementedError("Aufgabe 11: Der Schildork braucht seinen Konstruktor.")

    def erleide_schaden(self, schaden):
        # TODO Aufgabe 11: Rüstung abziehen, mindestens 1 Schaden, dann super().
        raise NotImplementedError("Aufgabe 11: Der Schild des Schildorks fehlt noch.")


class Troll(Gegner):
    """Ein zäher Gegner, der sich beim Wandern heilt."""

    def __init__(self, name, leben, tempo, belohnung):
        # TODO Aufgabe 12: Erst super().__init__(...), dann self.heilung.
        raise NotImplementedError("Aufgabe 12: Der Troll braucht seinen Konstruktor.")

    def bewege(self, sekunden):
        # TODO Aufgabe 12: Wandern mit super().bewege(...) und danach heilen.
        raise NotImplementedError("Aufgabe 12: Der Troll weiß noch nicht, wie er heilt.")


class Wachtmeister(Turm):
    """Die vierte Turmart. Treffer und Upgrades erbt sie von Turm."""

    def __init__(self, x, y):
        # TODO Aufgabe 13: Basiskonstruktor, dann die eigenen Werte.
        raise NotImplementedError("Aufgabe 13: Der Wachtmeister braucht seinen Konstruktor.")

    def waehle_ziel(self, gegner):
        # TODO Aufgabe 13: Der schwächste erreichbare Gegner.
        raise NotImplementedError("Aufgabe 13: Der Wachtmeister sucht noch sein Ziel.")


class Gebaeude:
    """Ein Gebäude mit Ertrag, zum Beispiel ein Sägewerk."""

    def __init__(self, art, name, ertrag):
        # TODO Aufgabe 14: Merke dir art, name und eine KOPIE von ertrag.
        raise NotImplementedError("Aufgabe 14: Das Gebäude braucht seinen Konstruktor.")

    def liefere(self, vorraete):
        # TODO Aufgabe 14: Addiere den Ertrag zum übergebenen Vorrats-Dictionary.
        raise NotImplementedError("Aufgabe 14: Das Gebäude liefert noch nichts.")


class Dorf(GrundDorf):
    """Rudersdorf aus Teil 1, erweitert um eine Gebäudeliste."""

    def __init__(self):
        """Vorbereitet: Erst das Dorf aus Teil 1 aufbauen, dann ergänzen."""
        super().__init__()
        self.gebaeude = []

    def anzahl(self, art):
        # TODO Aufgabe 14: Wie viele Gebäude dieser Art stehen schon?
        raise NotImplementedError("Aufgabe 14: Zähle die Gebäude einer Art.")

    def baue_gebaeude(self, art):
        # TODO Aufgabe 14: Prüfen, bezahlen, Gebaeude-Objekt anhängen.
        raise NotImplementedError("Aufgabe 14: Rudersdorf lernt gerade, Gebäude zu bauen.")

    def sammle_einkommen(self):
        super().sammle_einkommen()  # Vorbereitet: Häuser und Bewohner aus Aufgabe 8.
        # TODO Aufgabe 14: Danach liefert jedes Gebäude in self.gebaeude seinen Ertrag.


class Chronik:
    """Das Kampfbuch von Rudersdorf: eine Liste besiegter Gegnernamen, älteste zuerst."""

    def __init__(self):
        """Vorbereitet: Eine neue Chronik ist eine leere Liste."""
        self.eintraege = []

    def trage_ein(self, name):
        # TODO Aufgabe 15: Den Namen hinten an die Liste anhängen.
        raise NotImplementedError("Aufgabe 15: Die Chronik wartet auf ihren ersten Eintrag.")

    def letzte(self, anzahl):
        # TODO Aufgabe 15: Höchstens anzahl neueste Einträge, der neueste zuerst.
        raise NotImplementedError("Aufgabe 15: Die Chronik kann noch nicht zurückblättern.")

    def zaehle(self, name):
        # TODO Aufgabe 15: Wie oft steht der Name in der Liste?
        raise NotImplementedError("Aufgabe 15: Die Chronik kann noch nicht zählen.")

    def ohne_doppelte(self):
        # TODO Aufgabe 15: Jeder Name einmal, in der Reihenfolge seines ersten Auftretens.
        raise NotImplementedError("Aufgabe 15: Die Chronik sortiert noch keine Doppelten aus.")


def erstelle_spielstand(dorf, tuerme, welle):
    # TODO Aufgabe 16: Ein Dictionary aus einfachen Werten, bereit für JSON.
    raise NotImplementedError("Aufgabe 16: Der Dorfschreiber kann noch nicht aufschreiben.")


def pruefe_spielstand(daten):
    # TODO Aufgabe 17: Gib eine Liste von Problemen zurück; leer heißt gültig.
    raise NotImplementedError("Aufgabe 17: Der Dorfschreiber prüft noch nicht.")
