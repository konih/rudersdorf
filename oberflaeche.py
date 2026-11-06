"""Vorbereitete Tkinter-Zeichenwerkstatt. Zum Lösen der Aufgaben nicht nötig."""

import math
import os
import random
import time
import tkinter as tk
from tkinter import font as tkfont

from spielkern import Spiel
from welt import BAUPLAENE, BAUPLAETZE, GEBAEUDE, MAX_GLEICHE_GEBAEUDE, MONSTER, WEG, WELLEN

HINTERGRUND = "#101d24"
TEXT = "#eee8cf"
GOLD = "#e8bc67"
SPIELSTAND = os.path.join(os.path.dirname(os.path.abspath(__file__)), "spielstand.json")
KURZNAMEN = {"pfeil": "Pfeil", "frost": "Frost", "kanone": "Kanone", "wache": "Wache"}
ROHSTOFFKUERZEL = {"gold": "G", "holz": "H", "stein": "S"}
# Wo Gebäude im Dorf erscheinen: zwei Plätze pro Art.
GEBAEUDEPLAETZE = {
    "saegewerk": [(612, 668), (676, 684)],
    "steinbruch": [(345, 650), (395, 668)],
    "markt": [(745, 640), (850, 640)],
}


def preis(kosten):
    """{"gold": 55, "holz": 20} wird zu "55 G · 20 H"."""
    return "  ·  ".join(f"{menge} {ROHSTOFFKUERZEL.get(r, r)}" for r, menge in kosten.items())


class Fenster:
    def __init__(self, wurzel, modell, referenz=False):
        self.wurzel = wurzel
        self.modell = modell
        self.referenz = referenz
        self.spiel = Spiel(modell)
        self.auswahl = "pfeil"
        self.markiert = None
        self.maus = (-100, -100)
        self.fehler = None
        self.zeit = 0
        self.tempo = 1
        self.letztes_bild = time.monotonic()
        self.knopfflaechen = []
        self.knopfschriften = {
            n: tkfont.Font(family="DejaVu Sans", size=n, weight="bold") for n in (9, 10, 11)
        }
        wurzel.title("Rudersdorf · Die Orks kommen!")
        wurzel.resizable(False, False)
        self.bild = tk.Canvas(wurzel, width=1180, height=760, bg=HINTERGRUND, highlightthickness=0)
        self.bild.pack()
        self.bild.bind("<Button-1>", self.klick)
        self.bild.bind("<Motion>", lambda e: setattr(self, "maus", (e.x, e.y)))
        wurzel.bind("1", lambda e: self.waehle("pfeil"))
        wurzel.bind("2", lambda e: self.waehle("frost"))
        wurzel.bind("3", lambda e: self.waehle("kanone"))
        wurzel.bind("4", lambda e: self.waehle("wache"))
        wurzel.bind("f", lambda e: self.schalte_tempo())
        wurzel.bind("s", lambda e: self.sicher(lambda: self.spiel.speichere(SPIELSTAND)))
        wurzel.bind("l", lambda e: self.sicher(lambda: self.spiel.lade(SPIELSTAND)))
        wurzel.bind("<space>", lambda e: self.sicher(self.weiter))
        wurzel.bind("n", lambda e: self.sicher(self.spiel.starte_welle))
        wurzel.bind("r", lambda e: self.neustart())
        wurzel.bind("<Escape>", lambda e: self.schliesse_hinweis())
        self.zeichne_land()
        self.tick()

    def text(self, x, y, inhalt, groesse=12, farbe=TEXT, fett=False, **extra):
        return self.bild.create_text(
            x,
            y,
            text=inhalt,
            fill=farbe,
            anchor="nw",
            font=("DejaVu Sans", groesse, "bold" if fett else "normal"),
            tags="beweglich",
            **extra,
        )

    def rechteck(self, *punkte, **optionen):
        return self.bild.create_rectangle(*punkte, tags="beweglich", **optionen)

    def oval(self, *punkte, **optionen):
        return self.bild.create_oval(*punkte, tags="beweglich", **optionen)

    def linie(self, *punkte, **optionen):
        return self.bild.create_line(*punkte, tags="beweglich", **optionen)

    def polygon(self, *punkte, **optionen):
        return self.bild.create_polygon(*punkte, tags="beweglich", **optionen)

    def zeichne_land(self):
        c = self.bild
        c.create_rectangle(0, 85, 920, 705, fill="#314c3b", outline="")
        zufall = random.Random(17)
        for _ in range(240):
            x, y = zufall.randrange(920), zufall.randrange(98, 700)
            c.create_line(x, y, x + 3, y - 4, fill=zufall.choice(["#3e5b43", "#3b5741", "#496148"]))
        # Kleine Wasserfläche und Schilf.
        c.create_oval(560, 100, 755, 245, fill="#263e3a", outline="", width=10)
        c.create_oval(575, 111, 744, 232, fill="#416e70", outline="#658583", width=3)
        for x, y in [(605, 145), (650, 195), (695, 151)]:
            c.create_line(x, y, x + 24, y, fill="#82a9a0", width=2)
        for x, y in [(570, 180), (727, 210), (590, 220)]:
            c.create_line(x, y, x - 3, y - 17, fill="#9eaa70", width=2)
            c.create_line(x + 4, y, x + 8, y - 21, fill="#9eaa70", width=2)
        punkte = [wert for punkt in WEG for wert in punkt]
        c.create_line(*punkte, fill="#253b31", width=56, joinstyle="round", capstyle="round")
        c.create_line(*punkte, fill="#82734f", width=44, joinstyle="round", capstyle="round")
        c.create_line(*punkte, fill="#ac9667", width=32, joinstyle="round", capstyle="round")
        c.create_line(*punkte, fill="#bba77d", width=2, dash=(3, 16))
        for x, y, s in [
            (45, 140, 1.2),
            (85, 119, 1),
            (155, 110, 1.1),
            (39, 420, 1.3),
            (90, 455, 1),
            (135, 530, 1.2),
            (70, 600, 1.3),
            (170, 650, 1),
            (510, 120, 0.8),
            (520, 430, 0.9),
            (580, 345, 0.9),
            (720, 580, 1.2),
            (780, 625, 1),
            (825, 580, 0.8),
            (880, 650, 1.3),
            (295, 120, 0.65),
        ]:
            c.create_oval(
                x - 22 * s, y + 15 * s, x + 23 * s, y + 27 * s, fill="#293e32", outline=""
            )
            c.create_rectangle(x - 4 * s, y, x + 4 * s, y + 20 * s, fill="#68513b", outline="")
            for off, breite in [(0, 25), (-14, 21), (-27, 16)]:
                c.create_polygon(
                    x,
                    y + (off - 35) * s,
                    x - breite * s,
                    y + (off + 8) * s,
                    x + breite * s,
                    y + (off + 8) * s,
                    fill="#203e33" if off == 0 else "#456a48",
                    outline="#294735",
                )
        c.create_rectangle(752, 260, 908, 402, fill="#6a7051", outline="#84916a", width=2)
        c.create_oval(770, 280, 900, 394, fill="#92916a", outline="")
        c.create_text(
            30,
            110,
            text="D E R   F L Ü S T E R W A L D",
            fill="#a6b691",
            anchor="nw",
            font=("DejaVu Sans", 10),
        )
        c.create_text(
            750,
            235,
            text="R U D E R S D O R F",
            fill="#e7dfb8",
            anchor="nw",
            font=("DejaVu Sans", 10, "bold"),
        )
        c.create_text(
            38, 337, text="ORKPFAD  →", fill="#d2c297", anchor="nw", font=("DejaVu Sans", 9, "bold")
        )
        # Getreidefeld: ein erster Erweiterungspunkt für Bauern und Nahrung.
        c.create_rectangle(780, 460, 887, 536, fill="#776c3d", outline="#b19a55", width=2)
        for x in range(790, 884, 12):
            for y in range(472, 530, 13):
                c.create_line(x, y, x, y - 7, fill="#d5b867", width=2)
                c.create_line(x - 3, y - 6, x, y - 4, x + 3, y - 7, fill="#d5b867")

    def haus(self, x, y, gross=False):
        breite, hoehe = (39, 35) if gross else (24, 23)
        self.oval(
            x - breite - 4, y + hoehe - 3, x + breite + 8, y + hoehe + 7, fill="#526248", outline=""
        )
        self.rechteck(
            x - breite, y, x + breite, y + hoehe, fill="#d4bb8a", outline="#594f3b", width=2
        )
        self.polygon(
            x - breite - 6,
            y,
            x,
            y - 22,
            x + breite + 6,
            y,
            fill="#8c4e3d",
            outline="#543e33",
            width=2,
        )
        self.linie(x, y, x, y + hoehe, fill="#705337", width=3)
        self.linie(x - breite, y + 10, x + breite, y + 10, fill="#705337", width=2)
        self.rechteck(x - 6, y + hoehe - 15, x + 6, y + hoehe, fill="#513e32", outline="")
        self.rechteck(x - breite + 6, y + 4, x - breite + 13, y + 11, fill="#f2d38a", outline="")
        self.rechteck(x + breite - 13, y + 4, x + breite - 6, y + 11, fill="#f2d38a", outline="")

    def zeichne_dorf(self):
        dorf = self.spiel.dorf
        self.haus(843, 290, True)
        for x, y in [
            (784, 340),
            (879, 352),
            (793, 395),
            (875, 410),
            (735, 500),
            (845, 565),
            (735, 290),
        ][: max(0, dorf.haeuser - 1)]:
            self.haus(x, y)
        # Jedes Haus ist im Zähler sichtbar, auf der Karte maximal acht.
        for i in range(min(dorf.bewohner, 20)):
            x = 780 + (i * 31) % 112 + math.sin(self.zeit * 0.6 + i) * 7
            y = 330 + (i * 19) % 70 + math.cos(self.zeit * 0.8 + i) * 5
            self.oval(x - 3, y + 4, x + 5, y + 8, fill="#666d4b", outline="")
            self.rechteck(
                x - 2,
                y - 1,
                x + 3,
                y + 6,
                fill=["#d6a65a", "#809bb2", "#b26d50"][i % 3],
                outline="",
            )
            self.oval(x - 2, y - 6, x + 3, y - 1, fill="#e1bf91", outline="")
        if dorf.max_mauer:
            farbe = "#9ca5a0" if dorf.mauer else "#636d65"
            for a, b in [(745, 815), (865, 915)]:
                self.rechteck(a, 410, b, 431, fill=farbe, outline="#48574f", width=2)
                for x in range(a, b, 14):
                    self.rechteck(x, 402, x + 8, 413, fill=farbe, outline="#48574f")
            self.text(770, 441, f"Stadtmauer  {dorf.mauer}/{dorf.max_mauer}", 9)
        for art, plaetze in GEBAEUDEPLAETZE.items():
            for x, y in plaetze[: self.anzahl_gebaeude(art)]:
                self.gebaeude(x, y, art)
        # Dorfwimpel.
        self.linie(843, 267, 843, 239, fill="#c7b28a", width=2)
        self.polygon(
            844, 239, 864 + math.sin(self.zeit * 3) * 3, 244, 844, 252, fill="#dfb55c", outline=""
        )

    def anzahl_gebaeude(self, art):
        return sum(1 for g in getattr(self.spiel.dorf, "gebaeude", []) if g.art == art)

    def gebaeude(self, x, y, art):
        self.oval(x - 30, y + 12, x + 30, y + 22, fill="#2b4234", outline="")
        if art == "saegewerk":
            self.rechteck(x - 26, y - 8, x + 22, y + 16, fill="#9a7550", outline="#4b3b2b", width=2)
            self.polygon(x - 30, y - 8, x - 2, y - 24, x + 26, y - 8, fill="#6e5236", outline="")
            for dy in (0, 7):
                self.linie(x + 22, y + dy, x + 34, y + dy, fill="#c8a46e", width=4)
            self.oval(x - 20, y - 2, x - 4, y + 14, fill="#b7bcbd", outline="#565e5f", width=2)
        elif art == "steinbruch":
            self.polygon(
                x - 28,
                y + 16,
                x - 14,
                y - 16,
                x + 4,
                y - 4,
                x + 26,
                y - 18,
                x + 30,
                y + 16,
                fill="#8d9293",
                outline="#4f5759",
                width=2,
            )
            for dx, dy in ((-10, 4), (8, 8), (16, -4)):
                self.rechteck(x + dx, y + dy, x + dx + 9, y + dy + 6, fill="#c3c7c4", outline="")
        else:
            self.rechteck(x - 24, y - 4, x + 24, y + 16, fill="#a8865a", outline="#4b3b2b", width=2)
            for i, farbe in enumerate(("#c4513f", "#e8d6a4", "#c4513f", "#e8d6a4")):
                self.polygon(
                    x - 28 + i * 14,
                    y - 4,
                    x - 21 + i * 14,
                    y - 18,
                    x - 14 + i * 14,
                    y - 4,
                    fill=farbe,
                    outline="",
                )
            self.oval(x - 8, y + 2, x + 2, y + 12, fill=GOLD, outline="")

    def zeichne_turm(self, x, y, art, stufe):
        farbe = BAUPLAENE[art]["farbe"]
        self.oval(x - 25, y + 12, x + 25, y + 26, fill="#253e32", outline="")
        self.rechteck(x - 17, y - 13, x + 17, y + 17, fill="#929c8e", outline="#344a40", width=2)
        self.linie(x - 16, y + 3, x + 17, y + 3, fill="#596d5e", width=2)
        self.linie(x, y + 3, x, y + 17, fill="#596d5e", width=2)
        for dx in (-16, -3, 10):
            self.rechteck(x + dx, y - 20, x + dx + 8, y - 10, fill="#bbc0a9", outline="#455b4c")
        if art == "frost":
            self.polygon(
                x,
                y - 39,
                x + 10,
                y - 24,
                x,
                y - 12,
                x - 10,
                y - 24,
                fill=farbe,
                outline="#d3ffff",
                width=2,
            )
        elif art == "wache":
            self.linie(x + 12, y - 12, x + 12, y - 44, fill="#d9cfb0", width=2)
            self.polygon(x + 13, y - 44, x + 31, y - 38, x + 13, y - 31, fill=farbe, outline="")
            self.oval(x - 11, y - 33, x + 7, y - 15, fill="#b7bcc4", outline="#4e5560", width=2)
            self.linie(x - 2, y - 33, x - 2, y - 40, fill=farbe, width=3)
        elif art == "kanone":
            self.linie(x, y - 10, x + 20, y - 29, fill="#303b3c", width=12)
            self.oval(x + 15, y - 34, x + 25, y - 24, fill="#141f26", outline="#9da49b", width=2)
        else:
            self.linie(x - 13, y - 28, x + 13, y - 17, fill=farbe, width=3)
            self.linie(x - 13, y - 17, x + 13, y - 28, fill=farbe, width=3)
            self.linie(x, y - 35, x, y - 10, fill="#e6d4a3", width=2)
        self.text(x - 12, y + 25, "★" * stufe, 10, GOLD)

    def zeichne_gegner(self, gegner):
        x, y = gegner.x, gegner.y
        art = getattr(gegner, "art", "ork")
        r = {"oger": 14, "troll": 17, "schildork": 10}.get(art, 9)
        self.oval(x - r, y + 7, x + r + 4, y + 16, fill="#384537", outline="")
        farbe = {"oger": "#9ab267", "troll": "#7f9a96", "schildork": "#6d8a45"}.get(art, "#7f9e4e")
        if gegner.frost_rest > 0:
            self.oval(x - r - 5, y - r - 5, x + r + 5, y + r + 5, outline="#86dce0", width=2)
        if gegner.art == "wolf":
            self.oval(x - 17, y, x + 13, y + 12, fill="#8c9384", outline="#39453c")
            self.polygon(x + 9, y, x + 22, y + 5, x + 9, y + 10, fill="#a3aa96", outline="")
        self.rechteck(x - r + 2, y, x + r - 2, y + r, fill="#765346", outline="#403e31")
        self.oval(x - r, y - r, x + r, y + 5, fill=farbe, outline="#394c30", width=2)
        self.polygon(x - r, y - 6, x - r - 6, y - 9, x - r, y + 1, fill=farbe, outline="")
        self.polygon(x + r, y - 6, x + r + 6, y - 9, x + r, y + 1, fill=farbe, outline="")
        self.oval(x - 5, y - 5, x - 2, y - 2, fill="#ece3ad", outline="")
        self.oval(x + 3, y - 5, x + 6, y - 2, fill="#ece3ad", outline="")
        self.linie(x + r + 5, y - 4, x + r + 5, y + 13, fill="#b4a886", width=2)
        if art == "schildork":
            self.oval(
                x - r - 9, y - 6, x - r + 3, y + 12, fill="#8b939c", outline="#d8dde0", width=2
            )
            self.oval(x - r - 5, y + 1, x - r - 1, y + 5, fill="#d8dde0", outline="")
        elif art == "troll":
            self.linie(x - 6, y - r + 2, x - 3, y - r - 4, fill="#4d625f", width=3)
            self.linie(x + 6, y - r + 2, x + 3, y - r - 4, fill="#4d625f", width=3)
            if gegner.frost_rest <= 0 and gegner.leben < gegner.max_leben:
                funkeln = math.sin(self.zeit * 6 + x) * 4
                self.text(x + r - 2, y - r - 22 + funkeln, "+", 11, "#a8e28a", True)
        self.rechteck(x - 17, y - r - 10, x + 17, y - r - 6, fill="#263b30", outline="")
        self.rechteck(
            x - 17,
            y - r - 10,
            x - 17 + 34 * max(0, gegner.leben / gegner.max_leben),
            y - r - 6,
            fill="#b5ce75",
            outline="",
        )

    def knopf(
        self, x, y, breite, hoehe, titel, aktion, aktiv=True, gewaehlt=False, untertitel=None
    ):
        hover = x <= self.maus[0] <= x + breite and y <= self.maus[1] <= y + hoehe
        farbe = "#405248" if hover and aktiv else "#263931"
        self.rechteck(
            x,
            y,
            x + breite,
            y + hoehe,
            fill=farbe if aktiv else "#202d2a",
            outline=GOLD if gewaehlt else "#536252",
            width=2 if gewaehlt else 1,
        )
        groesse = next(
            (n for n in (11, 10, 9) if self.knopfschriften[n].measure(titel) <= breite - 24), 9
        )
        self.text(x + 12, y + 9, titel, groesse, GOLD if aktiv else "#809083", True)
        if untertitel:
            self.text(x + 12, y + 31, untertitel, 9, "#c4c7ae" if aktiv else "#809083")
        self.knopfflaechen.append((x, y, x + breite, y + hoehe, aktion, aktiv))

    def zeichne(self):
        self.bild.delete("beweglich")
        self.knopfflaechen = []
        s, d = self.spiel, self.spiel.dorf
        self.zeichne_dorf()
        for i, (x, y) in enumerate(BAUPLAETZE):
            if i in s.tuerme:
                turm = s.tuerme[i]
                if self.markiert == i:
                    r = turm.reichweite
                    self.oval(x - r, y - r, x + r, y + r, outline="#cebc7d", dash=(5, 5), width=2)
                self.zeichne_turm(x, y, turm.art, turm.stufe)
            else:
                self.oval(
                    x - 23,
                    y - 23,
                    x + 23,
                    y + 23,
                    fill="#405640",
                    outline="#a5a575",
                    dash=(4, 4),
                    width=2,
                )
                self.text(x - 6, y - 14, "+", 20, "#d5ca91")
        for gegner in s.gegner:
            self.zeichne_gegner(gegner)
        for x, y, a, b, art, _rest in s.effekte:
            self.linie(x, y - 20, a, b, fill=BAUPLAENE[art]["farbe"], width=3)
            if art == "kanone":
                self.oval(a - 22, b - 22, a + 22, b + 22, outline="#f3ae72", width=3)
        for x, y, inhalt, rest in s.anzeigen:
            self.text(x - 10, y, inhalt, 12, GOLD if rest > 0.3 else "#a08a55", True)
        if self.markiert in s.tuerme:
            self.turminfo(s.tuerme[self.markiert])
        # Kopfbereich verdeckt Zeichnungen, die außerhalb der Karte liegen.
        self.rechteck(0, 0, 1180, 85, fill=HINTERGRUND, outline="")
        self.text(25, 14, "RUDERSDORF", 25, GOLD, True)
        self.text(27, 52, "D I E   O R K S   K O M M E N !", 10, "#b7c6ad")
        self.text(395, 20, f"DORF  {d.leben}/{d.max_leben}", 13, TEXT, True)
        self.text(395, 47, f"Mauer {d.mauer}  ·  {d.bewohner} Bewohner", 10, "#b7c6ad")
        for x, schluessel, name, farbe in [
            (655, "gold", "GOLD", GOLD),
            (760, "holz", "HOLZ", "#bccb8c"),
            (865, "stein", "STEIN", "#b2c4c8"),
        ]:
            self.text(x, 17, str(d.vorraete[schluessel]), 20, farbe, True)
            self.text(x, 50, name, 9, "#a6b6ab")
        self.rechteck(920, 85, 1180, 760, fill="#172a28", outline="")
        self.zeichne_seitenleiste(s, d)
        self.rechteck(0, 705, 920, 760, fill=HINTERGRUND, outline="")
        self.text(23, 715, s.hinweis, 11, width=875)
        self.text(
            23,
            740,
            ("REFERENZLÖSUNG" if self.referenz else "LUKIS WERKSTATT")
            + "  ·  1–4 Turm  ·  Leertaste Pause  ·  F Tempo"
            + f" {self.tempo}×  ·  S Speichern  ·  L Laden  ·  R Neustart",
            8,
            "#91a498",
        )
        self.text(1020, 20, "LUKIS DORF", 11, GOLD, True)
        self.text(1010, 46, "Ein Python-Abenteuer", 9, "#a6b6ab")
        if s.phase in ("sieg", "verloren"):
            self.rechteck(200, 280, 720, 465, fill="#172b28", outline=GOLD, width=3)
            self.text(
                235,
                306,
                "RUDERSDORF IST GERETTET!" if s.phase == "sieg" else "DAS DORF BRAUCHT DICH",
                20,
                GOLD,
                True,
            )
            self.text(235, 348, s.hinweis, 12, width=440)
            self.text(
                235,
                396,
                f"Welle {s.welle}  ·  {s.besiegt} Gegner besiegt  ·  {s.beute_gesamt} Gold Beute",
                11,
                "#c4c7ae",
            )
            self.text(235, 425, "Drücke R für eine neue Verteidigung.", 12)
        elif s.pause:
            self.rechteck(310, 305, 640, 385, fill="#172b28", outline=GOLD, width=2)
            self.text(370, 325, "VERSCHNAUFPAUSE", 18, GOLD, True)
        if self.fehler:
            self.rechteck(140, 245, 790, 480, fill="#192c29", outline=GOLD, width=3)
            self.text(170, 270, "DEINE NÄCHSTE MISSION", 20, GOLD, True)
            self.text(170, 315, self.fehler, 12, width=580)
            self.text(
                170,
                395,
                "Öffne AUFGABEN.md und modell.py. Nach einer Änderung\nstarte das Spiel neu. Deine Tests helfen dir beim Tüfteln.",
                11,
                width=580,
            )
            self.text(
                170, 451, "Esc: Hinweis schließen    ·    R: Spiel zurücksetzen", 10, "#bbccae"
            )

    def zeichne_seitenleiste(self, s, d):
        self.text(940, 96, "DEIN VERTEIDIGUNGSPLAN", 10, "#b9c5ad", True)
        for i, (art, plan) in enumerate(BAUPLAENE.items()):
            self.knopf(
                940 + (i % 2) * 113,
                116 + (i // 2) * 56,
                107,
                50,
                f"{i + 1} {KURZNAMEN.get(art, plan['name'])}",
                lambda a=art: self.waehle(a),
                gewaehlt=self.auswahl == art,
                untertitel=preis(plan["kosten"]),
            )
        plan = BAUPLAENE[self.auswahl]
        self.text(940, 230, f"{plan['name']}: {plan['kurz']}", 9, "#abbba6")
        self.text(940, 252, "RUDERSDORF AUSBAUEN", 10, "#b9c5ad", True)
        bauphase = s.phase == "bauen"
        dorfknoepfe = [
            ("Mauer +5", "20 H  ·  30 S", lambda: s.dorf_aktion("baue_mauer")),
            ("Reparatur", "10 S", lambda: s.dorf_aktion("repariere_mauer")),
            ("Haus", "30 G  ·  25 H", lambda: s.dorf_aktion("baue_haus")),
        ]
        for art, plan in GEBAEUDE.items():
            dorfknoepfe.append(
                (
                    f"{plan['name']} {self.anzahl_gebaeude(art)}/{MAX_GLEICHE_GEBAEUDE}",
                    preis(plan["kosten"]),
                    lambda a=art: s.baue_gebaeude(a),
                )
            )
        for i, (titel, untertitel, aktion) in enumerate(dorfknoepfe):
            self.knopf(
                940 + (i % 2) * 113,
                272 + (i // 2) * 52,
                107,
                46,
                titel,
                aktion,
                bauphase,
                untertitel=untertitel,
            )
        turm = s.tuerme.get(self.markiert)
        titel = (
            f"Turm ↑  ·  {35 * turm.stufe} G"
            if turm and turm.stufe < 3
            else "Für Upgrade Turm wählen"
        )
        if turm and turm.stufe >= 3:
            titel = "Höchste Stufe erreicht"
        self.knopf(
            940,
            430,
            220,
            38,
            titel,
            lambda: s.verbessere(self.markiert),
            bauphase and turm is not None and turm.stufe < 3,
        )
        self.text(940, 480, "SPÄHER MELDEN", 10, "#b9c5ad", True)
        self.text(940, 499, self.spaehertext(), 9, "#dcd6b8", width=220)
        self.text(940, 556, "ZULETZT BESIEGT", 10, "#b9c5ad", True)
        self.text(940, 575, self.chroniktext(), 9, "#dcd6b8", width=220)
        self.text(940, 625, f"WELLE {s.welle} / {len(WELLEN)}", 12, GOLD, True)
        self.text(
            940,
            650,
            f"{len(s.gegner) + len(s.warteschlange)} Gegner übrig  ·  {d.haeuser} Häuser",
            10,
        )
        titel = (
            "Nächste Welle  [N]"
            if bauphase
            else ("Weiter  [Leertaste]" if s.pause else "Pause  [Leertaste]")
        )
        if s.phase in ("sieg", "verloren"):
            titel = "Noch einmal spielen  [R]"
        self.knopf(940, 689, 220, 46, titel, self.weiter)

    def spaehertext(self):
        """Zeichnen darf nie abstürzen: Offene Aufgaben erscheinen als Hinweis."""
        try:
            bericht = self.spiel.spaeherbericht()
        except NotImplementedError:
            return "Die Späher warten auf Aufgabe 10."
        except Exception as fehler:
            return f"Späherbericht: {type(fehler).__name__}. Prüfe Aufgabe 10."
        if bericht is None:
            return "Die Welle läuft!" if self.spiel.phase == "welle" else "Keine Gegner mehr."
        teile = [
            f"{anzahl}× {MONSTER[art]['name'] if art in MONSTER else art}"
            for art, anzahl in bericht.items()
        ]
        return "  ·  ".join(teile) or "Keine Gegner gesichtet."

    def chroniktext(self):
        chronik = self.spiel.chronik
        if chronik is None:
            return "Noch keine Chronik."
        try:
            namen = chronik.letzte(4)
        except NotImplementedError:
            return "Die Chronik wartet auf Aufgabe 15."
        except Exception as fehler:
            return f"Chronik: {type(fehler).__name__}. Prüfe Aufgabe 15."
        return "  ·  ".join(str(n) for n in namen) or "Noch niemand besiegt."

    def turminfo(self, turm):
        x, y = turm.x, turm.y
        links = x + 30 if x < 760 else x - 200
        self.rechteck(links, y - 44, links + 170, y - 4, fill="#172b28", outline="#536252")
        self.text(
            links + 8, y - 40, f"{BAUPLAENE[turm.art]['name']} · Stufe {turm.stufe}", 9, GOLD, True
        )
        self.text(
            links + 8,
            y - 23,
            f"{turm.schaden} Schaden · {turm.reichweite} weit · {turm.nachladezeit} s",
            8,
        )

    def schalte_tempo(self):
        self.tempo = 2 if self.tempo == 1 else 1

    def waehle(self, art):
        self.auswahl = art
        self.markiert = None

    def weiter(self):
        if self.spiel.phase == "bauen":
            self.spiel.starte_welle()
        elif self.spiel.phase in ("sieg", "verloren"):
            self.neustart()
        else:
            self.spiel.pause = not self.spiel.pause

    def schliesse_hinweis(self):
        self.fehler = None

    def neustart(self):
        self.spiel = Spiel(self.modell)
        self.fehler = None
        self.markiert = None

    def sicher(self, aktion):
        if self.fehler:
            return
        try:
            aktion()
        except NotImplementedError as fehler:
            self.spiel.pause = True
            self.fehler = str(fehler)
        except Exception as fehler:
            # Echte Programmierfehler bleiben zusätzlich im Terminal nachvollziehbar.
            import traceback

            traceback.print_exc()
            self.spiel.pause = True
            self.fehler = f"Beim Ausprobieren gab es einen Fehler: {type(fehler).__name__}: {fehler}.\nStarte die Tests für deine aktuelle Aufgabe."

    def klick(self, ereignis):
        if self.fehler:
            self.schliesse_hinweis()
            return
        for x, y, a, b, aktion, aktiv in self.knopfflaechen:
            if x <= ereignis.x <= a and y <= ereignis.y <= b:
                if aktiv:
                    self.sicher(aktion)
                return
        for platz, (x, y) in enumerate(BAUPLAETZE):
            if math.hypot(ereignis.x - x, ereignis.y - y) <= 28:
                if platz in self.spiel.tuerme:
                    self.markiert = platz
                else:
                    self.sicher(lambda p=platz: self.spiel.baue_turm(p, self.auswahl))
                return

    def tick(self):
        jetzt = time.monotonic()
        sekunden = min(0.05, jetzt - self.letztes_bild)
        self.letztes_bild = jetzt
        self.zeit += sekunden
        for _ in range(self.tempo):
            self.sicher(lambda: self.spiel.schritt(sekunden))
        self.zeichne()
        self.timer = self.wurzel.after(33, self.tick)
