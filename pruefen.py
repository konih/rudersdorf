"""Freundlicher Teststarter, ausschließlich mit der Python-Standardbibliothek."""

import argparse
import os
import unittest


class LernErgebnis(unittest.TestResult):
    def startTest(self, test):
        super().startTest(test)
        print(f"\n{test.__class__.__name__} · {test._testMethodName[8:].replace('_', ' ')}")

    def addSuccess(self, test):
        super().addSuccess(test)
        print("  ✓ Das klappt!")

    def addFailure(self, test, err):
        super().addFailure(test, err)
        print(f"  → Noch ein Schritt: {err[1]}")

    def addError(self, test, err):
        super().addError(test, err)
        if isinstance(err[1], NotImplementedError):
            print(f"  ○ Noch offen: {err[1]}")
        else:
            print(f"  → Python meldet {err[0].__name__}: {err[1]}")
            print("    Schau dir die Fehlerstelle an:")
            print(self.errors[-1][1])

    def addSubTest(self, test, subtest, err):
        super().addSubTest(test, subtest, err)
        if err:
            print(f"  → Prüfe {subtest}: {err[1]}")


def main():
    parser = argparse.ArgumentParser(description="Dein Trainingsplatz für Rudersdorf")
    parser.add_argument(
        "aufgabe",
        nargs="?",
        type=int,
        choices=range(1, 18),
        metavar="AUFGABE",
        help="Aufgabennummer 1 bis 17 (Standard: 1)",
    )
    parser.add_argument("--alle", action="store_true", help="alle Aufgaben 1 bis 17 prüfen")
    parser.add_argument("--basis", action="store_true", help="Grundaufgaben 1 bis 6 prüfen")
    parser.add_argument("--teil1", action="store_true", help="Teil 1: Aufgaben 1 bis 9 prüfen")
    parser.add_argument("--teil2", action="store_true", help="Teil 2: Aufgaben 10 bis 17 prüfen")
    parser.add_argument("--loesung", action="store_true", help="ausdrücklich die Referenz prüfen")
    args = parser.parse_args()
    auswahl = [args.aufgabe is not None, args.alle, args.basis, args.teil1, args.teil2]
    if sum(auswahl) > 1:
        parser.error("Wähle eine Aufgabennummer ODER --alle, --basis, --teil1 oder --teil2.")
    os.environ["RUDERSDORF_LOESUNG"] = "1" if args.loesung else "0"
    from tests import test_aufgaben, test_aufgaben2

    if args.alle:
        nummern = range(1, 18)
    elif args.basis:
        nummern = range(1, 7)
    elif args.teil1:
        nummern = range(1, 10)
    elif args.teil2:
        nummern = range(10, 18)
    else:
        nummern = [args.aufgabe or 1]
    suite = unittest.TestSuite(
        unittest.defaultTestLoader.loadTestsFromTestCase(
            getattr(test_aufgaben if n < 10 else test_aufgaben2, f"Aufgabe{n:02}")
        )
        for n in nummern
    )
    print("RUDERSDORF · " + ("Referenzlösung" if args.loesung else "Deine Werkstatt"))
    ergebnis = LernErgebnis()
    suite.run(ergebnis)
    print(f"\n{ergebnis.testsRun} Tests ausgeführt.")
    if ergebnis.wasSuccessful():
        print("Alles grün! Gut gemacht, Luki. Probiere deinen Fortschritt im Spiel aus.")
    else:
        print(
            "Noch nicht alles grün — genau dafür sind die Tests da. Nimm dir einen Hinweis nach dem anderen vor."
        )
    return 0 if ergebnis.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main())
