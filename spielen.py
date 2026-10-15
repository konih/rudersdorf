"""Start: python spielen.py; Referenz ausdrücklich mit --loesung auswählen."""

import argparse
import importlib


def main():
    parser = argparse.ArgumentParser(description="Verteidige Rudersdorf gegen die Orks!")
    parser.add_argument(
        "--loesung", action="store_true", help="die fertige Referenz aus loesung/ spielen"
    )
    args = parser.parse_args()
    try:
        import tkinter as tk

        from oberflaeche import Fenster
    except ImportError:
        parser.exit(
            1, "Tkinter fehlt in diesem Python. Hinweise zur Installation stehen in README.md.\n"
        )
    try:
        wurzel = tk.Tk()
    except tk.TclError as fehler:
        parser.exit(
            1,
            f"Das Fenster konnte nicht geöffnet werden: {fehler}\nStarte das Spiel auf einem Computer mit grafischer Oberfläche.\n",
        )
    modell = importlib.import_module("loesung.modell" if args.loesung else "modell")
    Fenster(wurzel, modell, args.loesung)
    wurzel.mainloop()


if __name__ == "__main__":
    main()
