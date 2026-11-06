# Wegweiser für ein größeres Rudersdorf

## Drei Teile mit klaren Aufgaben

```text
modell.py                 Die Regeln: Was passiert bei einem Treffer oder Kauf?
       ↑
spielkern.py + welt.py     Der Ablauf: Wann erscheint ein Gegner, wann endet eine Welle?
       ↑
oberflaeche.py             Die Ansicht: Was wird gezeichnet, welchen Knopf klickst du?
```

Der Spielkern erhält das Modell beim Erstellen: `Spiel(modell)`.
`spielen.py --loesung` übergibt ausdrücklich `loesung.modell`.
So laufen Lernstand und Referenz mit derselben Karte und derselben Spielschleife.
Es gibt keinen automatischen Rückgriff auf gelöste Pflichtaufgaben.
Nur das ausdrücklich optionale `sammle_einkommen` darf `NotImplementedError` werfen,
ohne die Wellen zu unterbrechen: Die Grundversorgung ist bereits vorhanden.

## Eine neue Gegnerart

Für eine neue Kombination aus Name, Leben, Tempo und Gold reicht ein Eintrag in
`welt.MONSTER`. Verwende den neuen Schlüssel in einer Liste von `welt.WELLEN`.
Die neue Art wird zunächst mit dem normalen Ork-Symbol gezeichnet und verursacht
1 Dorfschaden. Besondere Darstellung ergänzt du in `Fenster.zeichne_gegner`.

Für **besonderes Verhalten** wie Rüstung brauchst du zusätzlich eine Unterklasse.
Der Schlüssel `"klasse"` in `welt.MONSTER` nennt sie; `Spiel.starte_welle` sucht sie
im Modell (so entstehen Schildork und Troll aus Teil 2). Der Dorfschaden beim
Durchbruch steht als `"dorfschaden"` ebenfalls in den Gegnerdaten.
`welt.WELLEN_STAERKE` multipliziert die Lebenspunkte jeder Welle.

## Eine neue Turmart

1. Ergänze die Klasse in deinem Modell, möglichst als Unterklasse von `Turm`.
2. Ergänze einen Bauplan in `welt.BAUPLAENE` mit `name`, `klasse`, `kosten`, `farbe`, `kurz`.
3. Ergänze ihre Zeichnung in `Fenster.zeichne_turm`.
4. Die Seitenleiste zeigt Turmarten als 2×2-Raster (`Fenster.zeichne_seitenleiste`).
   Für eine fünfte Art brauchst du eine dritte Reihe: Rücke den Dorfbereich nach unten.
5. Ergänze bei Bedarf ein neues Tastenkürzel, einen `KURZNAMEN`-Eintrag und Verhaltenstests.

Die Spielschleife kennt nur Zielauswahl, Treffer und Nachladezeit.
Eine neue Trefferwirkung braucht deshalb normalerweise keine neue Schleife.

## Ein neues Gebäude

`Dorf` aus Teil 1 hält Vorräte und einfache Zähler. Das `Dorf` aus Teil 2 erbt davon
und hat eine Gebäudeliste; jedes `Gebaeude` kennt seinen Ertrag. Ein neuer Gebäudetyp
braucht einen Eintrag in `welt.GEBAEUDE`, zwei Plätze in `GEBAEUDEPLAETZE` und eine
Zeichnung in `Fenster.gebaeude`. Die Seitenleiste ergänzt den Knopf automatisch,
hat aber nur Platz für sechs Dorfknöpfe.

Halte die Berechnung des Einkommens im Modell. Zeichnungen und Animationen dürfen
keine Rohstoffe erzeugen: Sonst beeinflusst die Bildrate den Kontostand.
Die Schaltfläche wird in `Fenster.zeichne` ergänzt, die Zeichnung in `zeichne_dorf`.
Der Spielkern erlaubt Dorfaktionen und Upgrades nur in Baupausen.

## Eine neue Partie-Regel

`Spiel.phase` ist eines von `bauen`, `welle`, `sieg`, `verloren`.
`pause` hält die laufende Welle an. Türme lassen sich auch während eines Angriffs bauen;
Mauer, Häuser und Upgrades nur zwischen Wellen. Neustart erstellt einen frischen Spielkern.

Der Weg besteht aus Punkten; `weg_position` rechnet zurückgelegte Strecke in eine
Position um. Gegner speichern zusätzlich ihre Strecke als `fortschritt`, sodass
die Zielauswahl nicht von einer zufälligen Bildschirmentfernung abhängt.

## Grenzen des jetzigen Rahmens

- Feste Fenstergröße 1180 × 760, keine Kamera oder Zoomfunktion.
- Ein Weg, neun Bauplätze, zehn von Hand zusammengestellte Wellen.
- Eine Mauer als gemeinsamer Schutzvorrat; keine einzeln platzierbaren Mauersegmente.
- Dorfbewohner bewegen sich dekorativ. Sie haben noch keine Berufe oder eigene Simulation.
- Bis zu acht Häuser und zwanzig Bewohner werden gezeichnet; die Wirtschaft zählt alle.
- Speichern nur in Baupausen und nur ein Spielstand; kein Sound, kein Internet, keine Zusatzpakete.
- Die Uhr nutzt kleine Zeitschritte. Nach langem Fensterstillstand holt das Spiel
  nicht die gesamte verstrichene Zeit nach; das ist für ein Lernspiel angenehmer.

Das sind bewusst überschaubare Ausgangspunkte für die Knobelaufgaben.
