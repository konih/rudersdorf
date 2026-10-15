# Rudersdorf wird dein Spiel

Die neun Missionen aus `AUFGABEN.md` haben klare Regeln und fertige Tests.
Hier entscheidest **du** über das Design. Für diese freien Erweiterungen gibt es
absichtlich noch keine fertige Lösung und keine fertigen Bewertungstests.
Schreibe zuerst zwei oder drei eigene Beispiele auf: Was soll passieren — und was nicht?

## 1 · Der Wachtmeister: andere Ziele auswählen ★

Der erste Turm beschießt den Gegner mit dem größten Fortschritt. Was wäre, wenn
ein Wachtmeister auf den Gegner mit den wenigsten Lebenspunkten zielen könnte?

- Füge eine neue Turm-Unterklasse hinzu, die nur `waehle_ziel` überschreibt.
- Behalte die Regeln für Reichweite und besiegte Gegner bei.
- Entscheide, wer bei gleichen Lebenspunkten gewinnt.

**Eigene Tests:** Ein schwacher Gegner außerhalb der Reichweite darf nicht gewinnen.
Eine leere Liste liefert weiterhin `None`. Ein Turmwechsel darf die Liste nicht sortieren.
**Denkfrage:** Wann ist diese Strategie schlechter als die ursprüngliche?

## 2 · Ein Ork mit Schild ★★

Ein Schildork kann kleine Treffer abwehren. Führe eine Unterklasse von `Gegner` ein,
die beispielsweise 3 Punkte Schaden pro Treffer abfängt.

- Wird aus 2 Schaden dann 0 oder mindestens 1? Du entscheidest und dokumentierst es.
- Große Treffer sollen weiterhin wirksam sein.
- Negative Treffer dürfen auch einen Schildork nicht heilen.
- Ergänze die Erzeugung im Spielkern: Bisher baut sie immer die Klasse `Gegner`.

**Eigene Tests:** Schaden kleiner, gleich und größer als die Rüstung;
mehrere Treffer hintereinander; Übertreffer auf fast besiegte Orks.
**Denkfrage:** Welche Turmart ist gegen diese Orks besonders geeignet?

## 3 · Die Dorfbewohner bekommen Berufe ★★

Bisher sind Bewohner eine Zahl. Mache daraus Figuren mit Namen und Berufen:
`Dorfbewohner`, `Holzfaeller`, `Steinmetzin` und `Baeuerin`.

- Beginne mit einem Konstruktor für Name und Beruf.
- Lass einen Bewohner pro Runde einen Rohstoffbeitrag als Dictionary liefern.
- Sammle die Beiträge einer Liste von Bewohnern im Dorf.
- Die Oberfläche soll weiterhin ohne Kenntnis einzelner Berufe zeichnen können.

**Eigene Tests:** Zwei Bewohner teilen keine veränderlichen Vorräte.
Ein leeres Dorf liefert nichts. Zwei Holzfäller liefern doppelt so viel wie einer.
**Denkfrage:** Sind verschiedene Unterklassen wirklich nötig, oder reicht manchmal
auch ein Beruf im Dictionary? Probiere beide Varianten auf Papier.

## 4 · Marktplatz und Sägewerk ★★

Gib dem Dorf Gebäude mit unterschiedlichen Fähigkeiten. Ein Sägewerk erzeugt Holz,
ein Steinbruch Stein, ein Marktplatz Gold.

- Plane eine gemeinsame Klasse `Gebaeude` mit Baukosten und Stufe.
- Sammle Gebäude in einer Liste.
- Ein neues Gebäude soll über denselben Bezahlmechanismus wie Häuser entstehen.
- Zeichne zunächst nur ein kleines Symbol oder Schild, dann ein richtiges Gebäude.

**Eigene Tests:** Ohne Vorräte kein Gebäude; Kosten nur einmal abbuchen;
Einkommen hängt von den tatsächlich vorhandenen Gebäuden ab.
**Denkfrage:** Wie verhinderst du, dass ein mächtiges Gebäude das Spiel sofort zu leicht macht?

## 5 · Ein richtiger Belagerungsangriff ★★★

Ein Rammbock macht der Mauer besonders viel Schaden. Ein Schamane stärkt andere Orks.
Oder ein Troll regeneriert zwischen Treffern Lebenspunkte.

Wähle **eine** Idee und beschreibe sie genau. Füge nicht alle gleichzeitig hinzu.

**Eigene Tests:** Ein besiegter Troll darf nicht wiederauferstehen. Heilung darf
`max_leben` nicht überschreiten. Ein Rammbock vor dem Dorf darf noch keinen
Mauerschaden verursachen. Kein Bonus nach dem Ende einer Welle.

## 6 · Rudersdorf schläft nicht: Speichern ★★★

Speichere zwischen Wellen einen Spielstand als JSON. Nutze die Python-Standardbibliothek.

- Speichere einfache Werte: Vorräte, Häuser, Bewohner, Mauer, Welle, Turmart,
  Bauplatz und Stufe. Speichere keine Tkinter-Objekte.
- Prüfe geladene Daten, bevor du den laufenden Spielstand ersetzt.
- Entscheide, wie du mit einer fehlenden oder kaputten Datei umgehst.
- Speichere zunächst nur in Baupausen. Gegner mitten auf dem Weg kommen später.

**Eigene Tests:** Speichern und Laden ergibt denselben Zustand; beschädigtes JSON
beschädigt nicht die aktuelle Partie; unbekannte Turmart und doppelter Bauplatz
werden verständlich gemeldet.

## 7 · Dein eigener Kartenbaukasten ★★★

Erweitere Rudersdorf um ein zweites Tal, eine Brücke oder eine andere Dorfposition.

- Beginne in `welt.py` mit Wegpunkten und Bauplätzen.
- Ein Weg muss mindestens zwei unterschiedliche aufeinanderfolgende Punkte haben.
- Der aktuelle Hintergrund wird separat gezeichnet: Passe ihn zur neuen Karte an.
- Später könntest du mehrere Karten als Daten speichern und auswählbar machen.

**Eigene Tests:** Eine Position am Anfang und Ende liegt auf dem Weg; ein Knick
funktioniert; keine Division durch null bei ungültigen Wegpunkten.

## Deine Idee zählt

Male dein nächstes Gebäude auf Papier. Schreibe darunter:

1. Was kann es?
2. Welche Werte braucht es beim Erstellen?
3. Welche Methode verändert diese Werte?
4. Was ist ein normaler Fall, was ein ungewöhnlicher Fall?
5. Wie kannst du beides ohne Fenster testen?

Damit hast du bereits einen kleinen Entwicklungsplan.
