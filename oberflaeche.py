"""Vorbereitete Tkinter-Zeichenwerkstatt. Zum Lösen der Aufgaben nicht nötig."""

import math
import random
import time
import tkinter as tk
from tkinter import font as tkfont

from spielkern import Spiel
from welt import BAUPLAENE, BAUPLAETZE, WEG, WELLEN

HINTERGRUND = "#101d24"
TEXT = "#eee8cf"
GOLD = "#e8bc67"


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
        # Dorfwimpel.
        self.linie(843, 267, 843, 239, fill="#c7b28a", width=2)
        self.polygon(
            844, 239, 864 + math.sin(self.zeit * 3) * 3, 244, 844, 252, fill="#dfb55c", outline=""
        )

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
        gross = gegner.art == "oger"
        r = 14 if gross else 9
        self.oval(x - r, y + 7, x + r + 4, y + 16, fill="#384537", outline="")
        farbe = "#9ab267" if gross else "#7f9e4e"
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
        self.text(940, 103, "DEIN VERTEIDIGUNGSPLAN", 10, "#b9c5ad", True)
        for i, (art, plan) in enumerate(BAUPLAENE.items()):
            self.knopf(
                940,
                134 + i * 70,
                220,
                60,
                f"{i + 1}  {plan['name']}  ·  {plan['kosten']['gold']} G",
                lambda a=art: self.waehle(a),
                gewaehlt=self.auswahl == art,
                untertitel=plan["kurz"],
            )
        self.text(940, 352, "Turm wählen → Bauplatz anklicken", 9, "#abbba6")
        self.text(940, 382, "RUDERSDORF AUSBAUEN", 10, "#b9c5ad", True)
        bauphase = s.phase == "bauen"
        self.knopf(
            940,
            408,
            220,
            44,
            "Mauer +5  ·  20 H / 30 S",
            lambda: s.dorf_aktion("baue_mauer"),
            bauphase,
        )
        self.knopf(
            940,
            460,
            220,
            44,
            "Reparatur +5  ·  10 S",
            lambda: s.dorf_aktion("repariere_mauer"),
            bauphase,
        )
        self.knopf(
            940, 512, 220, 44, "Haus · 30 G / 25 H", lambda: s.dorf_aktion("baue_haus"), bauphase
        )
        turm = s.tuerme.get(self.markiert)
        titel = (
            f"Turm ↑  ·  {35 * turm.stufe} G"
            if turm and turm.stufe < 3
            else "Für Upgrade Turm wählen"
        )
        if turm and turm.stufe == 3:
            titel = "Höchste Stufe erreicht"
        self.knopf(
            940,
            564,
            220,
            44,
            titel,
            lambda: s.verbessere(self.markiert),
            bauphase and turm is not None and turm.stufe < 3,
        )
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
        self.rechteck(0, 705, 920, 760, fill=HINTERGRUND, outline="")
        self.text(23, 715, s.hinweis, 11, width=875)
        self.text(
            23,
            740,
            ("REFERENZLÖSUNG" if self.referenz else "LUKIS WERKSTATT")
            + "  ·  1–3 Turm wählen  ·  Leertaste Pause  ·  R Neustart",
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
            self.text(235, 352, s.hinweis, 12, width=440)
            self.text(235, 418, "Drücke R für eine neue Verteidigung.", 12)
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
        self.sicher(lambda: self.spiel.schritt(sekunden))
        self.zeichne()
        self.timer = self.wurzel.after(33, self.tick)
