# Luki, Rudersdorf braucht dich!

Im Flüsterwald sammeln sich die Orks. In Rudersdorf klopft die Schmiedin auf ihren
Amboss, der Bäcker schließt seine Tür und die Dorfwache schaut zu dir:
**„Unsere Türme stehen bereit. Kannst du ihnen beibringen, was sie tun sollen?“**

Du arbeitest in `modell.py`. Die Zeichnungen, Knöpfe und Uhr sind schon fertig.
Die Stellen mit `raise NotImplementedError(...)` sind deine Baustellen.
Ersetze diesen Platzhalter durch deinen Code. Ändere die Namen der Klassen,
Methoden und Parameter nicht: Spiel und Tests kennen genau diese Namen.

## So arbeitest du an einer Mission

1. Lies die Mission und die erwarteten Regeln.
2. Starte ihren Test: `python pruefen.py 1` (Nummer passend ersetzen).
3. Implementiere zuerst den einfachen Fall.
4. Starte denselben Test noch einmal. Lies immer zuerst **einen** Hinweis.
5. Ergänze die Randfälle. Grün? Erkläre jemandem, warum dein Code funktioniert.
6. Probiere nach den Grundaufgaben die komplette Partie mit `python spielen.py`.

Die Tests sind dein Trainingspartner, keine Benotung. Am Anfang sind rote Ergebnisse
normal. Ein Hinweis ist eine konkrete Situation, die dein Code noch lernen muss.
Manchmal braucht ein Kapitel eine frühere Methode: Aufgabe 4–6 verwenden etwa die
Schadensregeln aus 2; die Zusätze verwenden die Bezahlung aus 3.
Die Tests für 2 stellen Test-Orks selbst bereit, damit du unabhängig von 1 üben kannst.

### Mini-Spickzettel

- **Klasse:** ein Bauplan, zum Beispiel `Gegner`.
- **Objekt:** ein konkreter Ork aus diesem Bauplan.
- **`__init__`:** wird beim Erstellen aufgerufen. Hier bekommt das Objekt seine Startwerte.
- **`self`:** dieses konkrete Objekt. `self.leben` gehört genau diesem Ork.
- **Methode:** eine Funktion an einem Objekt, zum Beispiel `ork.erleide_schaden(12)`.
- **`return`:** gibt ein Ergebnis an den aufrufenden Code zurück. `print` ersetzt das nicht.
- **Liste:** mehrere Dinge in einer Reihenfolge, zum Beispiel Gegner auf dem Weg.
- **Dictionary:** Werte unter Namen, zum Beispiel `{"gold": 160, "holz": 80}`.

Die Eingaben des Spiels sind Zahlen in den unten beschriebenen Bereichen.
Du brauchst keine Zeichenketten in Zahlen umzuwandeln und keine fremden Datentypen
abzufangen. Die ausdrücklich beschriebenen Grenzfälle gehören aber dazu.

---

## 1 · Die Orks bekommen Namen

**Du änderst:** `Gegner.__init__(self, name, leben, tempo, belohnung)`.
**Du übst:** Konstruktor und Objektattribute.

Jeder Ork braucht einen eigenen Steckbrief. Beim Erstellen werden vier Werte
übergeben. Speichere sie am Objekt:

| Attribut | Startwert | Bedeutung |
| --- | --- | --- |
| `name` | Parameter `name` | Name des Gegners |
| `leben` | Parameter `leben` | Aktuelle Lebenspunkte |
| `max_leben` | ebenfalls Parameter `leben` | Voller Lebensbalken |
| `tempo` | Parameter `tempo` | Wegstrecke in Pixeln pro Sekunde |
| `belohnung` | Parameter `belohnung` | Gold nach dem Sieg über diesen Gegner |
| `fortschritt` | `0.0` | Schon zurückgelegter Weg |
| `x`, `y` | jeweils `0.0` | Bildschirmposition, später vom Spiel gesetzt |
| `frost_rest` | `0.0` | Verbleibende Sekunden im Frost |

`leben` und `tempo` sind beim Erstellen positiv, `belohnung` nicht negativ.
Du brauchst dafür in dieser Mission keine zusätzliche Prüfung.

**Beispiel:** `Gegner("Grummel", 70, 33, 11)` hat 70 aktuelle und maximale
Lebenspunkte. Ein zweiter Ork darf seine Werte behalten, wenn Grummel verletzt wird.

**Fertig, wenn:** `python pruefen.py 1` grün ist. `__init__` braucht kein `return`.

<details><summary>Hinweis 1</summary>
Eine lokale Variable verschwindet nach der Methode. Ein Attribut wie `self.name`
bleibt am Objekt gespeichert.
</details>
<details><summary>Hinweis 2</summary>
Wenn ein Parameter `farbe` hieße, wäre `self.farbe = farbe` die passende Zuweisung.
Übertrage dieses Muster auf den Steckbrief. Manche Startwerte kommen nicht aus Parametern.
</details>

**Denkfrage:** Warum speichern wir `max_leben` zusätzlich zu `leben`?

---

## 2 · Treffer!

**Du änderst:** `Gegner.erleide_schaden(schaden)` und `Gegner.ist_besiegt()`.
**Du übst:** Rechnen, Vergleichen und Rückgabewerte.

Ein Pfeil soll den Ork verletzen. Dabei gelten vier Regeln:

1. Nicht negativer Schaden wird vom **aktuellen** Leben abgezogen.
2. Leben kann bis 0 sinken, aber niemals darunter.
3. Negativer Schaden wird ignoriert. Er darf den Gegner nicht heilen.
4. `max_leben` verändert sich nicht.

`erleide_schaden` verändert das Objekt und braucht keinen Rückgabewert.
`ist_besiegt` gibt dagegen **`True` bei Leben ≤ 0**, sonst **`False`** zurück.
Auch ein Testobjekt mit negativem Leben gilt als besiegt.

| Vorher | Schaden | Nachher |
| --- | --- | --- |
| 40 | 12 | 28 |
| 40 | 100 | 0 |
| 40 | -10 | 40 |
| 40 | 0 | 40 |

**Fertig, wenn:** `python pruefen.py 2` grün ist.

<details><summary>Hinweis 1</summary>
Löse zuerst den normalen Treffer. Überlege dann getrennt: Was passiert, wenn der
Schaden größer als das Leben ist? Und was passiert beim Abziehen einer negativen Zahl?
</details>
<details><summary>Hinweis 2</summary>
Du kannst Grenzen mit `if` prüfen oder mit `min` und `max` begrenzen.
Ein Vergleich ist bereits ein Wahrheitswert, den du zurückgeben kannst.
</details>

**Denkfrage:** Was wäre der Unterschied zwischen `print(self.leben <= 0)` und
`return self.leben <= 0` für den aufrufenden Turm?

---

## 3 · Die Dorfkasse

**Du änderst:** `Dorf.bezahle(kosten)`.
**Du übst:** Dictionaries und eine Änderung, die nur vollständig stattfinden darf.

`self.vorraete` enthält zu Beginn `{"gold": 160, "holz": 80, "stein": 60}`.
`kosten` ist ein Dictionary, zum Beispiel `{"gold": 45, "holz": 10}`.

**Vertrag:**

- Sind **alle** Preise gültig und bezahlbar, ziehe sie ab und gib `True` zurück.
- Fehlt auch nur ein Rohstoff, gib `False` zurück und ändere **überhaupt nichts**.
- Genau genug Vorrat reicht aus.
- Ein nicht vorhandener Rohstoff hat Bestand 0.
- Negative Kosten sind ungültig: gesamter Kauf abgelehnt, keine Veränderung.
- `{}` und Preise von 0 sind kostenlos und erfolgreich.
- Ein unbekannter Rohstoff mit Preis 0 ist auch kostenlos; lege dafür keinen neuen Eintrag an.
- Verändere niemals das übergebene `kosten`-Dictionary.

**Die Falle:** Bei `{"gold": 10, "stein": 999}` reicht Gold, aber Stein nicht.
Wenn du erst Gold abziehst und dann den fehlenden Stein bemerkst, verliert das Dorf
Geld, obwohl gar nichts gebaut wird!

**Fertig, wenn:** `python pruefen.py 3` grün ist.

<details><summary>Hinweis 1</summary>
Trenne Prüfen und Bezahlen. Dafür darfst du zweimal über das Dictionary laufen.
</details>
<details><summary>Hinweis 2</summary>
`for name, anzahl in kosten.items():` liefert Schlüssel und Wert zusammen.
`self.vorraete.get(name, 0)` liefert bei einem unbekannten Namen 0.
Buche erst ab, nachdem die gesamte Prüfung erfolgreich war.
</details>

**Denkfrage:** Warum wäre ein Preis-Dictionary, das beim Kaufen verändert wird,
für den nächsten Turmkauf gefährlich?

---

## 4 · Wen beschießen wir?

**Du änderst:** `Turm.waehle_ziel(gegner)`.
**Du übst:** Liste durchsuchen und einen besten Kandidaten merken.

Ein Turm bekommt eine Liste von Gegnerobjekten. Er soll **das Objekt** des
gefährlichsten erreichbaren Gegners zurückgeben, nicht dessen Namen oder Index.

- Besiegte Gegner werden ignoriert.
- Der Abstand zwischen Turm und Gegner muss **höchstens** `self.reichweite` sein.
- Unter diesen Kandidaten gewinnt der größte `fortschritt`.
- Bei gleichem Fortschritt bleibt der **erste passende Gegner in der Liste** ausgewählt.
- Kein passender Gegner? Gib `None` zurück.
- Die übergebene Liste bleibt unverändert, einschließlich ihrer Reihenfolge.

**Abstand:** `hypot(unterschied_x, unterschied_y)` berechnet ihn.
`hypot` ist bereits importiert. Beide Unterschiede berechnest du aus den Positionen
von Gegner und Turm. Beispiel: 3 Pixel waagerecht und 4 senkrecht ergeben Abstand 5.

**Beispiel:** Ein Ork mit Fortschritt 90 ist gefährlicher als einer mit Fortschritt 5,
auch wenn letzterer näher am Turm steht. Ein Ork außerhalb der Reichweite ist kein Ziel.

**Fertig, wenn:** `python pruefen.py 4` grün ist.

<details><summary>Hinweis 1</summary>
Starte mit „noch kein Ziel“. Gehe dann durch alle Gegner. Erst prüfen, ob der Kandidat
erlaubt ist; erst danach prüfen, ob er besser als das bisherige Ziel ist.
</details>
<details><summary>Hinweis 2</summary>
`None` steht für „kein Objekt“. Bevor du auf `ziel.fortschritt` zugreifst,
muss es überhaupt ein Ziel geben. Bei Gleichstand sollst du das Ziel nicht ersetzen.
</details>

**Denkfrage:** Warum kann der nächstgelegene Ork strategisch das falsche Ziel sein?

---

## 5 · Eis und Donner

**Du änderst:** die Konstruktoren und `treffe(ziel, gegner)` in `Frostturm` und `Kanonenturm`.
**Du übst:** Vererbung, `super()` und das Überschreiben einer Methode.

`Turm` hat bereits Position, Stufe, Reichweite, Schaden und eine Nachladezeit.
`Pfeilturm` erbt alles unverändert. Die Spezialtürme brauchen diese gemeinsame
Ausstattung ebenfalls — kopiere sie nicht in jede Klasse.

**Konstruktoren:** Rufe den Basiskonstruktor mit `super().__init__(x, y)` auf.
Passe danach nur diese Werte an:

| Typ | `schaden` | `reichweite` | `nachladezeit` |
| --- | --- | --- | --- |
| Frostturm | 5 | 110 | 1.2 |
| Kanonenturm | 18 | 145 | 1.8 |

**Frosttreffer:**

- Nur `ziel` erleidet `self.schaden`.
- Seine `frost_rest` wird auf mindestens 2.0 Sekunden gesetzt.
- Eine schon längere Frostzeit bleibt erhalten.
- Die vorbereitete Bewegung halbiert das Tempo während dieser Zeit automatisch.

**Kanonentreffer:**

- Der Einschlag liegt an der Position von `ziel`.
- Jeder lebende Gegner mit Abstand **höchstens 45** zum Einschlag erleidet `self.schaden`.
- Das Ziel steht selbst in der übergebenen Liste und wird genau einmal getroffen.
- Gegner außerhalb dieses Radius und bereits besiegte Gegner werden nicht getroffen.
- Verändere die Gegnerliste nicht. Das Aufräumen kommt in Mission 6.

`treffe` braucht keinen Rückgabewert. Die Spielschleife kümmert sich um Nachladen
und die Frage, wann geschossen wird. Verwende in den Treffermethoden
**`self.schaden`**, damit ein späteres Upgrade tatsächlich stärker schießt.

**Fertig, wenn:** `python pruefen.py 5` grün ist.

<details><summary>Hinweis 1</summary>
Ein Spezialturm **ist ein** Turm. Mit dem Basiskonstruktor erbt er seine normale
Ausstattung. Eine Methode mit demselben Namen ersetzt das geerbte Verhalten.
</details>
<details><summary>Hinweis 2</summary>
Für Frost brauchst du keine Schleife. Für die Kanone schon: Prüfe jeden Gegner
gegen die Position des Ziels, nicht gegen die Position der Kanone.
</details>

**Denkfrage:** Was fehlt dem Frostturm, wenn du `super().__init__` vergisst?

---

## 6 · Nach dem Kampf

**Du änderst:** die freie Funktion `sammle_beute(gegner, dorf)` am Dateiende.
**Du übst:** Eine neue Liste aufbauen und unterschiedliche Fälle behandeln.

Diese Funktion gehört keiner Klasse an, deshalb gibt es hier kein `self`.

- Gehe durch die übergebene Gegnerliste.
- Für jeden besiegten Gegner addierst du dessen `belohnung` zu `dorf.vorraete["gold"]`.
- Jeder lebende Gegner kommt in eine **neue Liste**, in ursprünglicher Reihenfolge.
- Gib diese neue Liste zurück.
- Die Eingabeliste bleibt unverändert. Holz und Stein ebenfalls.
- Auch eine leere Liste ist erlaubt.

Der Spielkern ersetzt die alte Liste durch dein Ergebnis. Beim nächsten Aufruf
bekommst du deshalb nur noch die Überlebenden. So wird Gold nicht doppelt gezählt.
Du musst keine zusätzliche „schon bezahlt“-Eigenschaft speichern.

**Beispiel:** `[besiegt(7 Gold), lebendig, besiegt(13 Gold)]` wird zu `[lebendig]`.
Das Dorf bekommt zusätzlich 20 Gold.

**Fertig, wenn:** `python pruefen.py 6` und anschließend
`python pruefen.py --basis` grün sind. **Jetzt gehört die erste Partie dir!**

<details><summary>Hinweis 1</summary>
Entferne keine Elemente aus der Liste, die du gerade durchläufst.
Sonst kann ein direkt folgender Gegner übersprungen werden.
</details>
<details><summary>Hinweis 2</summary>
Lege am Anfang eine leere Liste an. Mit `.append(...)` sammelst du die Überlebenden.
Denke an `return` nach der Schleife, nicht mitten darin.
</details>

**Denkfrage:** Was würde passieren, wenn der Spielkern beim nächsten Mal wieder
die alte Liste mit denselben besiegten Orks übergäbe?

---

## 7 · Zusatz: Die Stadtmauer

**Du änderst:** `Dorf.baue_mauer()` und `Dorf.repariere_mauer()`.
**Voraussetzung:** Aufgabe 3.

Rudersdorf braucht Schutz für den Fall, dass ein Ork durchbricht.
Die vorbereitete Methode `erleide_schaden` verbraucht zuerst Mauerpunkte;
übriger Schaden trifft die Dorf-Lebenspunkte. Das musst du nicht neu schreiben.

**Bauen:** Bezahle 20 Holz und 30 Stein. Nur bei Erfolg erhöhen sich `mauer` und
`max_mauer` jeweils um 5. Gib `True` bei Erfolg, sonst `False` zurück.
Ein wiederholter Ausbau addiert weitere 5 Punkte. Auch eine beschädigte Mauer
bekommt durch Ausbau nur 5 aktuelle Punkte dazu, keine kostenlose Vollreparatur.

**Reparieren:** Ohne Mauer oder bei voller Mauer: `False`, keine Kosten.
Andernfalls bezahle 10 Stein. Bei Erfolg erhöhe `mauer` um bis zu 5, höchstens
auf `max_mauer`, und gib `True` zurück. `max_mauer` verändert sich dabei nicht.
Bei Geldmangel bleibt alles unverändert und das Ergebnis ist `False`.

**Fertig, wenn:** `python pruefen.py 7` grün ist. Probiere die Dorfknöpfe aus.

<details><summary>Hinweis</summary>
Verwende deine fertige Methode `bezahle`, damit ein fehlender Rohstoff nicht zu
Teilzahlungen führt. Prüfe bei der Reparatur zuerst, ob sie überhaupt nötig ist.
</details>

---

## 8 · Zusatz: Neue Nachbarn

**Du änderst:** `Dorf.baue_haus()` und `Dorf.sammle_einkommen()`.
**Voraussetzung:** Aufgabe 3.

Ein Haus kostet **30 Gold und 25 Holz**. Bei erfolgreicher Bezahlung wachsen
`haeuser` um 1 und `bewohner` um 4; Ergebnis `True`. Bei Mangel: nichts ändern,
`False` zurückgeben. Das Dorf beginnt mit 3 Häusern und 12 Bewohnern.

Für `sammle_einkommen` gilt:

| Quelle | Einkommen pro Aufruf |
| --- | --- |
| Jedes Haus | 5 Gold und 3 Stein |
| Jeder Bewohner | 1 Holz |

Addiere diese Beträge zu den vorhandenen Vorräten. Verändere weder Häuser noch
Bewohner. Die Methode braucht keinen Rückgabewert. Ein leeres Dorf erzeugt nichts.
Der Spielkern ruft sie **einmal zwischen zwei Wellen** auf, zusätzlich zur
Grundversorgung. Nach der letzten Welle ist bereits gewonnen, dann gibt es kein Einkommen.

**Fertig, wenn:** `python pruefen.py 8` grün ist. Neue Häuser erscheinen im Dorf.
Die Zeichnung zeigt maximal acht Häuser und zwanzig Bewohner; für die Wirtschaft
zählen alle. Diese Begrenzung kannst du später selbst erweitern.

<details><summary>Hinweis</summary>
Du musst nicht für jedes Haus einzeln zählen. Multiplikation passt hier gut.
Achte auf den Unterschied zwischen „auf einen Wert setzen“ und „etwas hinzufügen“.
</details>

---

## 9 · Zusatz: Die Turmschmiede

**Du änderst:** `Turm.verbessere(dorf)`.
**Voraussetzung:** Aufgabe 3; die Spezialturm-Prüfung nutzt auch 5.

Jeder Turm beginnt auf Stufe 1. Maximalstufe ist 3.

1. Auf Stufe 3 oder höher: `False`, keine Veränderung.
2. Kosten sind **35 Gold mal aktuelle Stufe**. Von 1 auf 2 also 35, von 2 auf 3 also 70.
3. Nur bei erfolgreicher Bezahlung: Stufe +1, Schaden +6, Reichweite +15.
4. Gib bei Erfolg `True`, bei Mangel `False` zurück.
5. Position und Nachladezeit bleiben gleich.

Die Spezialtürme erben diese Methode. Du musst sie nicht dreimal schreiben.
Im Spiel: Zwischen Wellen einen gebauten Turm anklicken, dann den Upgrade-Knopf.

**Fertig, wenn:** `python pruefen.py 9` und `python pruefen.py --alle` grün sind.

<details><summary>Hinweis</summary>
Berechne den Preis, bevor du die Stufe erhöhst. Nutze die Dorfkasse zum Bezahlen.
Erhöhe erst danach die drei Turmeigenschaften.
</details>

**Geschafft?** Der Orkkönig hat davon gehört … Weiter geht es in
[AUFGABEN-TEIL2.md](AUFGABEN-TEIL2.md). Freie Ideen ohne Lösung findest du in
[KNOBELAUFGABEN.md](KNOBELAUFGABEN.md).
