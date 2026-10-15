"""Identische Verhaltenstests für eigene Implementierung und Referenzlösung."""

import importlib
import os
import unittest

m = importlib.import_module(
    "loesung.modell" if os.environ.get("RUDERSDORF_LOESUNG") == "1" else "modell"
)


class LernTest(unittest.TestCase):
    def gleich(self, ist, soll, hinweis):
        self.assertEqual(ist, soll, f"{hinweis}\n    Erwartet: {soll!r}\n    Bekommen: {ist!r}")

    def gegner(self, x=0, y=0, fortschritt=0, leben=40, belohnung=9):
        # Absichtlich unabhängig von Aufgabe 1: Jedes Kapitel ist einzeln testbar.
        g = object.__new__(m.Gegner)
        g.name, g.leben, g.max_leben = "Test-Ork", leben, 40
        g.tempo, g.belohnung, g.fortschritt = 48, belohnung, fortschritt
        g.x, g.y, g.frost_rest = x, y, 0.0
        return g


class Aufgabe01(LernTest):
    """Konstruktor: Jeder Ork bekommt eigene Eigenschaften."""

    def test_01_uebergebene_werte(self):
        g = m.Gegner("Grummel", 70, 33, 11)
        for attribut, soll in {
            "name": "Grummel",
            "leben": 70,
            "max_leben": 70,
            "tempo": 33,
            "belohnung": 11,
        }.items():
            self.gleich(
                getattr(g, attribut, None),
                soll,
                f"Speichere den Parameter in self.{attribut}. Verwende die übergebenen Werte statt fester Zahlen.",
            )

    def test_02_startwerte(self):
        g = m.Gegner("Ork", 40, 48, 9)
        for attribut in ("fortschritt", "x", "y", "frost_rest"):
            self.gleich(
                getattr(g, attribut, None),
                0,
                f"Denke auch an den Startwert: self.{attribut} beginnt bei 0.",
            )

    def test_03_jeder_ork_ist_eigenstaendig(self):
        a, b = m.Gegner("A", 40, 20, 3), m.Gegner("B", 90, 10, 7)
        a.leben = 1
        self.gleich(
            b.leben,
            90,
            "Jeder Gegner braucht eigene Lebenspunkte. Speichere sie am Objekt mit self.",
        )
        self.gleich(b.max_leben, 90, "max_leben merkt sich den ursprünglichen Lebensvorrat.")


class Aufgabe02(LernTest):
    """Lebenspunkte: Treffer, Übertreffer und ungültiger Schaden."""

    def test_01_normaler_treffer(self):
        g = self.gegner()
        g.erleide_schaden(12)
        self.gleich(g.leben, 28, "Ein Treffer mit 12 Schaden soll aus 40 Lebenspunkten 28 machen.")
        self.gleich(g.max_leben, 40, "Der Treffer verändert leben, aber nicht max_leben.")

    def test_02_starker_treffer(self):
        g = self.gegner()
        g.erleide_schaden(100)
        self.gleich(
            g.leben, 0, "Prüfe auch den starken Treffer: Lebenspunkte dürfen nicht unter 0 fallen."
        )

    def test_03_negativer_schaden(self):
        g = self.gegner()
        g.erleide_schaden(-10)
        self.gleich(
            g.leben,
            40,
            "Negativer Schaden ist kein Heiltrank. Ignoriere ihn, ohne den Ork zu heilen.",
        )

    def test_04_null_schaden(self):
        g = self.gegner()
        g.erleide_schaden(0)
        self.gleich(g.leben, 40, "Ein Treffer mit 0 Schaden verändert nichts.")

    def test_05_besiegt_oder_lebendig(self):
        for leben, erwartet in [(1, False), (0, True), (-1, True)]:
            with self.subTest(leben=leben):
                self.assertIs(
                    self.gegner(leben=leben).ist_besiegt(),
                    erwartet,
                    f"Bei {leben} Lebenspunkten soll ist_besiegt() genau {erwartet} zurückgeben. Denke an return und an <= 0.",
                )

    def test_06_mehrere_treffer(self):
        g = self.gegner()
        for schaden in (15, 15, 15, 15):
            g.erleide_schaden(schaden)
        self.gleich(
            g.leben,
            0,
            "Mehrere Treffer bauen auf dem aktuellen Leben auf; auch ein besiegter Ork bleibt bei 0.",
        )


class Aufgabe03(LernTest):
    """Dictionaries: Einkaufen ohne versehentlich Vorräte zu verlieren."""

    def test_01_bezahlbarer_kauf(self):
        d = m.Dorf()
        self.assertIs(
            d.bezahle({"gold": 45, "holz": 10}), True, "Ein bezahlbarer Kauf muss True zurückgeben."
        )
        self.gleich(
            d.vorraete,
            {"gold": 115, "holz": 70, "stein": 60},
            "Ziehe jeden Preis genau einmal ab. Unbenutzte Rohstoffe bleiben gleich.",
        )

    def test_02_exakt_passend(self):
        d = m.Dorf()
        self.assertIs(
            d.bezahle({"gold": 160}), True, "Genau genug Gold reicht! Prüfe mit >= statt nur >."
        )
        self.gleich(d.vorraete["gold"], 0, "Nach einem genau passenden Kauf bleiben 0 Gold.")

    def test_03_abbruch_ohne_teilzahlung(self):
        d = m.Dorf()
        vorher = d.vorraete.copy()
        self.assertIs(
            d.bezahle({"gold": 10, "stein": 999}),
            False,
            "Der zweite Rohstoff fehlt: Der gesamte Kauf muss scheitern.",
        )
        self.gleich(
            d.vorraete,
            vorher,
            "Der bezahlbare Teil reicht noch nicht: Prüfe ALLE Preise, bevor du das erste Gold abziehst.",
        )

    def test_04_unbekannter_rohstoff(self):
        d = m.Dorf()
        vorher = d.vorraete.copy()
        self.assertIs(
            d.bezahle({"kristalle": 1}),
            False,
            "Ein unbekannter Rohstoff hat Bestand 0. Dictionary.get hilft dir.",
        )
        self.gleich(d.vorraete, vorher, "Ein abgelehnter Kauf verändert keine Vorräte.")

    def test_05_negative_kosten(self):
        d = m.Dorf()
        vorher = d.vorraete.copy()
        self.assertIs(
            d.bezahle({"gold": 10, "holz": -5}),
            False,
            "Negative Kosten sind ungültig. Lehne den gesamten Kauf ab.",
        )
        self.gleich(
            d.vorraete,
            vorher,
            "Ungültige Preise dürfen weder Rohstoffe schenken noch vorher Gold abbuchen.",
        )

    def test_06_kostenlos(self):
        d = m.Dorf()
        vorher = d.vorraete.copy()
        for kosten in ({}, {"gold": 0}, {"kristalle": 0}):
            self.assertIs(
                d.bezahle(kosten),
                True,
                "Kostenlos klappt auch bei einem unbekannten Rohstoff mit Preis 0.",
            )
        self.gleich(
            d.vorraete, vorher, "Ein kostenloser Kauf lässt das Vorrats-Dictionary unverändert."
        )

    def test_07_preisliste_bleibt_gleich(self):
        d = m.Dorf()
        kosten = {"gold": 20, "holz": 3}
        d.bezahle(kosten)
        self.gleich(
            kosten,
            {"gold": 20, "holz": 3},
            "Ändere die Vorräte, nicht das übergebene Preis-Dictionary.",
        )

    def test_08_doerfer_teilen_keine_vorraete(self):
        a, b = m.Dorf(), m.Dorf()
        a.bezahle({"gold": 10})
        self.gleich(b.vorraete["gold"], 160, "Jedes Dorf behält seine eigenen Vorräte.")


class Aufgabe04(LernTest):
    """Listen durchsuchen: Der gefährlichste erreichbare Gegner gewinnt."""

    def test_01_leere_liste(self):
        self.assertIsNone(m.Turm(0, 0).waehle_ziel([]), "Noch kein Gegner da: Gib None zurück.")

    def test_02_gefaehrlichster_statt_naechster(self):
        t = m.Turm(0, 0)
        nah, weit = self.gegner(10, 0, 5), self.gegner(100, 0, 90)
        self.assertIs(
            t.waehle_ziel([nah, weit]),
            weit,
            "Der größte Fortschritt entscheidet, nicht der kleinste Abstand oder die Listenposition.",
        )

    def test_03_reichweite_und_besiegte(self):
        t = m.Turm(0, 0)
        tot = self.gegner(10, 0, 500, 0)
        fern = self.gegner(126, 0, 400)
        lebend = self.gegner(20, 0, 10)
        self.assertIs(
            t.waehle_ziel([tot, fern, lebend]),
            lebend,
            "Überspringe sowohl besiegte als auch zu weit entfernte Gegner.",
        )

    def test_04_genau_auf_dem_rand(self):
        t = m.Turm(10, 20)
        g = self.gegner(85, 120, 50)  # Abstand 125: 75² + 100² = 125².
        self.assertIs(
            t.waehle_ziel([g]),
            g,
            "Genau auf der Reichweitengrenze ist noch erreichbar. Rechne mit beiden Koordinaten und <=.",
        )

    def test_05_niemand_erreichbar(self):
        self.assertIsNone(
            m.Turm(0, 0).waehle_ziel([self.gegner(1000, 0)]),
            "Wenn niemand erreichbar ist, bleibt das Ziel None.",
        )

    def test_06_gleichstand_und_liste_unveraendert(self):
        a, b = self.gegner(20, 0, 80), self.gegner(30, 0, 80)
        gegner = [a, b]
        self.assertIs(
            m.Turm(0, 0).waehle_ziel(gegner),
            a,
            "Bei Gleichstand bleibt der erste passende Gegner das Ziel.",
        )
        self.gleich(
            gegner, [a, b], "Die Zielsuche darf die Gegnerliste weder sortieren noch verkürzen."
        )


class Aufgabe05(LernTest):
    """Vererbung: Frost und Flächenschaden ergänzen den normalen Turm."""

    def test_01_frost_konstruktor(self):
        t = m.Frostturm(12, 34)
        self.assertIsInstance(t, m.Turm, "Ein Frostturm soll von Turm erben.")
        for name, soll in {
            "x": 12,
            "y": 34,
            "stufe": 1,
            "abklingzeit": 0,
            "schaden": 5,
            "reichweite": 110,
            "nachladezeit": 1.2,
        }.items():
            self.gleich(
                getattr(t, name, None),
                soll,
                f"Frostturm: Prüfe {name}. Initialisiere erst mit super(), ändere dann die Spezialwerte.",
            )

    def test_02_kanonen_konstruktor(self):
        t = m.Kanonenturm(56, 78)
        self.assertIsInstance(t, m.Turm, "Ein Kanonenturm soll von Turm erben.")
        for name, soll in {
            "x": 56,
            "y": 78,
            "stufe": 1,
            "abklingzeit": 0,
            "schaden": 18,
            "reichweite": 145,
            "nachladezeit": 1.8,
        }.items():
            self.gleich(
                getattr(t, name, None),
                soll,
                f"Kanonenturm: Prüfe {name}; vergiss den Basiskonstruktor nicht.",
            )

    def test_03_frost_trifft_nur_das_ziel(self):
        t = m.Frostturm(0, 0)
        a, b = self.gegner(), self.gegner()
        t.treffe(a, [a, b])
        self.gleich(
            (a.leben, a.frost_rest),
            (35, 2.0),
            "Frost verursacht 5 Schaden UND setzt die Frostzeit auf mindestens 2 Sekunden.",
        )
        self.gleich(
            (b.leben, b.frost_rest),
            (40, 0),
            "Der Frostturm trifft nur das gewählte Ziel, nicht alle Gegner.",
        )

    def test_04_frost_nicht_verkuerzen(self):
        g = self.gegner()
        g.frost_rest = 4
        m.Frostturm(0, 0).treffe(g, [g])
        self.gleich(
            g.frost_rest,
            4,
            "Ein neuer Frosttreffer darf eine schon längere Frostzeit nicht verkürzen.",
        )

    def test_05_kanone_radius_um_einschlag(self):
        t = m.Kanonenturm(0, 0)
        ziel = self.gegner(100, 100)
        rand = self.gegner(127, 136)  # Abstand zum Ziel genau 45.
        draussen = self.gegner(146, 100)
        am_turm = self.gegner(0, 0)
        tot = self.gegner(100, 100, leben=0)
        gegner = [ziel, rand, draussen, am_turm, tot]
        t.treffe(ziel, gegner)
        self.gleich(
            [g.leben for g in gegner],
            [22, 22, 40, 40, 0],
            "Die Explosion gilt im Radius 45 UM DAS ZIEL, einschließlich Rand. Triff jeden lebenden Gegner darin genau einmal.",
        )
        self.gleich(
            len(gegner),
            5,
            "Die Kanone verursacht Schaden; entferne hier noch keine Gegner aus der Liste.",
        )

    def test_06_schaden_nach_upgrade(self):
        for klasse in (m.Frostturm, m.Kanonenturm):
            with self.subTest(turm=klasse.__name__):
                t = klasse(0, 0)
                t.schaden = 23
                g = self.gegner()
                t.treffe(g, [g])
                self.gleich(
                    g.leben,
                    17,
                    "Nutze self.schaden statt einer festen Zahl in treffe(), damit spätere Upgrades wirken.",
                )


class Aufgabe06(LernTest):
    """Neue Listen bauen: Besiegte entfernen und Gold einsammeln."""

    def test_01_beute_und_ueberlebende(self):
        d = m.Dorf()
        a, b, c = (
            self.gegner(leben=0, belohnung=7),
            self.gegner(),
            self.gegner(leben=0, belohnung=13),
        )
        vorher = [a, b, c]
        nachher = m.sammle_beute(vorher, d)
        self.gleich(
            nachher, [b], "Gib nur die lebenden Gegner zurück, in ihrer ursprünglichen Reihenfolge."
        )
        self.gleich(
            d.vorraete["gold"],
            180,
            "Addiere die Belohnungen aller besiegten Gegner zu vorhandenem Gold.",
        )
        self.gleich(
            vorher,
            [a, b, c],
            "Baue eine neue Liste. Verändere nicht die Liste, die du gerade durchläufst.",
        )
        self.assertIsNot(nachher, vorher, "Das Ergebnis muss eine neue Liste sein.")

    def test_02_besiegte_direkt_hintereinander(self):
        d = m.Dorf()
        ergebnis = m.sammle_beute(
            [self.gegner(leben=0), self.gegner(leben=0), self.gegner(leben=0)], d
        )
        self.gleich(
            ergebnis, [], "Drei besiegte Gegner hintereinander: Überspringe keinen beim Entfernen."
        )
        self.gleich(
            d.vorraete["gold"], 187, "Auch direkt benachbarte besiegte Gegner geben jeweils Gold."
        )

    def test_03_keine_doppelte_beute(self):
        d = m.Dorf()
        rest = m.sammle_beute([self.gegner(leben=0), self.gegner()], d)
        rest = m.sammle_beute(rest, d)
        self.gleich(
            d.vorraete["gold"],
            169,
            "Beim nächsten Aufruf mit der zurückgegebenen Liste darf es keine doppelte Belohnung geben.",
        )
        self.gleich(len(rest), 1, "Der lebende Ork bleibt auf dem Weg.")

    def test_04_leer_und_reihenfolge(self):
        d = m.Dorf()
        self.gleich(m.sammle_beute([], d), [], "Auch eine leere Liste ist erlaubt.")
        a, b = self.gegner(), self.gegner()
        self.gleich(m.sammle_beute([b, a], d), [b, a], "Lebende Gegner behalten ihre Reihenfolge.")
        self.gleich(
            d.vorraete,
            {"gold": 160, "holz": 80, "stein": 60},
            "Ohne besiegte Gegner ändern sich keine Vorräte.",
        )


class Aufgabe07(LernTest):
    """Zusatz: Stadtmauer bauen und reparieren."""

    def test_01_mauer_bauen(self):
        d = m.Dorf()
        self.assertIs(d.baue_mauer(), True, "Mit genug Holz und Stein klappt der Mauerbau.")
        self.gleich(
            (d.mauer, d.max_mauer),
            (5, 5),
            "Ein Ausbau erhöht aktuelle und maximale Mauerpunkte um 5.",
        )
        self.gleich(
            d.vorraete,
            {"gold": 160, "holz": 60, "stein": 30},
            "Mauerbau kostet 20 Holz und 30 Stein.",
        )
        d.baue_mauer()
        self.gleich(
            (d.mauer, d.max_mauer),
            (10, 10),
            "Ein zweiter Ausbau addiert 5, statt wieder auf 5 zu setzen.",
        )

    def test_02_fehlende_vorraete(self):
        d = m.Dorf()
        d.vorraete["stein"] = 0
        vorher = d.vorraete.copy()
        self.assertIs(d.baue_mauer(), False, "Ohne Stein kann keine Mauer gebaut werden.")
        self.gleich(
            (d.mauer, d.max_mauer, d.vorraete),
            (0, 0, vorher),
            "Ein gescheiterter Ausbau verändert weder Mauer noch Vorräte.",
        )

    def test_03_reparieren_bis_zum_maximum(self):
        d = m.Dorf()
        d.mauer, d.max_mauer = 3, 5
        self.assertIs(d.repariere_mauer(), True, "Eine beschädigte Mauer kann repariert werden.")
        self.gleich(
            (d.mauer, d.max_mauer, d.vorraete["stein"]),
            (5, 5, 50),
            "Reparatur kostet 10 Stein, heilt bis zu 5 Punkte und bleibt am Maximum stehen.",
        )

    def test_04_volle_oder_fehlende_mauer(self):
        for punkte in (0, 5):
            d = m.Dorf()
            d.mauer = d.max_mauer = punkte
            self.assertIs(
                d.repariere_mauer(),
                False,
                "Ohne Mauer oder bei voller Mauer gibt es nichts zu reparieren.",
            )
            self.gleich(
                d.vorraete["stein"], 60, "Eine unnötige Reparatur darf keinen Stein verbrauchen."
            )

    def test_05_reparatur_ohne_stein(self):
        d = m.Dorf()
        d.mauer, d.max_mauer = 1, 10
        d.vorraete["stein"] = 9
        self.assertIs(
            d.repariere_mauer(), False, "9 Stein reichen nicht für eine Reparatur für 10 Stein."
        )
        self.gleich(
            (d.mauer, d.max_mauer, d.vorraete["stein"]),
            (1, 10, 9),
            "Eine unbezahlbare Reparatur verändert nichts.",
        )


class Aufgabe08(LernTest):
    """Zusatz: Häuser, Bewohner und Einkommen."""

    def test_01_haus_bauen(self):
        d = m.Dorf()
        self.assertIs(d.baue_haus(), True, "Mit genug Vorräten zieht eine neue Familie ein.")
        self.gleich((d.haeuser, d.bewohner), (4, 16), "Ein Haus bedeutet +1 Haus und +4 Bewohner.")
        self.gleich(
            d.vorraete,
            {"gold": 130, "holz": 55, "stein": 60},
            "Ein Haus kostet 30 Gold und 25 Holz.",
        )

    def test_02_haus_nicht_bezahlbar(self):
        d = m.Dorf()
        d.vorraete["holz"] = 24
        vorher = d.vorraete.copy()
        self.assertIs(d.baue_haus(), False, "24 Holz reichen noch nicht: Es werden 25 gebraucht.")
        self.gleich(
            (d.haeuser, d.bewohner, d.vorraete),
            (3, 12, vorher),
            "Ein gescheiterter Hausbau verändert weder Dorf noch Vorräte.",
        )

    def test_03_einkommen(self):
        d = m.Dorf()
        d.haeuser, d.bewohner = 4, 16
        d.sammle_einkommen()
        self.gleich(
            d.vorraete,
            {"gold": 180, "holz": 96, "stein": 72},
            "Pro Haus gibt es 5 Gold und 3 Stein, pro Bewohner 1 Holz. Addiere zum Vorrat.",
        )
        d.sammle_einkommen()
        self.gleich(
            d.vorraete,
            {"gold": 200, "holz": 112, "stein": 84},
            "Jede abgeschlossene Zwischenwelle bringt das Einkommen erneut.",
        )

    def test_04_leeres_dorf(self):
        d = m.Dorf()
        d.haeuser, d.bewohner = 0, 0
        d.sammle_einkommen()
        self.gleich(
            d.vorraete,
            {"gold": 160, "holz": 80, "stein": 60},
            "Ein Dorf ohne Häuser und Bewohner erzeugt kein Einkommen.",
        )


class Aufgabe09(LernTest):
    """Zusatz: Turm-Upgrades bis Stufe 3."""

    def test_01_verbessern(self):
        d, t = m.Dorf(), m.Pfeilturm(0, 0)
        self.assertIs(t.verbessere(d), True, "Ein bezahlbares Upgrade muss True zurückgeben.")
        self.gleich(
            (t.stufe, t.schaden, t.reichweite, d.vorraete["gold"]),
            (2, 18, 140, 125),
            "Von Stufe 1 kostet das Upgrade 35 Gold und gibt +1 Stufe, +6 Schaden, +15 Reichweite.",
        )
        t.verbessere(d)
        self.gleich(
            (t.stufe, t.schaden, t.reichweite, d.vorraete["gold"]),
            (3, 24, 155, 55),
            "Das zweite Upgrade kostet 35 mal die ALTE Stufe, also 70 Gold.",
        )

    def test_02_maximalstufe(self):
        d, t = m.Dorf(), m.Pfeilturm(0, 0)
        t.stufe = 3
        self.assertIs(
            t.verbessere(d), False, "Auf Stufe 3 ist Schluss. Prüfe das vor dem Bezahlen."
        )
        self.gleich(
            (t.stufe, t.schaden, t.reichweite, d.vorraete["gold"]),
            (3, 12, 125, 160),
            "Ein abgelehntes Upgrade darf nichts verändern.",
        )

    def test_03_zu_wenig_gold(self):
        d, t = m.Dorf(), m.Pfeilturm(0, 0)
        d.vorraete["gold"] = 34
        self.assertIs(t.verbessere(d), False, "34 Gold reichen nicht für das erste Upgrade.")
        self.gleich(
            (t.stufe, t.schaden, t.reichweite, d.vorraete["gold"]),
            (1, 12, 125, 34),
            "Ohne Bezahlung bleiben Turm und Gold unverändert.",
        )

    def test_04_spezialturm_erbt_upgrade(self):
        d, t = m.Dorf(), m.Frostturm(0, 0)
        t.verbessere(d)
        self.gleich(
            (t.stufe, t.schaden, t.reichweite, t.nachladezeit),
            (2, 11, 125, 1.2),
            "Auch der Frostturm erbt verbessere(). Seine eigene Nachladezeit bleibt erhalten.",
        )
