"""Vorbereiteter Ablauf. Das Lernmodell wird ausdrücklich von außen übergeben."""

import json
from math import hypot

from welt import (
    BAUPLAENE,
    BAUPLAETZE,
    GEBAEUDE,
    MONSTER,
    TEIL1_WELLEN,
    WEG,
    WELLEN,
    WELLEN_STAERKE,
)

LAENGEN = [hypot(b[0] - a[0], b[1] - a[1]) for a, b in zip(WEG, WEG[1:], strict=False)]
WEGLAENGE = sum(LAENGEN)
GEGNERWERTE = ("name", "leben", "tempo", "belohnung")


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
        self.anzeigen = []  # Schwebende Texte wie "+9" über besiegten Gegnern.
        self.welle = 0
        self.warteschlange = []
        self.spawn_rest = 0
        self.phase = "bauen"
        self.pause = False
        self.besiegt = 0
        self.beute_gesamt = 0
        self.chronik = modell.Chronik() if hasattr(modell, "Chronik") else None
        self.hinweis = "Willkommen, Luki! Baue Türme und beschütze Rudersdorf."

    def baue_turm(self, platz, art):
        if self.phase in ("sieg", "verloren") or platz not in range(len(BAUPLAETZE)):
            return False
        if platz in self.tuerme or art not in BAUPLAENE:
            return False
        plan = BAUPLAENE[art]
        turm = getattr(self.modell, plan["klasse"])(*BAUPLAETZE[platz])
        if not self.dorf.bezahle(plan["kosten"]):
            self.hinweis = "Dafür fehlen Vorräte. Spare noch etwas."
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
            daten = MONSTER[art]
            klasse = getattr(self.modell, daten["klasse"])
            werte = {name: daten[name] for name in GEGNERWERTE}
            werte["leben"] = round(werte["leben"] * WELLEN_STAERKE[self.welle])
            gegner = klasse(**werte)
            gegner.art = art
            gegner.x, gegner.y = weg_position(0)
            vorbereitete.append(gegner)
        self.warteschlange = vorbereitete
        self.welle += 1
        self.spawn_rest = 0
        self.phase = "welle"
        self.hinweis = f"Welle {self.welle}: Die Orks sind unterwegs!"
        return True

    def spaeherbericht(self):
        """Gegnerarten der nächsten Welle, nur in der Baupause."""
        if self.phase != "bauen" or self.welle >= len(WELLEN):
            return None
        # Eine Kopie schützt die Weltdaten vor versehentlichen Änderungen.
        return self.modell.spaeherbericht(list(WELLEN[self.welle]))

    def dorf_aktion(self, aktion, *argumente):
        if self.phase != "bauen":
            self.hinweis = "Das Dorf baut und repariert zwischen den Wellen."
            return False
        erfolgreich = getattr(self.dorf, aktion)(*argumente)
        self.hinweis = (
            "Rudersdorf wächst!"
            if erfolgreich
            else "Vorräte fehlen oder bereits vollständig ausgebaut."
        )
        return erfolgreich

    def baue_gebaeude(self, art):
        ok = self.dorf_aktion("baue_gebaeude", art)
        if ok:
            self.hinweis = GEBAEUDE[art]["name"] + " gebaut. Es liefert nach jeder Welle."
        return ok

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
        self.anzeigen = [
            (x, y - 30 * sekunden, text, rest - sekunden)
            for x, y, text, rest in self.anzeigen
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
        besiegte = [g for g in self.gegner if g.ist_besiegt()]
        self.gegner = self.modell.sammle_beute(self.gegner, self.dorf)
        for g in besiegte:
            self.besiegt += 1
            self.beute_gesamt += g.belohnung
            self.anzeigen.append((g.x, g.y - 20, f"+{g.belohnung}", 0.9))
            self.trage_in_chronik_ein(g.name)
        auf_dem_weg = []
        for gegner in self.gegner:
            gegner.bewege(sekunden)
            gegner.x, gegner.y = weg_position(gegner.fortschritt)
            if gegner.fortschritt >= WEGLAENGE:
                self.dorf.erleide_schaden(MONSTER[gegner.art]["dorfschaden"])
            else:
                auf_dem_weg.append(gegner)
        self.gegner = auf_dem_weg
        if self.dorf.leben <= 0:
            self.phase = "verloren"
            self.hinweis = "Das Dorf musste fliehen. Mit einer neuen Strategie klappt es!"
        elif not self.gegner and not self.warteschlange:
            self.beende_welle()

    def trage_in_chronik_ein(self, name):
        if self.chronik is None:
            return
        try:
            self.chronik.trage_ein(name)
        except NotImplementedError:
            pass  # Aufgabe 15 ist eine Anzeige: Sie darf keine Welle unterbrechen.

    def beende_welle(self):
        if self.welle == len(WELLEN):
            self.phase = "sieg"
            self.hinweis = "Rudersdorf ist gerettet! Heute wird auf dem Dorfplatz gefeiert."
            return
        self.phase = "bauen"
        # Grundversorgung funktioniert auch ohne Zusatzaufgabe 8.
        self.dorf.vorraete["gold"] += 35
        self.dorf.vorraete["holz"] += 15
        self.dorf.vorraete["stein"] += 10
        self.hinweis = "Verschnaufpause! +35 Gold, +15 Holz, +10 Stein. Bereit zum Ausbau."
        if self.welle == TEIL1_WELLEN:
            self.hinweis = (
                "Teil 1 geschafft! Doch die Späher melden Schildorks und Trolle. "
                "Neue Missionen warten in AUFGABEN-TEIL2.md."
            )
        try:
            self.dorf.sammle_einkommen()
        except NotImplementedError:
            pass  # Nur diese ausdrücklich optionale Zusatzaufgabe darf fehlen.

    # --- Spielstand (Teil 2, Aufgaben 15 und 16) ---

    def spielstand(self):
        return self.modell.erstelle_spielstand(self.dorf, self.tuerme, self.welle)

    def speichere(self, pfad):
        if self.phase != "bauen":
            self.hinweis = "Gespeichert wird in der Verschnaufpause zwischen den Wellen."
            return False
        text = json.dumps(self.spielstand(), indent=2, ensure_ascii=False)
        with open(pfad, "w", encoding="utf-8") as datei:
            datei.write(text)
        self.hinweis = f"Spielstand vor Welle {self.welle + 1} gespeichert."
        return True

    def lade(self, pfad):
        if self.phase == "welle":
            self.hinweis = "Laden geht nur zwischen den Wellen."
            return False
        try:
            with open(pfad, encoding="utf-8") as datei:
                daten = json.load(datei)
        except FileNotFoundError:
            self.hinweis = "Noch kein Spielstand gespeichert. Drücke S in einer Baupause."
            return False
        except (OSError, UnicodeDecodeError, json.JSONDecodeError):
            self.hinweis = "Der Spielstand ist beschädigt und wurde nicht geladen."
            return False
        return self.lade_spielstand(daten)

    def lade_spielstand(self, daten):
        probleme = self.modell.pruefe_spielstand(daten)
        if probleme:
            self.hinweis = f"Spielstand abgelehnt: {probleme[0]}"
            return False
        # Erst alles neu bauen, dann austauschen: Ein Fehler lässt die Partie unberührt.
        werte = daten["dorf"]
        dorf = self.modell.Dorf()
        dorf.vorraete = dict(werte["vorraete"])
        for name in ("leben", "mauer", "max_mauer", "haeuser", "bewohner"):
            setattr(dorf, name, werte[name])
        for art in werte["gebaeude"]:
            plan = GEBAEUDE[art]
            dorf.gebaeude.append(self.modell.Gebaeude(art, plan["name"], plan["ertrag"]))
        tuerme = {}
        schmiede = self.modell.Dorf()  # Bezahlt die gespeicherten Upgrades noch einmal.
        for eintrag in daten["tuerme"]:
            plan = BAUPLAENE[eintrag["art"]]
            turm = getattr(self.modell, plan["klasse"])(*BAUPLAETZE[eintrag["platz"]])
            turm.art = eintrag["art"]
            while turm.stufe < eintrag["stufe"]:
                schmiede.vorraete["gold"] = 10**6
                if not turm.verbessere(schmiede):
                    break
            tuerme[eintrag["platz"]] = turm
        self.dorf, self.tuerme, self.welle = dorf, tuerme, daten["welle"]
        self.gegner, self.warteschlange, self.effekte, self.anzeigen = [], [], [], []
        self.phase, self.pause = "bauen", False
        self.hinweis = f"Spielstand geladen. Weiter geht es mit Welle {self.welle + 1}."
        return True
