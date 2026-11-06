# Rudersdorf wird dein Spiel

Die Missionen aus `AUFGABEN.md` und `AUFGABEN-TEIL2.md` haben klare Regeln und fertige Tests.
Hier entscheidest **du** über das Design. Für diese freien Erweiterungen gibt es
absichtlich keine fertige Lösung und keine fertigen Bewertungstests.
Schreibe zuerst zwei oder drei eigene Beispiele auf: Was soll passieren — und was nicht?

> Einige frühere Knobelideen sind inzwischen echte Missionen geworden: der Wachtmeister (13),
> der Schildork (11), der Troll (12), die Gebäude (14) und das Speichern (16–17).
> Schau dir an, wie sie gelöst wurden, und baue darauf auf.

## 1 · Der Giftturm ★★

Ein Giftpfeil wirkt nicht sofort, sondern **über Zeit**: zum Beispiel 4 Schaden pro
Sekunde, 3 Sekunden lang.

- Der Turm setzt beim Treffer am Ziel eine Giftzeit, ähnlich wie `frost_rest`.
- Den Schaden verursacht der Gegner selbst in `bewege`, mit `super().bewege(...)` wie beim Troll.
- Entscheide: Verlängert ein zweiter Treffer das Gift oder wird es stärker?
- Ergänze Bauplan, Kurzname und Zeichnung (siehe `ERWEITERN.md`).

**Eigene Tests:** Gift läuft ab; ein besiegter Gegner nimmt keinen weiteren Schaden;
Gift und Troll-Heilung zusammen: Wer gewinnt? Schildork-Rüstung gegen Gift?
**Denkfrage:** Warum ist Gift gegen Schildorks so stark?

## 2 · Rudersdorfs Bestenliste ★★

Nach Sieg oder Niederlage soll das Spiel eine Bestenliste zeigen: die fünf besten
Partien nach besiegten Gegnern.

- Eine Partie ist ein Dictionary, etwa `{"name": "Luki", "besiegt": 74, "welle": 10}`.
- Die Bestenliste ist eine **Liste** solcher Dictionaries. Neue Einträge kommen hinzu;
  danach wird sortiert und auf fünf gekürzt.
- Tipp: `sorted(liste, key=lambda partie: partie["besiegt"], reverse=True)` und `liste[:5]`.
- Speichere die Liste als JSON wie in Mission 16.

**Eigene Tests:** Leere Liste; genau fünf; ein sechster, schlechterer Eintrag fällt raus;
Gleichstand. **Denkfrage:** Wer gewinnt bei Gleichstand — die ältere oder die neuere Partie?

## 3 · Die Chronik wird schlau ★

Erweitere die `Chronik` aus Mission 15:

- `haeufigster()` gibt den Namen zurück, der am öftesten vorkommt (bei Gleichstand der zuerst gesehene).
- `statistik()` liefert ein Dictionary Name → Anzahl. Kommt dir das aus Mission 10 bekannt vor?
- Zeige nach dem Sieg „Am meisten besiegt: Ork (31×)“.

**Eigene Tests:** Leere Chronik; ein einziger Eintrag; Gleichstand.

## 4 · Türme verkaufen ★★

Ein Turm am falschen Platz? Verkaufe ihn für die Hälfte des Baupreises.

- Entscheide, ob Upgrades auch zur Hälfte erstattet werden.
- Der Spielkern speichert Türme in `self.tuerme`; der Bauplatz wird wieder frei.
- Verkaufen nur in Baupausen, oder auch während einer Welle?
- Achtung bei ungeraden Preisen: 45 Gold / 2 = 22,5. Rundest du ab oder auf?

**Eigene Tests:** Verkaufen und neu bauen auf demselben Platz; Holzpreis beim Wachtmeister;
verkaufen eines nicht vorhandenen Turms ändert nichts.

## 5 · Die Dorfbewohner bekommen Berufe ★★

Bisher sind Bewohner eine Zahl. Mache daraus Figuren mit Namen und Berufen:
`Dorfbewohner`, `Holzfaeller`, `Steinmetzin` und `Baeuerin`.

- Beginne mit einem Konstruktor für Name und Beruf.
- Lass einen Bewohner pro Runde einen Rohstoffbeitrag als Dictionary liefern —
  genau wie `Gebaeude.liefere` aus Mission 14.
- Die Oberfläche soll weiterhin ohne Kenntnis einzelner Berufe zeichnen können.

**Eigene Tests:** Zwei Bewohner teilen keine veränderlichen Vorräte.
Zwei Holzfäller liefern doppelt so viel wie einer.
**Denkfrage:** Sind verschiedene Unterklassen wirklich nötig, oder reicht ein Beruf im Dictionary?

## 6 · Der Orkkönig persönlich ★★★

Eine elfte Welle mit nur einem Gegner: dem Orkkönig.

- Er hat sehr viele Lebenspunkte und einen Schild **und** heilt sich.
  Kannst du von Schildork **und** Troll erben? (Stichwort: Mehrfachvererbung, `super()` in beiden.)
- Oder ruft er alle 5 Sekunden zwei Orks herbei? Dann muss der Spielkern neue Gegner
  während der Welle aufnehmen können.
- Wähle **eine** Idee und beschreibe sie genau, bevor du programmierst.

**Eigene Tests:** Besiegter König ruft niemanden mehr; Heilung nicht über `max_leben`;
die Welle endet erst, wenn auch die herbeigerufenen Orks weg sind.

## 7 · Ein richtiger Belagerungsangriff ★★★

Ein Rammbock macht der Mauer besonders viel Schaden. Ein Schamane stärkt andere Orks.

**Eigene Tests:** Ein Rammbock vor dem Dorf darf noch keinen Mauerschaden verursachen.
Kein Bonus nach dem Ende einer Welle. Ein besiegter Schamane stärkt niemanden mehr.

## 8 · Dein eigener Kartenbaukasten ★★★

Erweitere Rudersdorf um ein zweites Tal, eine Brücke oder eine andere Dorfposition.

- Beginne in `welt.py` mit Wegpunkten und Bauplätzen.
- Ein Weg muss mindestens zwei unterschiedliche aufeinanderfolgende Punkte haben.
- Der aktuelle Hintergrund wird separat gezeichnet: Passe ihn zur neuen Karte an.
- Später könntest du mehrere Karten als Daten speichern und auswählbar machen.
  Achtung: Ein Spielstand aus Mission 16 passt dann nur zu seiner Karte. Wie merkst du das?

**Eigene Tests:** Eine Position am Anfang und Ende liegt auf dem Weg; ein Knick
funktioniert; keine Division durch null bei ungültigen Wegpunkten.

## Deine Idee zählt

Male dein nächstes Gebäude, deinen nächsten Gegner oder Turm auf Papier. Schreibe darunter:

1. Was kann es?
2. Welche Werte braucht es beim Erstellen?
3. Von welcher Klasse erbt es, und welche Methode überschreibt es?
4. Was ist ein normaler Fall, was ein ungewöhnlicher Fall?
5. Wie kannst du beides ohne Fenster testen?

Damit hast du bereits einen kleinen Entwicklungsplan.
