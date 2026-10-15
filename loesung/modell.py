"""Referenzlösung: Spielregeln ohne Fenster, Tastatur oder Zufall."""

from math import hypot


class Gegner:
    """Ein Gegner wandert auf einem vorbereiteten Weg Richtung Rudersdorf."""

    def __init__(self, name, leben, tempo, belohnung):
        self.name = name
        self.max_leben = leben
        self.leben = leben
        self.tempo = tempo
        self.belohnung = belohnung
        self.fortschritt = 0.0
        self.x = 0.0
        self.y = 0.0
        self.frost_rest = 0.0

    def erleide_schaden(self, schaden):
        """Negative Treffer ignorieren; Lebenspunkte bleiben mindestens null."""
        self.leben = max(0, self.leben - max(0, schaden))

    def ist_besiegt(self):
        return self.leben <= 0

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
        """Alles oder nichts: Erst ALLE Kosten prüfen, dann abbuchen."""
        for rohstoff, menge in kosten.items():
            if menge < 0 or self.vorraete.get(rohstoff, 0) < menge:
                return False
        for rohstoff, menge in kosten.items():
            if menge:
                self.vorraete[rohstoff] -= menge
        return True

    def erleide_schaden(self, schaden):
        """Vorbereitet: Eine vorhandene Mauer fängt Schaden zuerst ab."""
        schaden = max(0, schaden)
        abgefangen = min(self.mauer, schaden)
        self.mauer -= abgefangen
        self.leben = max(0, self.leben - (schaden - abgefangen))

    def baue_mauer(self):
        if not self.bezahle({"holz": 20, "stein": 30}):
            return False
        self.max_mauer += 5
        self.mauer += 5
        return True

    def repariere_mauer(self):
        if self.mauer == self.max_mauer:
            return False
        if not self.bezahle({"stein": 10}):
            return False
        self.mauer = min(self.max_mauer, self.mauer + 5)
        return True

    def baue_haus(self):
        if not self.bezahle({"gold": 30, "holz": 25}):
            return False
        self.haeuser += 1
        self.bewohner += 4
        return True

    def sammle_einkommen(self):
        self.vorraete["gold"] += self.haeuser * 5
        self.vorraete["holz"] += self.bewohner
        self.vorraete["stein"] += self.haeuser * 3


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
        """Lebender Gegner mit größtem Fortschritt; bei Gleichstand der erste."""
        ziel = None
        for kandidat in gegner:
            abstand = hypot(kandidat.x - self.x, kandidat.y - self.y)
            if not kandidat.ist_besiegt() and abstand <= self.reichweite:
                if ziel is None or kandidat.fortschritt > ziel.fortschritt:
                    ziel = kandidat
        return ziel

    def treffe(self, ziel, gegner):
        ziel.erleide_schaden(self.schaden)

    def verbessere(self, dorf):
        if self.stufe >= 3:
            return False
        if not dorf.bezahle({"gold": 35 * self.stufe}):
            return False
        self.stufe += 1
        self.schaden += 6
        self.reichweite += 15
        return True


class Pfeilturm(Turm):
    """Erbt das vorbereitete Verhalten vollständig."""


class Frostturm(Turm):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.schaden = 5
        self.reichweite = 110
        self.nachladezeit = 1.2

    def treffe(self, ziel, gegner):
        ziel.erleide_schaden(self.schaden)
        ziel.frost_rest = max(ziel.frost_rest, 2.0)


class Kanonenturm(Turm):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.schaden = 18
        self.reichweite = 145
        self.nachladezeit = 1.8

    def treffe(self, ziel, gegner):
        for kandidat in gegner:
            if not kandidat.ist_besiegt():
                if hypot(kandidat.x - ziel.x, kandidat.y - ziel.y) <= 45:
                    kandidat.erleide_schaden(self.schaden)


def sammle_beute(gegner, dorf):
    """Neue Liste lebender Gegner zurückgeben, jeden besiegten einmal belohnen."""
    lebende = []
    for kandidat in gegner:
        if kandidat.ist_besiegt():
            dorf.vorraete["gold"] += kandidat.belohnung
        else:
            lebende.append(kandidat)
    return lebende
