"""Techniktests: Sie prüfen den vorbereiteten Rahmen mit der Referenzlösung."""

import unittest

from loesung import modell
from spielkern import WEGLAENGE, Spiel, weg_position
from welt import WEG, WELLEN


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
        for platz in (1, 4, 7):
            s.baue_turm(platz, "pfeil")
        for _ in WELLEN:
            for platz in list(s.tuerme):
                s.verbessere(platz)
            s.dorf_aktion("baue_mauer")
            s.starte_welle()
            for _ in range(12000):
                s.schritt(0.05)
                if s.phase != "welle":
                    break
            self.assertNotEqual(
                s.phase, "welle", "Die Welle muss in endlicher Zeit abschließbar sein."
            )
        self.assertEqual(s.phase, "sieg")
        self.assertGreater(s.dorf.leben, 0)
        vorher = s.dorf.vorraete.copy()
        s.schritt(10)
        self.assertEqual(
            s.dorf.vorraete, vorher, "Nach dem Sieg darf es kein wiederholtes Einkommen geben."
        )
        self.assertFalse(s.starte_welle())
        self.assertFalse(s.baue_turm(0, "pfeil"))

    def test_ohne_tuerme_geht_das_dorf_verloren(self):
        s = Spiel(modell)
        for _ in WELLEN:
            s.starte_welle()
            for _ in range(12000):
                s.schritt(0.05)
                if s.phase != "welle":
                    break
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
