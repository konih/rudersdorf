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
        from loesung import modell
        from oberflaeche import Fenster

        f = Fenster(self.wurzel, modell, True)
        self.wurzel.update()
        self.klick(f, 265, 270)
        self.assertEqual(len(f.spiel.tuerme), 1)
        self.klick(f, 950, 420)  # Stadtmauer.
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
        import modell
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
