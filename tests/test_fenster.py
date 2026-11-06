"""Echte Fenster-Interaktion; auf Rechnern ohne Display automatisch übersprungen."""

import os
import sys
import unittest
from types import SimpleNamespace


@unittest.skipUnless(
    os.environ.get("DISPLAY") or sys.platform in ("win32", "darwin"),
    "Fenstertest braucht ein Display (Linux: xvfb-run).",
)
class FensterTests(unittest.TestCase):
    def setUp(self):
        import tkinter as tk

        self.wurzel = tk.Tk()
        self.fehler = []
        self.wurzel.report_callback_exception = lambda *args: self.fehler.append(args)

    def tearDown(self):
        self.wurzel.destroy()

    def klick(self, fenster, x, y):
        fenster.bild.event_generate("<Button-1>", x=x, y=y)
        self.wurzel.update()
        fenster.zeichne()

    def test_bauen_welle_pause_und_neustart(self):
        from loesung import modell2 as modell
        from oberflaeche import Fenster

        f = Fenster(self.wurzel, modell, True)
        self.wurzel.update()
        self.klick(f, 265, 270)
        self.assertEqual(len(f.spiel.tuerme), 1)
        self.klick(f, 950, 290)  # Stadtmauer.
        self.assertEqual(f.spiel.dorf.mauer, 5)
        self.klick(f, 950, 700)  # Welle.
        self.assertEqual(f.spiel.phase, "welle")
        for _ in range(40):
            f.spiel.schritt(0.05)
        f.zeichne()
        self.klick(f, 950, 700)  # Pause.
        self.assertTrue(f.spiel.pause)
        f.neustart()
        f.zeichne()
        self.assertEqual(f.spiel.welle, 0)
        self.assertEqual(f.spiel.tuerme, {})
        self.assertFalse(self.fehler)
        self.assertIsNone(f.fehler)

    def test_werkstatt_zeigt_offene_aufgabe(self):
        import modell2 as modell
        from oberflaeche import Fenster

        # Diese offene Aufgabe bleibt eine Test-Fixture, auch wenn Luki seine löst.
        class OffenerGegner(modell.Gegner):
            def __init__(self, *args, **kwargs):
                raise NotImplementedError("Aufgabe 1: Gib dem Gegner seine Eigenschaften.")

        werkstatt = SimpleNamespace(**vars(modell))
        werkstatt.Gegner = OffenerGegner
        f = Fenster(self.wurzel, werkstatt)
        self.wurzel.update()
        self.klick(f, 950, 700)
        self.assertIn("Aufgabe 1", f.fehler)
        self.assertEqual(f.spiel.welle, 0)
        self.assertEqual(f.spiel.phase, "bauen")
        self.assertFalse(self.fehler)
        self.assertEqual(f.spiel.dorf.vorraete["gold"], 160)

    def test_teil2_knoepfe_und_anzeigen(self):
        from loesung import modell2 as modell
        from oberflaeche import Fenster

        f = Fenster(self.wurzel, modell, True)
        self.wurzel.update()
        self.klick(f, 1060, 190)  # Wachtmeister wählen.
        self.assertEqual(f.auswahl, "wache")
        self.klick(f, 265, 270)
        self.assertEqual(type(f.spiel.tuerme[1]).__name__, "Wachtmeister")
        self.klick(f, 1060, 350)  # Sägewerk.
        self.assertEqual([g.art for g in f.spiel.dorf.gebaeude], ["saegewerk"])
        self.assertIn("5× Ork", f.spaehertext())
        self.klick(f, 265, 270)  # Turm markieren zeigt seine Werte.
        self.assertEqual(f.markiert, 1)
        f.schalte_tempo()
        self.assertEqual(f.tempo, 2)
        self.assertFalse(self.fehler)
        self.assertIsNone(f.fehler)

    def test_offene_teil2_anzeigen_stuerzen_nicht_ab(self):
        import modell2 as modell
        from oberflaeche import Fenster

        werkstatt = SimpleNamespace(**vars(modell))
        werkstatt.spaeherbericht = lambda welle: (_ for _ in ()).throw(
            NotImplementedError("Aufgabe 10")
        )
        f = Fenster(self.wurzel, werkstatt)
        self.wurzel.update()
        f.zeichne()
        self.assertIn("Aufgabe 10", f.spaehertext())
        self.assertFalse(self.fehler)
