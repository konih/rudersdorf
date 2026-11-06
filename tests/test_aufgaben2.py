"""Teil 2: Identische Verhaltenstests für eigene Implementierung und Referenzlösung."""

import copy
import importlib
import json
import os
import unittest

from welt import BAUPLAETZE, GEBAEUDE, MAX_GLEICHE_GEBAEUDE, WELLEN

REFERENZ = os.environ.get("RUDERSDORF_LOESUNG") == "1"
m1 = importlib.import_module("loesung.modell" if REFERENZ else "modell")
m = importlib.import_module("loesung.modell2" if REFERENZ else "modell2")


class LernTest(unittest.TestCase):
    def gleich(self, ist, soll, hinweis):
        self.assertEqual(ist, soll, f"{hinweis}\n    Erwartet: {soll!r}\n    Bekommen: {ist!r}")

    def gegner(self, klasse=None, x=0, y=0, fortschritt=0, leben=40, max_leben=40, **extra):
        # Absichtlich ohne Konstruktor: Jede Methode ist einzeln testbar.
        g = object.__new__(klasse or m.Gegner)
        g.name, g.leben, g.max_leben = "Test", leben, max_leben
        g.tempo, g.belohnung, g.fortschritt = 40, 10, fortschritt
        g.x, g.y, g.frost_rest = x, y, 0.0
        for name, wert in extra.items():
            setattr(g, name, wert)
        return g

    def turm(self, art, platz, stufe=1):
        t = object.__new__(m.Turm)
        t.art, t.stufe = art, stufe
        t.x, t.y = BAUPLAETZE[platz]
        return t


class Aufgabe10(LernTest):
    """Späherbericht: Gegnerarten in einem Dictionary zählen."""

    def test_01_zaehlen(self):
        self.gleich(
            m.spaeherbericht(["ork", "wolf", "ork", "oger", "ork"]),
            {"ork": 3, "wolf": 1, "oger": 1},
            "Zähle jede Gegnerart. Ein neuer Schlüssel beginnt bei 1, ein bekannter wächst um 1.",
        )

    def test_02_reihenfolge_des_ersten_auftretens(self):
        bericht = m.spaeherbericht(["troll", "ork", "troll", "wolf"])
        self.gleich(
            list(bericht),
            ["troll", "ork", "wolf"],
            "Die Arten erscheinen in der Reihenfolge, in der der Späher sie zuerst sieht. "
            "Ein Dictionary merkt sich die Einfügereihenfolge — sortiere nicht.",
        )

    def test_03_leere_welle(self):
        self.gleich(m.spaeherbericht([]), {}, "Eine leere Welle ergibt einen leeren Bericht.")

    def test_04_welle_bleibt_unveraendert(self):
        welle = ["ork", "ork", "wolf"]
        m.spaeherbericht(welle)
        self.gleich(
            welle, ["ork", "ork", "wolf"], "Der Späher zählt nur, er schickt niemanden weg."
        )

    def test_05_jeder_bericht_ist_neu(self):
        m.spaeherbericht(["ork", "ork"])
        self.gleich(
            m.spaeherbericht(["ork"]),
            {"ork": 1},
            "Jeder Aufruf beginnt mit einem neuen, leeren Dictionary. "
            "Ein Dictionary außerhalb der Funktion würde alte Zählungen mitschleppen.",
        )


class Aufgabe11(LernTest):
    """Vererbung: Der Schildork wehrt kleine Treffer ab."""

    def schildork(self, leben=60, ruestung=4):
        return self.gegner(m.Schildork, leben=leben, max_leben=60, ruestung=ruestung)

    def test_01_konstruktor(self):
        g = m.Schildork("Eisenzahn", 60, 40, 14)
        self.assertIsInstance(g, m1.Gegner, "Ein Schildork soll von Gegner erben.")
        for name, soll in {
            "name": "Eisenzahn",
            "leben": 60,
            "max_leben": 60,
            "tempo": 40,
            "belohnung": 14,
            "fortschritt": 0,
            "frost_rest": 0,
            "ruestung": 4,
        }.items():
            self.gleich(
                getattr(g, name, None),
                soll,
                f"Schildork: Prüfe {name}. Reiche alle vier Werte an super().__init__ weiter "
                "und setze danach self.ruestung.",
            )

    def test_02_ruestung_faengt_ab(self):
        g = self.schildork()
        g.erleide_schaden(12)
        self.gleich(g.leben, 52, "12 Schaden minus 4 Rüstung ergibt 8 Schaden: 60 → 52.")

    def test_03_mindestens_ein_kratzer(self):
        for schaden in (1, 4):
            with self.subTest(schaden=schaden):
                g = self.schildork()
                g.erleide_schaden(schaden)
                self.gleich(
                    g.leben,
                    59,
                    f"Ein echter Treffer mit {schaden} Schaden macht trotz Rüstung mindestens 1 Schaden.",
                )

    def test_04_kein_heiltrank(self):
        for schaden in (0, -7):
            with self.subTest(schaden=schaden):
                g = self.schildork()
                g.erleide_schaden(schaden)
                self.gleich(
                    g.leben, 60, f"{schaden} Schaden ist kein Treffer: kein Kratzer, keine Heilung."
                )

    def test_05_uebertreffer_und_besiegt(self):
        g = self.schildork(leben=3)
        g.erleide_schaden(50)
        self.gleich(
            g.leben,
            0,
            "Auch der Schildork fällt nicht unter 0. Tipp: super().erleide_schaden kennt diese Regel schon.",
        )
        self.assertIs(g.ist_besiegt(), True, "ist_besiegt() erbt der Schildork einfach.")

    def test_06_eigene_ruestung(self):
        g = self.schildork(ruestung=10)
        g.erleide_schaden(13)
        self.gleich(g.leben, 57, "Verwende self.ruestung statt einer festen 4.")

    def test_07_normaler_ork_bleibt_normal(self):
        g = self.gegner(m1.Gegner)
        g.erleide_schaden(12)
        self.gleich(g.leben, 28, "Die Rüstung gehört nur dem Schildork, nicht allen Gegnern.")


class Aufgabe12(LernTest):
    """Überschreiben mit super(): Der Troll heilt sich beim Wandern."""

    def troll(self, leben=100, frost=0.0, heilung=8):
        g = self.gegner(m.Troll, leben=leben, max_leben=170, heilung=heilung)
        g.tempo, g.frost_rest = 20, frost
        return g

    def test_01_konstruktor(self):
        g = m.Troll("Moosbart", 170, 25, 30)
        self.assertIsInstance(g, m1.Gegner, "Ein Troll soll von Gegner erben.")
        for name, soll in {
            "name": "Moosbart",
            "leben": 170,
            "max_leben": 170,
            "tempo": 25,
            "fortschritt": 0,
            "heilung": 8,
        }.items():
            self.gleich(
                getattr(g, name, None),
                soll,
                f"Troll: Prüfe {name}. Erst super().__init__, dann self.heilung = 8.",
            )

    def test_02_wandern_und_heilen(self):
        g = self.troll()
        g.bewege(1)
        self.gleich(
            g.fortschritt, 20, "Der Troll läuft weiter wie jeder Gegner: Rufe super().bewege auf."
        )
        self.gleich(g.leben, 108, "In einer Sekunde heilt der Troll 8 Lebenspunkte: 100 → 108.")

    def test_03_heilung_pro_sekunde(self):
        g = self.troll()
        g.bewege(0.5)
        self.gleich(g.leben, 104, "Die Heilung hängt von der Zeit ab: 8 mal 0.5 Sekunden = 4.")

    def test_04_nicht_ueber_max_leben(self):
        g = self.troll(leben=168)
        g.bewege(2)
        self.gleich(g.leben, 170, "Heilung endet bei max_leben.")

    def test_05_besiegt_bleibt_besiegt(self):
        g = self.troll(leben=0)
        g.bewege(1)
        self.gleich(g.leben, 0, "Ein besiegter Troll darf nicht wiederauferstehen.")

    def test_06_frost_stoppt_heilung(self):
        g = self.troll(frost=0.5)
        g.bewege(1)
        self.gleich(
            g.fortschritt,
            15,
            "Frost bremst den Troll wie jeden Gegner (super().bewege rechnet das schon).",
        )
        self.gleich(
            g.leben,
            100,
            "Ein Troll, der zu Beginn des Schritts gefroren ist, heilt in diesem Schritt nicht. "
            "Merke dir den Frost, BEVOR super().bewege ihn verringert.",
        )
        g.bewege(1)
        self.gleich(g.leben, 108, "Nach dem Auftauen heilt der Troll wieder.")

    def test_07_negative_zeit(self):
        g = self.troll()
        g.bewege(-1)
        self.gleich(
            (g.fortschritt, g.leben), (0, 100), "Negative Zeit bewegt nicht und heilt nicht."
        )


class Aufgabe13(LernTest):
    """Neue Turmart: Der Wachtmeister zielt auf den schwächsten Gegner."""

    def test_01_konstruktor(self):
        t = m.Wachtmeister(7, 8)
        self.assertIsInstance(t, m1.Turm, "Ein Wachtmeister soll von Turm erben.")
        for name, soll in {
            "x": 7,
            "y": 8,
            "stufe": 1,
            "abklingzeit": 0,
            "schaden": 9,
            "reichweite": 160,
            "nachladezeit": 0.7,
        }.items():
            self.gleich(getattr(t, name, None), soll, f"Wachtmeister: Prüfe {name}.")

    def test_02_schwaechster_gewinnt(self):
        t = m.Wachtmeister(0, 0)
        stark_vorn = self.gegner(x=10, fortschritt=300, leben=40)
        schwach = self.gegner(x=20, fortschritt=5, leben=6)
        self.assertIs(
            t.waehle_ziel([stark_vorn, schwach]),
            schwach,
            "Der Wachtmeister wählt die wenigsten AKTUELLEN Lebenspunkte, nicht den größten Fortschritt.",
        )

    def test_03_reichweite_und_besiegte(self):
        t = m.Wachtmeister(0, 0)
        tot = self.gegner(x=5, leben=0)
        fern = self.gegner(x=161, leben=1)
        ziel = self.gegner(x=30, leben=20)
        self.assertIs(
            t.waehle_ziel([tot, fern, ziel]),
            ziel,
            "Besiegte (0 Leben sind nicht 'am schwächsten'!) und zu weit entfernte Gegner zählen nicht.",
        )

    def test_04_rand_und_niemand(self):
        t = m.Wachtmeister(0, 0)
        rand = self.gegner(x=96, y=128)  # Abstand genau 160.
        self.assertIs(t.waehle_ziel([rand]), rand, "Genau auf der Grenze ist noch erreichbar.")
        self.assertIsNone(t.waehle_ziel([]), "Keine Gegner: None.")
        self.assertIsNone(t.waehle_ziel([self.gegner(x=500)]), "Niemand erreichbar: None.")

    def test_05_gleichstand_und_liste(self):
        a, b = self.gegner(x=10, leben=9), self.gegner(x=20, leben=9)
        gegner = [a, b]
        self.assertIs(
            m.Wachtmeister(0, 0).waehle_ziel(gegner), a, "Bei Gleichstand bleibt der erste."
        )
        self.gleich(gegner, [a, b], "Die Liste bleibt unverändert, auch ihre Reihenfolge.")

    def test_06_erbt_treffer_und_upgrade(self):
        t, d = m.Wachtmeister(0, 0), m1.Dorf()
        self.assertIs(t.verbessere(d), True, "verbessere() erbt der Wachtmeister von Turm.")
        g = self.gegner()
        t.treffe(g, [g])
        self.gleich(g.leben, 25, "Nach dem Upgrade trifft er mit 9 + 6 = 15 Schaden.")


class Aufgabe14(LernTest):
    """Klassen zusammenarbeiten lassen: Gebäude bringen Rohstoffe."""

    def test_01_gebaeude_merkt_sich_eine_kopie(self):
        ertrag = {"holz": 15}
        g = m.Gebaeude("saegewerk", "Sägewerk", ertrag)
        self.gleich(
            (g.art, g.name, g.ertrag),
            ("saegewerk", "Sägewerk", {"holz": 15}),
            "Speichere alle drei.",
        )
        ertrag["holz"] = 999
        self.gleich(
            g.ertrag,
            {"holz": 15},
            "Das Gebäude braucht ein EIGENES Dictionary. Tipp: dict(ertrag) baut eine Kopie.",
        )

    def test_02_gebaeude_liefert(self):
        g = m.Gebaeude("x", "Zauberbrunnen", {"gold": 5, "kristalle": 2})
        vorraete = {"gold": 10, "holz": 1}
        g.liefere(vorraete)
        self.gleich(
            vorraete,
            {"gold": 15, "holz": 1, "kristalle": 2},
            "liefere() addiert jeden Ertrag zum übergebenen Vorrat; ein neuer Rohstoff beginnt bei 0.",
        )
        g.liefere(vorraete)
        self.gleich(vorraete["gold"], 20, "Jeder Aufruf liefert erneut.")

    def test_03_dorf_erbt_und_ergaenzt(self):
        self.assertTrue(issubclass(m.Dorf, m1.Dorf), "Das neue Dorf erbt vom Dorf aus Teil 1.")
        a, b = m.Dorf(), m.Dorf()
        self.gleich(
            (a.vorraete, a.leben, a.gebaeude),
            ({"gold": 160, "holz": 80, "stein": 60}, 20, []),
            "Das Dorf startet wie in Teil 1 und zusätzlich mit einer leeren Gebäudeliste.",
        )
        self.assertIsNot(a.gebaeude, b.gebaeude, "Jedes Dorf hat seine eigene Gebäudeliste.")

    def test_04_bauen_kostet_und_merkt(self):
        d = m.Dorf()
        self.assertIs(d.baue_gebaeude("saegewerk"), True, "Ein bezahlbares Sägewerk wird gebaut.")
        self.gleich(
            d.vorraete,
            {"gold": 120, "holz": 80, "stein": 45},
            "Ein Sägewerk kostet laut welt.GEBAEUDE 40 Gold und 15 Stein.",
        )
        self.gleich(len(d.gebaeude), 1, "Das neue Gebäude kommt in self.gebaeude.")
        neu = d.gebaeude[0]
        self.assertIsInstance(
            neu, m.Gebaeude, "Speichere ein Gebaeude-Objekt, nicht nur den Namen."
        )
        self.gleich(
            (neu.art, neu.name, neu.ertrag),
            ("saegewerk", "Sägewerk", {"holz": 15}),
            "Art, Name und Ertrag stammen aus welt.GEBAEUDE.",
        )
        self.gleich(d.anzahl("saegewerk"), 1, "anzahl() zählt Gebäude einer Art.")
        self.gleich(d.anzahl("markt"), 0, "Noch kein Markt gebaut: 0.")

    def test_05_unbekannt_oder_unbezahlbar(self):
        d = m.Dorf()
        d.vorraete["holz"] = 39
        vorher = copy.deepcopy(d.vorraete)
        for art in ("drachenhort", "markt"):
            with self.subTest(art=art):
                self.assertIs(
                    d.baue_gebaeude(art), False, f"{art}: unbekannt oder zu teuer → False."
                )
        self.gleich((d.vorraete, d.gebaeude), (vorher, []), "Ein abgelehnter Bau verändert nichts.")

    def test_06_hoechstens_zwei_gleiche(self):
        d = m.Dorf()
        d.vorraete = {"gold": 999, "holz": 999, "stein": 999}
        for _ in range(MAX_GLEICHE_GEBAEUDE):
            d.baue_gebaeude("steinbruch")
        vorher = dict(d.vorraete)
        self.assertIs(
            d.baue_gebaeude("steinbruch"),
            False,
            f"Höchstens {MAX_GLEICHE_GEBAEUDE} Gebäude derselben Art. Prüfe das VOR dem Bezahlen.",
        )
        self.gleich(d.vorraete, vorher, "Ein abgelehnter dritter Steinbruch kostet nichts.")
        self.assertIs(d.baue_gebaeude("markt"), True, "Eine andere Art ist weiter erlaubt.")

    def test_07_einkommen_mit_gebaeuden(self):
        d = m.Dorf()
        d.gebaeude = [
            m.Gebaeude("saegewerk", "Sägewerk", {"holz": 15}),
            m.Gebaeude("markt", "Marktplatz", {"gold": 20}),
            m.Gebaeude("markt", "Marktplatz", {"gold": 20}),
        ]
        d.sammle_einkommen()
        self.gleich(
            d.vorraete,
            {"gold": 160 + 15 + 40, "holz": 80 + 12 + 15, "stein": 60 + 9},
            "Erst das Einkommen aus Teil 1 (super().sammle_einkommen()), dann liefert jedes Gebäude.",
        )

    def test_08_weltdaten_bleiben_gleich(self):
        vorher = copy.deepcopy(GEBAEUDE)
        d = m.Dorf()
        d.vorraete = {"gold": 999, "holz": 999, "stein": 999}
        d.baue_gebaeude("markt")
        d.sammle_einkommen()
        d.gebaeude[0].ertrag["gold"] = 1
        self.gleich(GEBAEUDE, vorher, "Bauen und Einkommen dürfen welt.GEBAEUDE nie verändern.")


class Aufgabe15(LernTest):
    """Listen: Die Chronik merkt sich jeden besiegten Gegner."""

    def chronik(self, *namen):
        c = m.Chronik()
        c.eintraege = list(namen)  # Unabhängig von trage_ein testbar.
        return c

    def test_01_eintragen_haengt_hinten_an(self):
        c = m.Chronik()
        self.gleich(c.eintraege, [], "Eine neue Chronik beginnt mit einer leeren Liste.")
        for name in ("Ork", "Troll", "Ork"):
            c.trage_ein(name)
        self.gleich(
            c.eintraege,
            ["Ork", "Troll", "Ork"],
            "trage_ein hängt den Namen HINTEN an: Die Liste bleibt in zeitlicher Reihenfolge.",
        )

    def test_02_chroniken_sind_getrennt(self):
        a, b = m.Chronik(), m.Chronik()
        a.trage_ein("Oger")
        self.gleich(b.eintraege, [], "Jede Chronik hat ihre eigene Liste.")

    def test_03_die_letzten_neueste_zuerst(self):
        c = self.chronik("A", "B", "C", "D", "E")
        self.gleich(
            c.letzte(3),
            ["E", "D", "C"],
            "letzte(3) liefert die drei neuesten Einträge, der neueste zuerst.",
        )
        self.gleich(c.letzte(1), ["E"], "letzte(1) ist nur der neueste Eintrag.")

    def test_04_zu_viel_oder_nichts(self):
        c = self.chronik("A", "B")
        self.gleich(c.letzte(10), ["B", "A"], "Mehr verlangt als vorhanden? Dann eben alle.")
        for n in (0, -3):
            with self.subTest(n=n):
                self.gleich(c.letzte(n), [], f"letzte({n}) ergibt eine leere Liste.")
        self.gleich(m.Chronik().letzte(3), [], "Eine leere Chronik hat keine letzten Einträge.")

    def test_05_letzte_veraendert_nichts(self):
        c = self.chronik("A", "B", "C")
        ergebnis = c.letzte(2)
        ergebnis.append("X")
        self.gleich(
            c.eintraege,
            ["A", "B", "C"],
            "letzte() gibt eine NEUE Liste zurück. Drehe nicht die Chronik selbst um.",
        )

    def test_06_zaehlen(self):
        c = self.chronik("Ork", "Wolfsreiter", "Ork", "Troll", "Ork")
        self.gleich(c.zaehle("Ork"), 3, "Zähle, wie oft der Name in der Liste steht.")
        self.gleich(c.zaehle("Drache"), 0, "Ein Name, der nie vorkam, zählt 0.")

    def test_07_ohne_doppelte(self):
        c = self.chronik("Ork", "Troll", "Ork", "Oger", "Troll", "Ork")
        self.gleich(
            c.ohne_doppelte(),
            ["Ork", "Troll", "Oger"],
            "Jeder Name nur einmal, in der Reihenfolge seines ersten Auftretens.",
        )
        self.gleich(
            c.eintraege,
            ["Ork", "Troll", "Ork", "Oger", "Troll", "Ork"],
            "ohne_doppelte() baut eine neue Liste; die Chronik selbst bleibt vollständig.",
        )
        self.gleich(m.Chronik().ohne_doppelte(), [], "Leere Chronik, leere Liste.")


class SpielstandTest(LernTest):
    def beispiel(self):
        d = m.Dorf()
        d.vorraete = {"gold": 95, "holz": 40, "stein": 12}
        d.leben, d.mauer, d.max_mauer = 17, 3, 10
        d.haeuser, d.bewohner = 5, 20
        d.gebaeude = [
            m.Gebaeude("markt", "Marktplatz", {"gold": 20}),
            m.Gebaeude("saegewerk", "Sägewerk", {"holz": 15}),
        ]
        tuerme = {7: self.turm("kanone", 7, 2), 1: self.turm("pfeil", 1, 3)}
        return d, tuerme

    def gueltig(self):
        return {
            "version": 1,
            "welle": 4,
            "dorf": {
                "vorraete": {"gold": 95, "holz": 40, "stein": 12},
                "leben": 17,
                "mauer": 3,
                "max_mauer": 10,
                "haeuser": 5,
                "bewohner": 20,
                "gebaeude": ["markt", "saegewerk"],
            },
            "tuerme": [
                {"platz": 1, "art": "pfeil", "stufe": 3},
                {"platz": 7, "art": "kanone", "stufe": 2},
            ],
        }


class Aufgabe16(SpielstandTest):
    """Zusatz: Den Spielstand als einfaches Dictionary aufschreiben."""

    def test_01_alles_drin(self):
        d, tuerme = self.beispiel()
        self.gleich(
            m.erstelle_spielstand(d, tuerme, 4),
            self.gueltig(),
            "Vergleiche Schlüssel für Schlüssel mit AUFGABEN-TEIL2.md. "
            "Türme kommen als Liste, sortiert nach Bauplatz.",
        )

    def test_02_json_tauglich(self):
        d, tuerme = self.beispiel()
        stand = m.erstelle_spielstand(d, tuerme, 4)
        self.gleich(
            json.loads(json.dumps(stand)),
            stand,
            "Nach JSON und zurück muss alles gleich sein. Speichere nur Zahlen, Texte, Listen "
            "und Dictionaries mit Text-Schlüsseln, keine Objekte.",
        )

    def test_03_eine_kopie_der_vorraete(self):
        d, tuerme = self.beispiel()
        stand = m.erstelle_spielstand(d, tuerme, 4)
        d.vorraete["gold"] = 0
        d.gebaeude.append(m.Gebaeude("markt", "Marktplatz", {"gold": 20}))
        self.gleich(
            (stand["dorf"]["vorraete"]["gold"], len(stand["dorf"]["gebaeude"])),
            (95, 2),
            "Ein Spielstand ist ein Foto: Spätere Änderungen am Dorf dürfen ihn nicht verändern.",
        )

    def test_04_leeres_dorf(self):
        stand = m.erstelle_spielstand(m.Dorf(), {}, 0)
        self.gleich(
            (stand["welle"], stand["tuerme"], stand["dorf"]["gebaeude"]),
            (0, [], []),
            "Ohne Türme und Gebäude entstehen leere Listen.",
        )


class Aufgabe17(SpielstandTest):
    """Zusatz: Einen geladenen Spielstand gründlich prüfen."""

    def kaputt(self, aendern):
        daten = self.gueltig()
        aendern(daten)
        return daten

    def test_01_gueltig_ist_gueltig(self):
        self.gleich(
            m.pruefe_spielstand(self.gueltig()), [], "Ein gültiger Spielstand hat keine Probleme."
        )
        ohne = self.gueltig()
        ohne["tuerme"], ohne["dorf"]["gebaeude"] = [], []
        self.gleich(m.pruefe_spielstand(ohne), [], "Keine Türme und Gebäude sind erlaubt.")

    def test_02_kein_dictionary(self):
        for daten in ([], "hallo", None, 7):
            with self.subTest(daten=daten):
                probleme = m.pruefe_spielstand(daten)
                self.assertIsInstance(probleme, list, "Gib immer eine Liste zurück.")
                self.assertTrue(probleme, "Ein Spielstand muss ein Dictionary sein.")

    def test_03_kaputte_spielstaende(self):
        def ohne(*schluessel):
            def aendern(d):
                ziel = d
                for s in schluessel[:-1]:
                    ziel = ziel[s]
                del ziel[schluessel[-1]]

            return aendern

        def setze(wert, *schluessel):
            def aendern(d):
                ziel = d
                for s in schluessel[:-1]:
                    ziel = ziel[s]
                ziel[schluessel[-1]] = wert

            return aendern

        faelle = {
            "falsche Version": setze(2, "version"),
            "Welle fehlt": ohne("welle"),
            "Welle zu groß": setze(len(WELLEN), "welle"),
            "Welle negativ": setze(-1, "welle"),
            "Welle als Text": setze("3", "welle"),
            "Dorf fehlt": ohne("dorf"),
            "Gold fehlt": ohne("dorf", "vorraete", "gold"),
            "negatives Holz": setze(-5, "dorf", "vorraete", "holz"),
            "Leben 0": setze(0, "dorf", "leben"),
            "Leben zu groß": setze(21, "dorf", "leben"),
            "Mauer über Maximum": setze(11, "dorf", "mauer"),
            "negative Häuser": setze(-1, "dorf", "haeuser"),
            "unbekanntes Gebäude": setze(["markt", "drachenhort"], "dorf", "gebaeude"),
            "drei Märkte": setze(["markt"] * 3, "dorf", "gebaeude"),
            "Türme kein Liste": setze({"1": "pfeil"}, "tuerme"),
            "unbekannte Turmart": setze("laser", "tuerme", 0, "art"),
            "Bauplatz zu groß": setze(len(BAUPLAETZE), "tuerme", 0, "platz"),
            "doppelter Bauplatz": setze(7, "tuerme", 0, "platz"),
            "Stufe 4": setze(4, "tuerme", 1, "stufe"),
            "Stufe fehlt": ohne("tuerme", 1, "stufe"),
        }
        for beschreibung, aendern in faelle.items():
            with self.subTest(fall=beschreibung):
                daten = self.kaputt(aendern)
                vorher = copy.deepcopy(daten)
                try:
                    probleme = m.pruefe_spielstand(daten)
                except NotImplementedError:
                    raise
                except Exception as fehler:
                    self.fail(
                        f"Bei '{beschreibung}' stürzt die Prüfung ab ({type(fehler).__name__}: "
                        f"{fehler}). Prüfe, ob ein Schlüssel existiert, bevor du ihn liest."
                    )
                self.assertTrue(
                    probleme,
                    f"'{beschreibung}' muss mindestens ein Problem melden.",
                )
                self.assertTrue(
                    all(isinstance(p, str) for p in probleme),
                    "Jedes Problem ist ein verständlicher Text.",
                )
                self.gleich(daten, vorher, "Prüfen heißt nur lesen: Ändere die Daten nicht.")
