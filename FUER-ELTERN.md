# Für Eltern und Mitlernende

## Erst neugierig machen, dann programmieren

Eine kurze Partie der Referenz (`python spielen.py --loesung`) zeigt, wofür Luki
programmiert. Danach zurück zu seiner Werkstatt, also **ohne** `--loesung`.
Die Referenz liegt auf Wunsch direkt im Repository; sie ist ein Vergleich, kein
Zugriffsschutz und kein Geheimnis.

Lieber eine Mission mit verstandenem grünem Test als alle Missionen abgeschrieben.
Die sechs Grundaufgaben sind der Kern; 7–9 sind getestete Zusatzaufgaben.
Die freien Ideen in `KNOBELAUFGABEN.md` sind offen und haben keine Musterlösung.
Es gibt keinen Zeitplan, den Luki einhalten muss.

Hilfreiche Fragen:

- „Was soll diese Methode zurückgeben, und wer braucht diesen Wert?“
- „Kannst du den Zustand vor und nach einem Aufruf auf Papier aufmalen?“
- „Welcher Test ist schon grün? Welcher ungewöhnliche Fall fehlt noch?“
- „Was gehört diesem einen Ork, was gehört dem Dorf?“
- „Welche Zeilen kann der Frostturm erben, welche braucht er selbst?“

## Warum die Oberfläche vorbereitet ist

Fensterschleifen, Koordinaten und Klickereignisse würden die Wiederholung von
Klassen, Listen und Dictionaries überlagern. Deshalb bleibt Lukis Einstieg bei
`modell.py`. Der Rahmen benutzt seine Methoden unmittelbar; es gibt keine heimliche
Ersatzimplementierung für unvollständige Grundaufgaben.

Das Fenster öffnet schon beim ungelösten Stand. Ein Platzhalter führt zu einer
Aufgabenmeldung. Ein echter Python-Fehler stoppt die Simulation, zeigt eine Meldung
und bleibt zusätzlich im Terminal nachvollziehbar. Nach Codeänderungen neu starten.
Der erste sichtbare Fortschritt einer Methode lässt sich am einfachsten im Test sehen;
eine vollständige Partie setzt alle sechs Grundaufgaben voraus.

## Testkonzept

46 Lerntests prüfen die neun Aufgaben mit denselben Eingaben und Erwartungen,
unabhängig davon, ob Werkstatt oder Referenz geladen ist. Tests prüfen Verhalten,
keine vorgeschriebene Schleifenform oder Quelltextfragmente. Alternative richtige
Lösungen sollen ebenso bestehen.

Die Abhängigkeiten sind absichtlich klein: Aufgabe 2 baut ihre Test-Orks unabhängig
vom noch unfertigen Konstruktor auf. Zielwahl und Beute nutzen die Schadensregeln;
Ausbauten nutzen die Dorfkasse. Das steht in der Aufgabenbeschreibung.

Zusätzliche Techniktests prüfen Wegberechnung, Pause, Käufe, Mauer, Frost,
Endzustände, Grundspiel ohne Zusatzeinkommen sowie echte Tkinter-Klicks.
Sie verwenden die Referenz für den Rahmen. Diese Tests bewerten also nicht Lukis
unfertige Grundaufgaben. Unter Linux ohne Display werden die Fenstertests übersprungen.

### Prüfung ohne Fenster

```sh
python pruefen.py --alle --loesung
python -m unittest tests.test_spielkern -v
```

### Gesamte Referenz einschließlich Fenster prüfen

Linux mit virtuellem Display:

```sh
sudo apt install python3-tk xvfb
RUDERSDORF_LOESUNG=1 xvfb-run -a /usr/bin/python3 -m unittest discover -v
```

Auf einem Desktop (PowerShell):

```powershell
$env:RUDERSDORF_LOESUNG = "1"
python -m unittest discover -v
Remove-Item Env:RUDERSDORF_LOESUNG
```

Auf macOS/Linux mit grafischer Sitzung:

```sh
RUDERSDORF_LOESUNG=1 python3 -m unittest discover -v
```

Die Umgebungsvariable wird nur für direkte `unittest`-Aufrufe benötigt.
Der Lernstarter `pruefen.py` setzt die Auswahl immer selbst nach `--loesung`.
Ein nacktes `python -m unittest discover` testet absichtlich auch die ungelösten
Grundaufgaben und wird am Anfang fehlschlagen. Für Luki deshalb `pruefen.py` verwenden.

### Automatische Prüfung auf GitHub

Der Workflow prüft die Referenz unter Python 3.10, 3.12 und 3.14, den Spielkern,
unter Linux echte Tkinter-Fenster im virtuellen Display und mit Ruff Format/Stil.
Die unfertigen Aufgaben sind **kein** Grund für dauerhaft rote CI: Geprüft wird
hier die mitgelieferte Referenz. Lukis Fortschritt zeigt sein eigener Teststarter.
Der CI-Status allein sagt daher ausdrücklich nicht, dass seine Aufgaben gelöst sind.

Ruff ist nur ein optionales Entwicklungswerkzeug, keine Voraussetzung fürs Spielen.
Für Wartung: `python -m pip install ruff==0.16.6`, dann `ruff check .` und
`ruff format --check .`. `hypot` ist im unfertigen Modell absichtlich bereits importiert.

## Ein Einstieg in die Spielstrategie

Drei Pfeiltürme auf den Plätzen nahe den engen Wegkurven sind ein guter Anfang.
Vor der nächsten Welle kannst du wählen: mehr Feuerkraft, ein Haus für späteres
Einkommen oder eine Mauer als Reserve. Eine vollständige Gewinnstrategie mit
Upgrades wird auch vom Techniktest simuliert; das Spiel ist also gewinnbar.
Verlieren ohne Verteidigung wird ebenfalls geprüft.

## Wenn etwas schiefgeht

- **„No module named tkinter“:** Installation und Python-Auswahl in README prüfen.
- **„can't open display“:** Spiel braucht einen Desktop; Tests funktionieren ohne Fenster.
- **„Noch offen“:** Der Platzhalter der genannten Methode ist noch vorhanden.
- **`AttributeError`:** Oft fehlt ein Konstruktorattribut oder `super().__init__`.
- **`None` statt `True`:** Vielleicht fehlt ein `return`.
- **Gold verschwindet ohne Gebäude:** Wahrscheinlich wird schon während der Prüfung abgebucht.
- **Orks werden übersprungen:** Vielleicht wird eine Liste beim Durchlaufen verändert.
- **Änderung wirkt nicht:** Datei speichern und Spielprozess neu starten. `R` setzt nur die Partie zurück.
