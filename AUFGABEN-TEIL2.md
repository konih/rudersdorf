# Teil 2 · Der Orkkönig erwacht

Luki, du hast Rudersdorf gerettet! Fünf Wellen lang hielten deine Türme stand.
Doch in der Nacht kommt ein Späher atemlos ins Dorf gerannt:
**„Der Orkkönig hat seine Truppen gesammelt! Orks mit Eisenschilden. Trolle, deren
Wunden sich von selbst schließen. Und jede Welle stärker als die letzte!“**

Die Schmiedin legt einen neuen Plan auf den Tisch. Die Dorfälteste öffnet ein
leeres Buch. Und die Wache fragt: **„Bringst du uns das Kämpfen noch einmal bei?“**

## So ist Teil 2 aufgebaut

Du arbeitest jetzt in **[modell2.py](modell2.py)**. Diese Datei baut auf deinem
`modell.py` aus Teil 1 auf: Sie importiert deine Klassen und **erweitert** sie.
Deshalb musst du `modell.py` nicht verändern. Deine gelösten Aufgaben bleiben, wie sie sind.

```sh
python pruefen.py 10      # eine Aufgabe prüfen
python pruefen.py --teil2 # alle Aufgaben 10 bis 17
python spielen.py         # spielen: Welle 6 bis 10 brauchen Teil 2
```

Das Spiel hat jetzt **zehn Wellen**. Welle 1 bis 5 kennst du schon. Ab Welle 6
schickt der Orkkönig neue Gegner, und ihre Lebenspunkte werden mit jeder Welle
mit einem Faktor aus `welt.WELLEN_STAERKE` multipliziert. Mit drei Pfeiltürmen
gewinnst du Teil 2 nicht mehr. Du brauchst die neuen Werkzeuge aus diesen Missionen.

Das Wichtigste in Teil 2 ist die **Vererbung mit `super()`**. Du hast sie in Mission 5
schon benutzt: `super().__init__(x, y)` ruft den Konstruktor der Elternklasse auf.
Jetzt rufst du so auch **normale Methoden** der Elternklasse auf und erweiterst sie:

```python
class Elternklasse:
    def sag_hallo(self):
        print("Hallo")


class Kind(Elternklasse):
    def sag_hallo(self):
        super().sag_hallo()  # erst das Verhalten der Eltern ...
        print("... und tschüss")  # ... dann das, was das Kind zusätzlich kann
```

### Mini-Spickzettel für Teil 2

- **`super().methode(...)`:** ruft die Methode der Elternklasse auf, auch wenn du sie überschrieben hast.
- **`dictionary.get(schluessel, 0)`:** liefert 0, falls der Schlüssel fehlt.
- **`liste.append(x)`:** hängt `x` hinten an.
- **`liste[-3:]`:** die letzten drei Elemente. **`liste[::-1]`:** die Liste rückwärts (als neue Liste).
- **`x in liste`:** `True`, wenn `x` in der Liste vorkommt.
- **`dict(original)`:** eine Kopie eines Dictionaries. Änderungen an der Kopie verändern das Original nicht.
- **`isinstance(wert, dict)`:** prüft, ob ein Wert ein Dictionary ist.

| Mission | Schwerpunkt | Im Spiel |
| --- | --- | --- |
| 10 · Der Späherbericht | Dictionary zum Zählen | Vorschau auf die nächste Welle |
| 11 · Der Schildork | Methode überschreiben, `super()` | Gegner ab Welle 6 |
| 12 · Der Troll | Reihenfolge mit `super()` | Gegner ab Welle 7 |
| 13 · Der Wachtmeister | Neue Turmart | Taste 4 |
| 14 · Sägewerk, Steinbruch, Markt | Klassen arbeiten zusammen | Dorfknöpfe |
| 15 · Die Chronik | **Listen** | „Zuletzt besiegt“ |
| 16 · Zusatz: Der Dorfschreiber | Daten für JSON aufschreiben | Taste S speichert |
| 17 · Zusatz: Die Siegelprüfung | Daten gründlich prüfen | Taste L lädt |

---

## 10 · Der Späherbericht

**Du änderst:** die Funktion `spaeherbericht(welle)`.
**Du übst:** ein Dictionary als Zähler.

Vor jeder Welle schleicht ein Späher in den Flüsterwald und zählt die Gegner.
`welle` ist eine Liste von Gegnerarten, zum Beispiel `["ork", "wolf", "ork"]`.
Gib ein **neues** Dictionary zurück, das jede Art auf ihre Anzahl abbildet:

```python
spaeherbericht(["ork", "wolf", "ork", "oger", "ork"])
# → {"ork": 3, "wolf": 1, "oger": 1}
```

- Die Arten stehen in der Reihenfolge, in der der Späher sie **zuerst** sieht.
  Ein Dictionary merkt sich die Reihenfolge, in der Schlüssel eingefügt wurden: Sortiere nicht.
- Eine leere Welle ergibt `{}`.
- Die übergebene Liste bleibt unverändert.
- Jeder Aufruf beginnt mit einem neuen, leeren Dictionary.

**Fertig, wenn:** `python pruefen.py 10` grün ist. In der Baupause zeigt die
Seitenleiste unter „SPÄHER MELDEN“, wer als Nächstes kommt.

<details><summary>Hinweis 1</summary>
Lege vor der Schleife ein leeres Dictionary an. Gehe dann jede Art durch.
Ist die Art schon im Dictionary, erhöhe ihren Wert. Sonst beginnt sie bei 1.
</details>
<details><summary>Hinweis 2</summary>
Mit `bericht.get(art, 0)` bekommst du den bisherigen Zählerstand oder 0.
Daraus wird in einer einzigen Zeile „bisheriger Stand plus 1“.
</details>

**Denkfrage:** Warum wäre ein Dictionary, das **außerhalb** der Funktion angelegt wird,
nach der zweiten Welle falsch?

---

## 11 · Der Schildork

**Du änderst:** `Schildork.__init__` und `Schildork.erleide_schaden`.
**Du übst:** eine geerbte Methode überschreiben und mit `super()` wiederverwenden.

Ein Schildork **ist ein** Gegner: Er hat Name, Leben, Tempo und alles andere wie in
Mission 1. Zusätzlich trägt er einen Eisenschild.

**Konstruktor:** Reiche alle vier Parameter an `super().__init__(...)` weiter.
Setze danach `self.ruestung = 4`.

**Treffer:** Der Schild fängt pro Treffer `self.ruestung` Punkte ab.

1. Schaden von 0 oder weniger ist kein Treffer: nichts passiert, auch keine Heilung.
2. Sonst ist der wirksame Schaden `schaden - self.ruestung`, **aber mindestens 1**.
   Ein echter Treffer kratzt immer ein bisschen.
3. Den wirksamen Schaden gibst du an `super().erleide_schaden(...)` weiter.
   Die Methode aus Mission 2 kennt schon die Regel „nicht unter 0“.

| Treffer | Rüstung | wirksam | Leben vorher → nachher |
| --- | --- | --- | --- |
| 12 | 4 | 8 | 60 → 52 |
| 4 | 4 | 1 | 60 → 59 |
| 1 | 4 | 1 | 60 → 59 |
| 0 | 4 | 0 | 60 → 60 |
| -7 | 4 | 0 | 60 → 60 |
| 50 | 4 | 46 | 3 → 0 |

`ist_besiegt` und `bewege` erbt der Schildork einfach. Die schreibst du nicht neu.

**Fertig, wenn:** `python pruefen.py 11` grün ist. Jetzt kann Welle 6 beginnen.

<details><summary>Hinweis 1</summary>
Prüfe zuerst den Fall „kein Treffer“ und beende die Methode dort mit `return`.
</details>
<details><summary>Hinweis 2</summary>
`max(1, schaden - self.ruestung)` ist nie kleiner als 1.
</details>

**Denkfrage:** Welcher deiner Türme ist gegen Schildorks am schwächsten, und warum?
Rechne nach: Frostturm (5 Schaden) gegen Kanonenturm (18 Schaden).

---

## 12 · Der Troll

**Du änderst:** `Troll.__init__` und `Troll.bewege`.
**Du übst:** eine geerbte Methode erweitern und auf die Reihenfolge achten.

Trolle sind langsam, aber ihre Wunden schließen sich, während sie wandern.

**Konstruktor:** Wie beim Schildork. Setze danach `self.heilung = 8`
(Lebenspunkte pro Sekunde).

**Bewegen:**

1. Der Troll läuft wie jeder Gegner: Rufe `super().bewege(sekunden)` auf.
2. Danach heilt er `self.heilung * sekunden` Lebenspunkte.
3. Er heilt nie über `max_leben` hinaus.
4. Ein besiegter Troll bleibt besiegt: Er heilt nicht.
5. Negative Zeit bewegt nicht und heilt nicht.
6. **Frost stoppt die Heilung:** Ist der Troll **zu Beginn** des Schritts gefroren
   (`frost_rest > 0`), heilt er in diesem Schritt gar nicht.

**Die Falle bei Regel 6:** `super().bewege` verringert `frost_rest`. Wenn du erst
danach nachschaust, ist der Frost vielleicht schon weg. Merke dir deshalb **vorher**
in einer Variablen, ob er gefroren war.

**Beispiel:** Ein Troll mit 100 von 170 Leben läuft eine Sekunde: danach 108.
Nach einer halben Sekunde wären es 104. Mit 168 Leben und zwei Sekunden: 170, nicht 184.

**Fertig, wenn:** `python pruefen.py 12` grün ist. Im Spiel funkelt ein grünes
Plus über einem Troll, der sich gerade heilt.

<details><summary>Hinweis</summary>
<code>war_gefroren = self.frost_rest > 0</code> muss vor <code>super().bewege(sekunden)</code> stehen.
Begrenzen kannst du mit <code>min(self.max_leben, ...)</code>.
</details>

**Denkfrage:** Warum ist ein Frostturm neben einem Troll plötzlich doppelt nützlich?

---

## 13 · Der Wachtmeister

**Du änderst:** `Wachtmeister.__init__` und `Wachtmeister.waehle_ziel`.
**Du übst:** eine neue Unterklasse mit eigener Strategie.

Der alte Wachtmeister hat ein scharfes Auge für angeschlagene Gegner. Er schießt nicht
auf den Gegner, der am weitesten ist, sondern auf den mit den **wenigsten aktuellen
Lebenspunkten**. So entkommt kein fast besiegter Ork.

**Konstruktor:** `super().__init__(x, y)`, dann:

| `schaden` | `reichweite` | `nachladezeit` |
| --- | --- | --- |
| 9 | 160 | 0.7 |

**Zielwahl:** Wie in Mission 4, nur das Vergleichskriterium ist anders.

- Besiegte und zu weit entfernte Gegner zählen nicht (Abstand **höchstens** `self.reichweite`).
- Unter den übrigen gewinnt das kleinste `leben`.
- Bei Gleichstand bleibt der **erste** passende Gegner der Liste ausgewählt.
- Kein passender Gegner: `None`. Die Liste bleibt unverändert.

Treffen und Upgrades erbt der Wachtmeister von `Turm`. Er kostet **55 Gold und 20 Holz**:
Sein Bauplan steht schon in `welt.BAUPLAENE`.

**Fertig, wenn:** `python pruefen.py 13` grün ist. Wähle ihn im Spiel mit **4**.

<details><summary>Hinweis</summary>
Schau dir deine Lösung von Mission 4 an. Welche einzige Zeile musst du ändern?
Denke daran: Ein besiegter Gegner mit 0 Leben hat zwar die wenigsten Lebenspunkte,
ist aber kein Ziel.
</details>

**Denkfrage:** Der Wachtmeister steht neben einem Troll mit 30 Leben und einem Ork
mit 40 Leben, der gleich das Dorf erreicht. Wen trifft er? Ist das klug?

---

## 14 · Sägewerk, Steinbruch und Markt

**Du änderst:** die Klasse `Gebaeude` und drei Methoden der neuen Klasse `Dorf`.
**Du übst:** Objekte in einer Liste, Kopien von Dictionaries, `super()` in einer normalen Methode.

Rudersdorf bekommt Gebäude, die nach jeder Welle Rohstoffe liefern.
Ihre Baupläne stehen in `welt.GEBAEUDE`:

| Art | Name | Kosten | Ertrag pro Welle |
| --- | --- | --- | --- |
| `"saegewerk"` | Sägewerk | 40 Gold, 15 Stein | 15 Holz |
| `"steinbruch"` | Steinbruch | 40 Gold, 25 Holz | 12 Stein |
| `"markt"` | Marktplatz | 40 Holz, 30 Stein | 20 Gold |

### a) Die Klasse `Gebaeude`

- `__init__(self, art, name, ertrag)`: Speichere `art`, `name` und eine **Kopie** von `ertrag`.
  Wenn später jemand das übergebene Dictionary ändert, bleibt der Ertrag des Gebäudes gleich.
- `liefere(self, vorraete)`: Addiere jeden Ertrag zum übergebenen Vorrats-Dictionary.
  Ein Rohstoff, den es im Vorrat noch nicht gibt, beginnt bei 0. Kein Rückgabewert.

### b) Das neue `Dorf`

Das neue `Dorf` erbt vom Dorf aus Teil 1. Sein Konstruktor ist schon vorbereitet:
Er ruft `super().__init__()` auf und legt `self.gebaeude = []` an.

- `anzahl(self, art)`: Wie viele Gebäude dieser Art stehen in `self.gebaeude`?
- `baue_gebaeude(self, art)`:
  1. Unbekannte Art (nicht in `GEBAEUDE`)? `False`.
  2. Schon `MAX_GLEICHE_GEBAEUDE` (also 2) Gebäude dieser Art? `False`, **ohne zu bezahlen**.
  3. Bezahle die Kosten mit deiner `bezahle`-Methode aus Mission 3. Zu teuer? `False`.
  4. Hänge ein neues `Gebaeude`-Objekt an `self.gebaeude` an. Ergebnis `True`.
- `sammle_einkommen(self)`: Die erste Zeile ist vorbereitet und holt das Einkommen
  aus Mission 8 mit `super()`. Ergänze, dass danach **jedes** Gebäude liefert.

`welt.GEBAEUDE` darf sich dabei nie verändern.

**Fertig, wenn:** `python pruefen.py 14` grün ist. Die Gebäude erscheinen auf der Karte.

<details><summary>Hinweis 1</summary>
Für <code>anzahl</code>: eine Zählvariable und eine Schleife über <code>self.gebaeude</code>.
Vergleiche <code>gebaeude.art</code> mit der gesuchten Art.
</details>
<details><summary>Hinweis 2</summary>
<code>plan = GEBAEUDE[art]</code> gibt dir <code>plan["name"]</code>, <code>plan["kosten"]</code> und
<code>plan["ertrag"]</code>. Für das Einkommen ruft das Dorf einfach <code>gebaeude.liefere(self.vorraete)</code>
für jedes Gebäude auf. Das Gebäude weiß selbst, was es liefert.
</details>

**Denkfrage:** Warum lassen wir das Gebäude selbst liefern, statt im Dorf
`if gebaeude.art == "markt": ...` zu schreiben? Was passiert, wenn du ein viertes Gebäude erfindest?

---

## 15 · Die Chronik

**Du änderst:** vier Methoden der Klasse `Chronik`.
**Du übst:** Listen: anhängen, ausschneiden, umdrehen, zählen, Doppelte aussortieren.

Die Dorfälteste schreibt jeden besiegten Gegner in ein dickes Buch. Die Chronik ist
eine Liste von Namen in `self.eintraege`: **der älteste Eintrag vorn, der neueste hinten.**
Der Konstruktor ist vorbereitet und beginnt mit einer leeren Liste.
Das Spiel ruft `trage_ein` für jeden besiegten Gegner auf und zeigt die vier
neuesten Namen unter „ZULETZT BESIEGT“.

| Methode | Ergebnis |
| --- | --- |
| `trage_ein(name)` | Hängt `name` **hinten** an. Kein Rückgabewert. |
| `letzte(anzahl)` | Die `anzahl` neuesten Einträge als **neue** Liste, **der neueste zuerst**. |
| `zaehle(name)` | Wie oft `name` in der Chronik steht. |
| `ohne_doppelte()` | Eine **neue** Liste, jeder Name nur einmal, in der Reihenfolge seines ersten Auftretens. |

**Beispiel:** Die Chronik enthält `["A", "B", "C", "D", "E"]`.

- `letzte(3)` → `["E", "D", "C"]`
- `letzte(10)` → `["E", "D", "C", "B", "A"]`: Gibt es weniger Einträge, dann eben alle.
- `letzte(0)` und `letzte(-3)` → `[]`

Für `["Ork", "Troll", "Ork", "Oger", "Troll", "Ork"]`:

- `zaehle("Ork")` → `3`, `zaehle("Drache")` → `0`
- `ohne_doppelte()` → `["Ork", "Troll", "Oger"]`

**Wichtig:** `letzte` und `ohne_doppelte` dürfen `self.eintraege` **nicht verändern**.
Die Chronik bleibt vollständig und in zeitlicher Reihenfolge.

**Fertig, wenn:** `python pruefen.py 15` grün ist.

<details><summary>Hinweis 1</summary>
Löse <code>letzte</code> in zwei Schritten: Erst die letzten Einträge herausschneiden
(<code>liste[-anzahl:]</code>), dann umdrehen (<code>[::-1]</code>). Beides erzeugt neue Listen.
Probiere aus, was <code>liste[-0:]</code> ergibt. Deshalb brauchst du für 0 einen eigenen Fall.
</details>
<details><summary>Hinweis 2</summary>
Für <code>ohne_doppelte</code>: Lege eine leere Ergebnisliste an. Gehe die Chronik durch und
hänge einen Namen nur an, wenn er noch <strong>nicht</strong> im Ergebnis steht (<code>not in</code>).
<code>liste.reverse()</code> wäre hier gefährlich. Weißt du, warum?
</details>

**Denkfrage:** Du könntest die neuesten Einträge auch vorn einfügen statt hinten.
Was würde sich dann an `letzte` ändern?

---

## 16 · Zusatz: Der Dorfschreiber

**Du änderst:** die Funktion `erstelle_spielstand(dorf, tuerme, welle)`.
**Du übst:** verschachtelte Dictionaries und Listen; Daten, die als JSON gespeichert werden können.

Mit **S** soll das Spiel in einer Baupause speichern. Der Spielkern schreibt die
Datei `spielstand.json`, aber **was** darin steht, bestimmst du. JSON kennt nur
Zahlen, Texte, `True`/`False`, `None`, Listen und Dictionaries mit **Text-Schlüsseln**.
Objekte wie Türme kann es nicht speichern. Du musst sie also in einfache Werte übersetzen.

- `dorf` ist dein `Dorf`-Objekt.
- `tuerme` ist das Dictionary des Spielkerns: **Bauplatz-Nummer → Turmobjekt**.
  Jeder Turm hat `art` (zum Beispiel `"pfeil"`) und `stufe`.
- `welle` ist die Anzahl der schon gestarteten Wellen.

Gib genau diese Form zurück:

```python
{
    "version": 1,
    "welle": 4,
    "dorf": {
        "vorraete": {"gold": 95, "holz": 40, "stein": 12},
        "leben": 17,
        "mauer": 3,
        "max_mauer": 10,
        "haeuser": 5,
        "bewohner": 20,
        "gebaeude": ["markt", "saegewerk"],  # die Arten, in Bau-Reihenfolge
    },
    "tuerme": [  # eine Liste, sortiert nach Bauplatz
        {"platz": 1, "art": "pfeil", "stufe": 3},
        {"platz": 7, "art": "kanone", "stufe": 2},
    ],
}
```

Ein Spielstand ist wie ein **Foto**: Ändert sich das Dorf später, darf sich der
Spielstand nicht mitverändern. Speichere also eine Kopie der Vorräte.

**Fertig, wenn:** `python pruefen.py 16` grün ist. Drücke im Spiel **S** in einer Baupause
und öffne danach `spielstand.json` im Editor. Erkennst du dein Dorf?

<details><summary>Hinweis</summary>
<code>sorted(tuerme)</code> liefert die Bauplätze aufsteigend. Für jeden Platz holst du mit
<code>tuerme[platz]</code> den Turm und baust ein kleines Dictionary.
</details>

**Denkfrage:** Warum ist `"tuerme"` eine Liste und kein Dictionary `{1: ..., 7: ...}`?
Tipp: Probiere `json.loads(json.dumps({1: "pfeil"}))` aus.

---

## 17 · Zusatz: Die Siegelprüfung

**Du änderst:** die Funktion `pruefe_spielstand(daten)`.
**Du übst:** Daten von außen misstrauen; Schlüssel prüfen, bevor man sie liest.

Mit **L** lädt das Spiel `spielstand.json`. Aber was, wenn jemand die Datei von Hand
verändert hat? Dann könnte das Dorf plötzlich 99 Leben, einen Turm auf Bauplatz 42
oder eine Laserkanone haben. Bevor der Spielkern einen Stand lädt, fragt er deshalb
deine Funktion.

Gib eine **Liste von Problemen** zurück, jedes als verständlicher Text.
**Eine leere Liste bedeutet: gültig.** Ist `daten` gar kein Dictionary, gib sofort
eine Liste mit einem Problem zurück.

Ein Spielstand ist nur gültig, wenn alles hier stimmt:

| Wo | Regel |
| --- | --- |
| `version` | genau `1` |
| `welle` | ganze Zahl von 0 bis `len(WELLEN) - 1` |
| `dorf` | ein Dictionary |
| `dorf["vorraete"]` | Dictionary mit `gold`, `holz` und `stein`, jeweils ganze Zahl ≥ 0 |
| `dorf["leben"]` | ganze Zahl von 1 bis 20 |
| `mauer`, `max_mauer`, `haeuser`, `bewohner` | ganze Zahlen ≥ 0, und `mauer` ≤ `max_mauer` |
| `dorf["gebaeude"]` | Liste bekannter Arten aus `GEBAEUDE`, höchstens `MAX_GLEICHE_GEBAEUDE` je Art |
| `tuerme` | eine Liste von Dictionaries |
| jeder Turm | `platz` ganze Zahl von 0 bis `len(BAUPLAETZE) - 1`, kein Platz doppelt, `art` aus `BAUPLAENE`, `stufe` 1, 2 oder 3 |

Und ganz wichtig: Die Funktion darf **niemals abstürzen**, auch wenn Schlüssel fehlen.
Sie verändert die Daten nicht, sie liest nur.

**Fertig, wenn:** `python pruefen.py 17` und `python pruefen.py --teil2` grün sind.
Speichere, öffne `spielstand.json`, setze `"leben": 99` und drücke **L**.
Das Dorf sollte dir den Grund für die Ablehnung nennen.

<details><summary>Hinweis 1</summary>
<code>daten.get("welle")</code> gibt <code>None</code> zurück, wenn der Schlüssel fehlt, statt abzustürzen.
<code>isinstance(wert, int)</code> prüft auf ganze Zahlen. Ein Text wie <code>"3"</code> ist keine Zahl.
</details>
<details><summary>Hinweis 2</summary>
Schreibe dir eine kleine Hilfsfunktion, die prüft: „Ist das eine ganze Zahl zwischen
kleinste und groesste?“ Du brauchst sie mindestens zehnmal.
Für doppelte Bauplätze: Merke dir die schon gesehenen Plätze in einer Liste (wie in Mission 15).
</details>

**Denkfrage für Fortgeschrittene:** In Python ist `True` auch eine ganze Zahl
(`isinstance(True, int)` ergibt `True`!). Ist `"welle": true` in der JSON-Datei gültig?
Wie würdest du das verhindern?

---

**Alles grün?** Dann hast du ein echtes Spiel mit Vererbung, Listen, Dictionaries
und Speicherständen gebaut. Ab jetzt gehört Rudersdorf ganz dir:
In [KNOBELAUFGABEN.md](KNOBELAUFGABEN.md) warten Ideen ohne fertige Lösung.
