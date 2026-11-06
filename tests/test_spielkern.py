"""Techniktests: Sie prüfen den vorbereiteten Rahmen mit der Referenzlösung."""

import json
import os
import tempfile
import unittest
from types import SimpleNamespace

from loesung import modell2 as modell
from spielkern import WEGLAENGE, Spiel, weg_position
from welt import TEIL1_WELLEN, WEG, WELLEN


def spiele_welle(s):
    for _ in range(20000):
        s.schritt(0.05)
        if s.phase != "welle":
            return


class SpielkernTests(unittest.TestCase):
    def test_weg_start_ende_und_knick(self):
        self.assertEqual(weg_position(-1), WEG[0])
        self.assertEqual(weg_position(185), WEG[1])
        self.assertEqual(weg_position(WEGLAENGE + 100), WEG[-1])

    def test_bauen_bezahlt_nur_einmal(self):
        s = Spiel(modell)
        self.assertTrue(s.baue_turm(1, "pfeil"))
        self.assertFalse(s.baue_turm(1, "frost"))
        self.assertEqual(s.dorf.vorraete["gold"], 115)
        self.assertEqual(len(s.tuerme), 1)

    def test_unbezahlbarer_und_ungueltiger_turm(self):
        s = Spiel(modell)
        s.dorf.vorraete["gold"] = 0
        self.assertFalse(s.baue_turm(0, "pfeil"))
        self.assertFalse(s.baue_turm(-1, "pfeil"))
        self.assertFalse(s.baue_turm(99, "pfeil"))
        self.assertFalse(s.baue_turm(0, "laser"))
        self.assertEqual(s.tuerme, {})

    def test_pause_stoppt_zeit(self):
        s = Spiel(modell)
        s.starte_welle()
        s.schritt(0.1)
        s.pause = True
        vorher = (s.gegner[0].fortschritt, s.spawn_rest)
        s.schritt(1)
        self.assertEqual((s.gegner[0].fortschritt, s.spawn_rest), vorher)

    def test_keine_doppelte_welle(self):
        s = Spiel(modell)
        self.assertTrue(s.starte_welle())
        self.assertFalse(s.starte_welle())
        self.assertEqual(s.welle, 1)
        self.assertEqual(len(s.warteschlange), 5)

    def test_ausbau_nur_zwischen_wellen(self):
        s = Spiel(modell)
        s.starte_welle()
        self.assertFalse(s.dorf_aktion("baue_mauer"))
        self.assertEqual(s.dorf.max_mauer, 0)

    def test_mauer_faengt_schaden_ab(self):
        d = modell.Dorf()
        d.baue_mauer()
        d.erleide_schaden(7)
        self.assertEqual((d.mauer, d.leben), (0, 18))
        d.erleide_schaden(-5)
        self.assertEqual(d.leben, 18)

    def test_frost_laeuft_waehrend_bewegung_aus(self):
        g = modell.Gegner("Ork", 40, 50, 9)
        g.frost_rest = 0.5
        g.bewege(1)
        self.assertEqual(g.fortschritt, 37.5)
        self.assertEqual(g.frost_rest, 0)
        g.bewege(1)
        self.assertEqual(g.fortschritt, 87.5)

    def test_sieg_mit_ausbaustrategie(self):
        s = Spiel(modell)
        plan = {
            0: [("turm", 1, "pfeil"), ("turm", 4, "pfeil"), ("turm", 7, "pfeil")],
            1: [("haus",), ("gebaeude", "markt")],
            2: [("turm", 3, "kanone"), ("gebaeude", "steinbruch")],
            3: [("turm", 5, "frost"), ("mauer",)],
            4: [("turm", 8, "wache"), ("gebaeude", "saegewerk")],
            5: [("turm", 2, "wache"), ("gebaeude", "markt")],
            6: [("turm", 0, "kanone"), ("mauer",)],
            7: [("turm", 6, "wache")],
        }
        for welle in range(len(WELLEN)):
            for schritt in plan.get(welle, []):
                if schritt[0] == "turm":
                    s.baue_turm(schritt[1], schritt[2])
                elif schritt[0] == "gebaeude":
                    s.baue_gebaeude(schritt[1])
                else:
                    s.dorf_aktion({"haus": "baue_haus", "mauer": "baue_mauer"}[schritt[0]])
            for platz in sorted(s.tuerme):
                s.verbessere(platz)
            s.dorf_aktion("repariere_mauer")
            self.assertTrue(s.starte_welle())
            spiele_welle(s)
            self.assertNotEqual(
                s.phase, "welle", "Die Welle muss in endlicher Zeit abschließbar sein."
            )
            self.assertNotEqual(s.phase, "verloren", f"Strategie verliert in Welle {s.welle}.")
        self.assertEqual(s.phase, "sieg")
        self.assertGreater(s.dorf.leben, 0)
        self.assertLessEqual(s.besiegt, sum(len(w) for w in WELLEN))
        self.assertGreater(s.beute_gesamt, 0)
        vorher = s.dorf.vorraete.copy()
        s.schritt(10)
        self.assertEqual(
            s.dorf.vorraete, vorher, "Nach dem Sieg darf es kein wiederholtes Einkommen geben."
        )
        self.assertFalse(s.starte_welle())
        self.assertFalse(s.baue_turm(0, "pfeil"))

    def test_teil1_strategie_reicht_nicht_fuer_teil2(self):
        s = Spiel(modell)
        for platz in (1, 4, 7):
            s.baue_turm(platz, "pfeil")
        for _ in WELLEN:
            if s.phase != "bauen":
                break
            s.starte_welle()
            spiele_welle(s)
        self.assertEqual(s.phase, "verloren", "Teil 2 soll eine neue Strategie verlangen.")
        self.assertGreater(s.welle, TEIL1_WELLEN - 2, "Teil 1 bleibt mit drei Türmen machbar.")

    def test_ohne_tuerme_geht_das_dorf_verloren(self):
        s = Spiel(modell)
        for _ in WELLEN:
            s.starte_welle()
            spiele_welle(s)
            if s.phase == "verloren":
                break
        self.assertEqual(s.phase, "verloren")
        self.assertEqual(s.dorf.leben, 0)
        self.assertFalse(s.starte_welle())

    def test_basis_ist_ohne_zusatzaufgaben_spielbar(self):
        class BasisDorf(modell.Dorf):
            def sammle_einkommen(self):
                raise NotImplementedError("Zusatz 8")

        class BasisModell:
            Dorf = BasisDorf
            Gegner = modell.Gegner
            Pfeilturm = modell.Pfeilturm

        s = Spiel(BasisModell)
        BasisModell.sammle_beute = staticmethod(modell.sammle_beute)
        for platz in (1, 4, 7):
            s.baue_turm(platz, "pfeil")
        s.starte_welle()
        for _ in range(12000):
            s.schritt(0.05)
            if s.phase != "welle":
                break
        self.assertEqual(s.phase, "bauen")
        self.assertGreaterEqual(s.dorf.vorraete["gold"], 60)

    def test_besiegte_gegner_verursachen_keinen_dorfschaden(self):
        s = Spiel(modell)
        s.starte_welle()
        g = s.warteschlange.pop()
        g.fortschritt, g.leben = WEGLAENGE, 0
        s.gegner.append(g)
        vorher = s.dorf.vorraete["gold"]
        s.schritt(0.05)
        self.assertEqual(s.dorf.leben, 20)
        self.assertEqual(s.dorf.vorraete["gold"], vorher + 9)
        self.assertNotIn(g, s.gegner)

    def test_dorfschaden_kommt_aus_den_weltdaten(self):
        s = Spiel(modell)
        s.welle = 6  # Welle 7 enthält einen Troll.
        s.starte_welle()
        troll = next(g for g in s.warteschlange if g.art == "troll")
        s.warteschlange = []
        troll.fortschritt = WEGLAENGE
        s.gegner = [troll]
        s.schritt(0.05)
        self.assertEqual(s.dorf.leben, 16)

    def test_teil2_wellen_bauen_eigene_klassen(self):
        s = Spiel(modell)
        s.welle = TEIL1_WELLEN
        s.starte_welle()
        arten = {type(g).__name__ for g in s.warteschlange}
        self.assertEqual(arten, {"Gegner", "Schildork"})

    def test_offene_teil2_aufgabe_veraendert_nichts(self):
        class OffenerSchildork(modell.Schildork):
            def __init__(self, *args, **kwargs):
                raise NotImplementedError("Aufgabe 11: offen")

        werkstatt = SimpleNamespace(**vars(modell))
        werkstatt.Schildork = OffenerSchildork
        s = Spiel(werkstatt)
        s.welle = TEIL1_WELLEN
        with self.assertRaises(NotImplementedError):
            s.starte_welle()
        self.assertEqual((s.phase, s.welle, s.warteschlange), ("bauen", TEIL1_WELLEN, []))

    def test_beute_zeigt_gold_und_zaehlt(self):
        s = Spiel(modell)
        s.starte_welle()
        g = s.warteschlange.pop()
        g.leben = 0
        s.gegner.append(g)
        s.schritt(0.05)
        self.assertEqual((s.besiegt, s.beute_gesamt), (1, 9))
        self.assertEqual([a[2] for a in s.anzeigen], ["+9"])
        self.assertEqual(s.chronik.letzte(5), ["Ork"])
        for _ in range(40):
            s.schritt(0.05)
        self.assertEqual(s.anzeigen, [], "Die Goldanzeige verschwindet nach kurzer Zeit.")

    def test_gebaeude_nur_zwischen_wellen(self):
        s = Spiel(modell)
        self.assertTrue(s.baue_gebaeude("markt"))
        s.starte_welle()
        self.assertFalse(s.baue_gebaeude("saegewerk"))
        self.assertEqual([g.art for g in s.dorf.gebaeude], ["markt"])

    def test_spaeherbericht_nur_in_der_baupause(self):
        s = Spiel(modell)
        self.assertEqual(s.spaeherbericht(), {"ork": 5})
        s.starte_welle()
        self.assertIsNone(s.spaeherbericht())
        s.welle, s.phase = len(WELLEN), "sieg"
        self.assertIsNone(s.spaeherbericht())

    def test_turmbau_mit_holzkosten(self):
        s = Spiel(modell)
        s.dorf.vorraete["holz"] = 19
        self.assertFalse(s.baue_turm(0, "wache"))
        s.dorf.vorraete["holz"] = 20
        self.assertTrue(s.baue_turm(0, "wache"))
        self.assertEqual((s.dorf.vorraete["gold"], s.dorf.vorraete["holz"]), (105, 0))

    def test_offene_chronik_unterbricht_keine_welle(self):
        class OffeneChronik(modell.Chronik):
            def trage_ein(self, name):
                raise NotImplementedError("Aufgabe 15: offen")

        werkstatt = SimpleNamespace(**vars(modell))
        werkstatt.Chronik = OffeneChronik
        s = Spiel(werkstatt)
        s.starte_welle()
        g = s.warteschlange.pop()
        g.leben = 0
        s.gegner.append(g)
        s.schritt(0.05)
        self.assertEqual((s.phase, s.besiegt, s.chronik.eintraege), ("welle", 1, []))


class SpielstandTests(unittest.TestCase):
    def setUp(self):
        self.ordner = tempfile.TemporaryDirectory()
        self.pfad = os.path.join(self.ordner.name, "spielstand.json")

    def tearDown(self):
        self.ordner.cleanup()

    def test_speichern_und_laden(self):
        s = Spiel(modell)
        s.baue_turm(1, "pfeil")
        s.baue_turm(4, "frost")
        s.verbessere(1)
        s.baue_gebaeude("markt")
        s.dorf_aktion("baue_mauer")
        s.starte_welle()
        spiele_welle(s)
        self.assertTrue(s.speichere(self.pfad))
        neu = Spiel(modell)
        self.assertTrue(neu.lade(self.pfad))
        self.assertEqual(neu.spielstand(), s.spielstand())
        self.assertEqual(neu.tuerme[1].schaden, 18, "Gespeicherte Stufen wirken wieder.")
        self.assertEqual(neu.tuerme[4].reichweite, 110)
        self.assertIsInstance(neu.tuerme[4], modell.Frostturm)
        neu.starte_welle()
        self.assertEqual(neu.welle, 2)

    def test_speichern_nur_in_der_baupause(self):
        s = Spiel(modell)
        s.starte_welle()
        self.assertFalse(s.speichere(self.pfad))
        self.assertFalse(os.path.exists(self.pfad))

    def test_kaputte_datei_laesst_partie_unveraendert(self):
        s = Spiel(modell)
        s.baue_turm(1, "pfeil")
        vorher = s.spielstand()
        for inhalt in ("{kaputt", json.dumps({"version": 1, "welle": 99})):
            with self.subTest(inhalt=inhalt):
                with open(self.pfad, "w", encoding="utf-8") as datei:
                    datei.write(inhalt)
                self.assertFalse(s.lade(self.pfad))
                self.assertEqual(s.spielstand(), vorher)
                self.assertIn("Spielstand", s.hinweis)
        self.assertFalse(s.lade(os.path.join(self.ordner.name, "fehlt.json")))
        self.assertEqual(s.spielstand(), vorher)
