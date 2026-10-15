"""Lukis Werkstatt: Hier implementierst du die Aufgaben aus AUFGABEN.md."""

from math import hypot


class Gegner:
    """Ein Gegner wandert auf einem vorbereiteten Weg Richtung Rudersdorf."""

    def __init__(self, name, leben, tempo, belohnung):
        # TODO Aufgabe 1: Gib dem Gegner seine Eigenschaften.
        raise NotImplementedError("Aufgabe 1: Gib dem Gegner seine Eigenschaften.")

    def erleide_schaden(self, schaden):
        # TODO Aufgabe 2: Berechne den verbleibenden Lebensvorrat.
        raise NotImplementedError("Aufgabe 2: Berechne den verbleibenden Lebensvorrat.")

    def ist_besiegt(self):
        # TODO Aufgabe 2: Ist der Lebensvorrat aufgebraucht?
        raise NotImplementedError("Aufgabe 2: Ist der Lebensvorrat aufgebraucht?")

    def bewege(self, sekunden):
        """Vorbereitet: Frost wirkt nur während seiner verbleibenden Dauer."""
        sekunden = max(0, sekunden)
        frostzeit = min(sekunden, self.frost_rest)
        self.fortschritt += self.tempo * (sekunden - frostzeit * 0.5)
        self.frost_rest = max(0, self.frost_rest - sekunden)


class Dorf:
    """Rudersdorfs Vorräte und Gebäude. Jedes Dorf hat eigene Vorräte."""

    def __init__(self):
        self.vorraete = {"gold": 160, "holz": 80, "stein": 60}
        self.leben = 20
        self.max_leben = 20
        self.mauer = 0
        self.max_mauer = 0
        self.haeuser = 3
        self.bewohner = 12

    def bezahle(self, kosten):
        # TODO Aufgabe 3: Prüfe erst alle Kosten, buche erst danach ab.
        raise NotImplementedError("Aufgabe 3: Prüfe erst alle Kosten, buche erst danach ab.")

    def erleide_schaden(self, schaden):
        """Vorbereitet: Eine vorhandene Mauer fängt Schaden zuerst ab."""
        schaden = max(0, schaden)
        abgefangen = min(self.mauer, schaden)
        self.mauer -= abgefangen
        self.leben = max(0, self.leben - (schaden - abgefangen))

    def baue_mauer(self):
        # TODO Aufgabe 7: Zusatzaufgabe Stadtmauer.
        raise NotImplementedError("Aufgabe 7: Zusatzaufgabe Stadtmauer.")

    def repariere_mauer(self):
        # TODO Aufgabe 7: Zusatzaufgabe Reparatur.
        raise NotImplementedError("Aufgabe 7: Zusatzaufgabe Reparatur.")

    def baue_haus(self):
        # TODO Aufgabe 8: Zusatzaufgabe neue Nachbarn.
        raise NotImplementedError("Aufgabe 8: Zusatzaufgabe neue Nachbarn.")

    def sammle_einkommen(self):
        # TODO Aufgabe 8: Zusatzaufgabe Einkommen.
        raise NotImplementedError("Aufgabe 8: Zusatzaufgabe Einkommen.")


class Turm:
    """Gemeinsame Eigenschaften; Unterklassen bestimmen die Trefferwirkung."""

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.stufe = 1
        self.reichweite = 125
        self.schaden = 12
        self.nachladezeit = 0.8
        self.abklingzeit = 0.0

    def waehle_ziel(self, gegner):
        # TODO Aufgabe 4: Suche den gefährlichsten erreichbaren Gegner.
        raise NotImplementedError("Aufgabe 4: Suche den gefährlichsten erreichbaren Gegner.")

    def treffe(self, ziel, gegner):
        ziel.erleide_schaden(self.schaden)

    def verbessere(self, dorf):
        # TODO Aufgabe 9: Zusatzaufgabe Turm-Upgrades.
        raise NotImplementedError("Aufgabe 9: Zusatzaufgabe Turm-Upgrades.")


class Pfeilturm(Turm):
    """Erbt das vorbereitete Verhalten vollständig."""


class Frostturm(Turm):
    def __init__(self, x, y):
        # TODO Aufgabe 5: Starte mit super().__init__(x, y).
        raise NotImplementedError("Aufgabe 5: Starte mit super().__init__(x, y).")

    def treffe(self, ziel, gegner):
        # TODO Aufgabe 5: Treffer und Frost gehören zusammen.
        raise NotImplementedError("Aufgabe 5: Treffer und Frost gehören zusammen.")


class Kanonenturm(Turm):
    def __init__(self, x, y):
        # TODO Aufgabe 5: Auch eine Kanone ist ein Turm.
        raise NotImplementedError("Aufgabe 5: Auch eine Kanone ist ein Turm.")

    def treffe(self, ziel, gegner):
        # TODO Aufgabe 5: Prüfe für jeden Gegner den Abstand zum Einschlag.
        raise NotImplementedError("Aufgabe 5: Prüfe für jeden Gegner den Abstand zum Einschlag.")


def sammle_beute(gegner, dorf):
    # TODO Aufgabe 6: Baue eine neue Liste, ohne die alte zu verändern.
    raise NotImplementedError("Aufgabe 6: Baue eine neue Liste, ohne die alte zu verändern.")
