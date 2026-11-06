# Rudersdorf · Die Orks kommen!

**Lukis Python-Werkstatt:** Verteidige ein kleines mittelalterliches Dorf gegen Orks,
Wolfsreiter und Oger. Baue Türme, schütze deine Nachbarn und lass Rudersdorf wachsen.
Du programmierst die Spielregeln — die grafische Welt ist schon vorbereitet.

![Rudersdorf mit Fachwerkhäusern, Orks und Verteidigungstürmen](docs/vorschau.png)

## Los geht's

Du brauchst **Python 3.10 oder neuer mit Tkinter**. Keine zusätzlichen Python-Pakete,
kein Konto und keine Internetverbindung zum Spielen oder Testen.
Das Fenster ist 1180 × 760 Pixel groß; plane zusätzlich Platz für die Fensterleiste ein.

1. Lade dieses Repository über **Code → Download ZIP** herunter und entpacke es,
   oder klone es mit `git clone https://github.com/konih/rudersdorf.git`.
2. Öffne den Ordner `rudersdorf` im Editor und ein Terminal **in diesem Ordner**.
3. Prüfe Python und Tkinter: `python -m tkinter`. Ein kleines Testfenster sollte erscheinen.
4. Starte deine Werkstatt:

   ```sh
   python spielen.py
   ```

5. Öffne [AUFGABEN.md](AUFGABEN.md) und löse Aufgabe 1 in **[modell.py](modell.py)**.
6. Teste nur diese Aufgabe:

   ```sh
   python pruefen.py 1
   ```

> Je nach Installation heißt der Befehl `python3` oder unter Windows `py`.
> Ersetze dann `python` in **allen** Befehlen entsprechend.
> Wenn mehrere Python-Versionen installiert sind, verwende für Spiel und Tests dieselbe.

**Teil 2 ist da!** Wer die Missionen 1–9 gelöst hat, macht in
[AUFGABEN-TEIL2.md](AUFGABEN-TEIL2.md) weiter: Schildorks, Trolle, ein vierter Turm,
Gebäude, eine Chronik aus Listen und Speicherstände. Teil 2 arbeitet in **`modell2.py`**,
das deine Lösungen aus `modell.py` importiert und erweitert. `modell.py` bleibt unverändert.

**Wichtig:** Die Werkstatt ist absichtlich ungelöst. Du siehst das Dorf sofort,
aber Aktionen können auf eine noch offene Aufgabe hinweisen. Erst nach den
Grundaufgaben 1–6 läuft eine vollständige Partie. Die Referenz wird niemals
unbemerkt geladen und deine Aufgaben werden niemals automatisch übersprungen.

### Tkinter fehlt?

- **Windows:** Installiere Python von [python.org](https://www.python.org/downloads/).
  Die Installationskomponente „Tcl/Tk and IDLE“ muss enthalten sein.
- **macOS:** Die Python-Installation von [python.org](https://www.python.org/downloads/macos/)
  bringt Tkinter mit. Prüfe anschließend `python3 -m tkinter`.
- **Ubuntu/Debian:** `sudo apt install python3-tk`, anschließend
  `/usr/bin/python3 -m tkinter`. Verwende dann auch für das Spiel `/usr/bin/python3`.
  Ein separat installiertes Python (etwa Homebrew) verwendet dieses Tkinter nicht automatisch.
- **Kein Bildschirm / Online-Editor:** Die Unit-Tests brauchen kein Fenster.
  Das Spiel braucht einen grafischen Desktop; ein Terminal allein reicht nicht.

## Spielen

- **1 / 2 / 3 / 4:** Pfeil-, Frost-, Kanonenturm oder Wachtmeister (Teil 2) auswählen.
- **Klick auf einen runden Bauplatz:** Turm kaufen und bauen. Der Preis wird oben rechts angezeigt.
- **N oder „Nächste Welle“:** Den nächsten Angriff starten. Wellen starten nie von selbst.
- **Leertaste:** Angriff pausieren/fortsetzen; zwischen Wellen die nächste starten.
- **Klick auf einen gebauten Turm:** Reichweite und Werte sehen, ihn für ein Upgrade auswählen.
- **F:** Spieltempo zwischen 1× und 2× umschalten.
- **S / L:** In einer Baupause speichern bzw. laden (Teil 2, Aufgaben 16–17).
- **Dorf-Schaltflächen:** Zwischen Wellen Mauer bauen, reparieren oder Häuser ergänzen.
  Diese Aktionen gehören zu den Zusatzaufgaben 7–9; Sägewerk, Steinbruch und Markt zu Aufgabe 14.
- **R:** Neue Partie beginnen, auch nach Sieg oder Niederlage. Verwirft den aktuellen Spielstand.
- **Esc:** Einen Aufgabenhinweis schließen. Nach Codeänderungen das Fenster schließen und neu starten.

**Ziel:** Überstehe alle zehn Wellen mit mindestens einem Dorf-Lebenspunkt.
Welle 1–5 bilden Teil 1; ab Welle 6 kommen Schildorks und Trolle, und die Gegner werden
mit jeder Welle zäher. Für Welle 6–10 brauchst du deshalb die Missionen aus Teil 2.
Ein durchgebrochener Ork oder Wolfsreiter verursacht 1 Schaden, ein Schildork 2,
ein Oger 3 und ein Troll 4 (`dorfschaden` in `welt.MONSTER`).
Eine vorhandene Stadtmauer fängt Schaden zuerst ab.
Besiegte Gegner geben Gold. Zwischen Wellen erhältst du Grundversorgung:
35 Gold, 15 Holz und 10 Stein. Mit Zusatzaufgabe 8 kommt das Einkommen des Dorfes hinzu.
Nach der letzten Welle ist das Spiel gewonnen; danach gibt es kein weiteres Einkommen.

## Dein Lernpfad

| Mission | Schwerpunkt | Testbefehl |
| --- | --- | --- |
| 1 · Die Orks bekommen Namen | Klassen, `__init__`, `self` | `python pruefen.py 1` |
| 2 · Treffer! | Methoden, Bedingungen, Grenzfälle | `python pruefen.py 2` |
| 3 · Die Dorfkasse | Dictionaries, faire Bezahlung | `python pruefen.py 3` |
| 4 · Wen beschießen wir? | Listen, Schleifen, Zielauswahl | `python pruefen.py 4` |
| 5 · Eis und Donner | Vererbung, `super()`, Überschreiben | `python pruefen.py 5` |
| 6 · Nach dem Kampf | Neue Listen, Belohnungen | `python pruefen.py 6` |
| 7 · Die Stadtmauer | Zusatz: Ausbau, Reparatur, Grenzen | `python pruefen.py 7` |
| 8 · Neue Nachbarn | Zusatz: Häuser und Einkommen | `python pruefen.py 8` |
| 9 · Die Turmschmiede | Zusatz: Upgrades und Vererbung | `python pruefen.py 9` |
| **Teil 2** · [AUFGABEN-TEIL2.md](AUFGABEN-TEIL2.md) | in `modell2.py` | |
| 10 · Der Späherbericht | Dictionary als Zähler | `python pruefen.py 10` |
| 11 · Der Schildork | Überschreiben mit `super()` | `python pruefen.py 11` |
| 12 · Der Troll | `super()` und Reihenfolge | `python pruefen.py 12` |
| 13 · Der Wachtmeister | Neue Turmart, eigene Zielwahl | `python pruefen.py 13` |
| 14 · Sägewerk, Steinbruch, Markt | Objekte in Listen, Kopien | `python pruefen.py 14` |
| 15 · Die Chronik | Listen: anhängen, ausschneiden, zählen | `python pruefen.py 15` |
| 16 · Der Dorfschreiber | Zusatz: Spielstand für JSON | `python pruefen.py 16` |
| 17 · Die Siegelprüfung | Zusatz: Daten prüfen | `python pruefen.py 17` |

`python pruefen.py --basis` prüft 1–6, `--teil1` prüft 1–9, `--teil2` prüft 10–17
und `--alle` prüft alles.
Ohne Argument beginnt der Teststarter bei Aufgabe 1. Fehlende Aufgaben und falsche
Ergebnisse führen bewusst zu Exitcode 1; alles richtig ergibt Exitcode 0.
Die Tests nennen Erwartung, tatsächliches Ergebnis und einen Hinweis.
Ein echter Python-Fehler zeigt zusätzlich die Fehlerstelle.

## Referenzlösung — erst selbst tüfteln!

Die vollständige Lösung liegt getrennt in **[loesung/](loesung/)**.
Sie verwendet dieselbe Oberfläche und dieselben Tests:

```sh
python spielen.py --loesung
python pruefen.py --alle --loesung
```

Deine `modell.py` wird dadurch weder verändert noch ersetzt. Auch ein versehentlich
gesetzter Umgebungswert schaltet `pruefen.py` nicht auf die Referenz um: Nur
`--loesung` tut das. Zum Vergleichen öffne beide Dateien nebeneinander, möglichst
erst nach einem eigenen Versuch.

## Wo finde ich was?

| Datei | Zweck |
| --- | --- |
| `modell.py` | **Deine Baustelle Teil 1:** Aufgaben 1–9 |
| `modell2.py` | **Deine Baustelle Teil 2:** Aufgaben 10–17, baut auf `modell.py` auf |
| `AUFGABEN.md` | Ausführliche Missionen mit Verträgen, Beispielen und gestuften Hinweisen |
| `AUFGABEN-TEIL2.md` | Die Missionen von Teil 2 |
| `KNOBELAUFGABEN.md` | Freie Erweiterungen mit Ideen für eigene Tests |
| `welt.py` | Karte, Bauplätze, Baupläne, Gegnerdaten, Gebäude, Wellen und Wellenstärke |
| `spielkern.py` | Vorbereitete Spielschleife, ohne Tkinter testbar |
| `oberflaeche.py` | Vorbereitete Zeichnungen, Animationen und Bedienung |
| `pruefen.py`, `tests/` | Lernfeedback und Techniktests |
| `loesung/modell.py`, `loesung/modell2.py` | Vollständig gelöste Aufgaben 1–9 und 10–17 |
| `FUER-ELTERN.md` | Lernbegleitung und technische Prüfung |
| `ERWEITERN.md` | Wegweiser für weitere Gebäude, Berufe und Spielideen |

Alle Grafiken werden mit Tkinter gezeichnet. Keine externen Bilddateien nötig.
Die Karte ist bewusst kompakt, der Schwierigkeitsgrad ein Einstieg, kein fertiges
kommerzielles Strategiespiel. Speichern gibt es ab Aufgabe 16, Sounds noch nicht.
Auf der Karte werden maximal acht Häuser und zwanzig Bewohner gezeichnet;
die Zähler und die Wirtschaft wachsen darüber hinaus weiter.

Lizenz: [MIT](LICENSE).
