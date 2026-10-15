"""Vorbereiteter Ablauf. Das Lernmodell wird ausdrücklich von außen übergeben."""

from math import hypot

from welt import BAUPLAENE, BAUPLAETZE, MONSTER, WEG, WELLEN

LAENGEN = [hypot(b[0] - a[0], b[1] - a[1]) for a, b in zip(WEG, WEG[1:], strict=False)]
WEGLAENGE = sum(LAENGEN)


def weg_position(fortschritt):
    rest = max(0, fortschritt)
    for a, b, laenge in zip(WEG, WEG[1:], LAENGEN, strict=False):
        if rest <= laenge:
            anteil = rest / laenge
            return a[0] + (b[0] - a[0]) * anteil, a[1] + (b[1] - a[1]) * anteil
        rest -= laenge
    return WEG[-1]


class Spiel:
    def __init__(self, modell):
        self.modell = modell
        self.dorf = modell.Dorf()
        self.tuerme = {}
        self.gegner = []
        self.effekte = []
        self.welle = 0
        self.warteschlange = []
        self.spawn_rest = 0
        self.phase = "bauen"
        self.pause = False
        self.hinweis = "Willkommen, Luki! Baue Türme und beschütze Rudersdorf."

    def baue_turm(self, platz, art):
        if self.phase in ("sieg", "verloren") or platz not in range(len(BAUPLAETZE)):
            return False
        if platz in self.tuerme or art not in BAUPLAENE:
            return False
        plan = BAUPLAENE[art]
        turm = getattr(self.modell, plan["klasse"])(*BAUPLAETZE[platz])
        if not self.dorf.bezahle(plan["kosten"]):
            self.hinweis = "Dafür fehlen Vorräte. Spare noch etwas Gold."
            return False
        turm.art = art
        self.tuerme[platz] = turm
        self.hinweis = plan["name"] + " ist bereit."
        return True

    def starte_welle(self):
        if self.phase != "bauen":
            return False
        # Erst erstellen, dann Spielzustand ändern: Offene Aufgaben bleiben gefahrlos.
        vorbereitete = []
        for art in WELLEN[self.welle]:
            gegner = self.modell.Gegner(**MONSTER[art])
            gegner.art = art
            gegner.x, gegner.y = weg_position(0)
            vorbereitete.append(gegner)
        self.warteschlange = vorbereitete
        self.welle += 1
        self.spawn_rest = 0
        self.phase = "welle"
        self.hinweis = f"Welle {self.welle}: Die Orks sind unterwegs!"
        return True

    def dorf_aktion(self, aktion):
        if self.phase != "bauen":
            self.hinweis = "Das Dorf baut und repariert zwischen den Wellen."
            return False
        erfolgreich = getattr(self.dorf, aktion)()
        self.hinweis = (
            "Rudersdorf wächst!"
            if erfolgreich
            else "Vorräte fehlen oder bereits vollständig ausgebaut."
        )
        return erfolgreich

    def verbessere(self, platz):
        if self.phase != "bauen" or platz not in self.tuerme:
            return False
        ok = self.tuerme[platz].verbessere(self.dorf)
        self.hinweis = "Turm verbessert!" if ok else "Zu wenig Gold oder schon Stufe 3."
        return ok

    def schritt(self, sekunden):
        if self.pause or self.phase != "welle" or sekunden <= 0:
            return
        self.effekte = [
            (x, y, a, b, art, rest - sekunden)
            for x, y, a, b, art, rest in self.effekte
            if rest > sekunden
        ]
        self.spawn_rest -= sekunden
        while self.warteschlange and self.spawn_rest <= 0:
            self.gegner.append(self.warteschlange.pop(0))
            self.spawn_rest += 1.25
        for turm in self.tuerme.values():
            turm.abklingzeit = max(0, turm.abklingzeit - sekunden)
            if turm.abklingzeit == 0:
                ziel = turm.waehle_ziel(self.gegner)
                if ziel is not None:
                    turm.treffe(ziel, self.gegner)
                    turm.abklingzeit = turm.nachladezeit
                    self.effekte.append((turm.x, turm.y, ziel.x, ziel.y, turm.art, 0.18))
        self.gegner = self.modell.sammle_beute(self.gegner, self.dorf)
        auf_dem_weg = []
        for gegner in self.gegner:
            gegner.bewege(sekunden)
            gegner.x, gegner.y = weg_position(gegner.fortschritt)
            if gegner.fortschritt >= WEGLAENGE:
                self.dorf.erleide_schaden(3 if gegner.art == "oger" else 1)
            else:
                auf_dem_weg.append(gegner)
        self.gegner = auf_dem_weg
        if self.dorf.leben <= 0:
            self.phase = "verloren"
            self.hinweis = "Das Dorf musste fliehen. Mit einer neuen Strategie klappt es!"
        elif not self.gegner and not self.warteschlange:
            if self.welle == len(WELLEN):
                self.phase = "sieg"
                self.hinweis = "Rudersdorf ist gerettet! Heute wird auf dem Dorfplatz gefeiert."
            else:
                self.phase = "bauen"
                # Grundversorgung funktioniert auch ohne Zusatzaufgabe 8.
                self.dorf.vorraete["gold"] += 35
                self.dorf.vorraete["holz"] += 15
                self.dorf.vorraete["stein"] += 10
                self.hinweis = "Verschnaufpause! +35 Gold, +15 Holz, +10 Stein. Bereit zum Ausbau."
                try:
                    self.dorf.sammle_einkommen()
                except NotImplementedError:
                    pass  # Nur diese ausdrücklich optionale Zusatzaufgabe darf fehlen.
