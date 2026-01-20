# Explorative Korrelationsanalyse zur Elektrofahrzeugquote in Deutschland

## Projektüberblick

Dieses Repository enthält die vollständige Datenaufbereitung, Analyse und Visualisierung einer explorativen Korrelationsanalyse auf Kreisebene für Deutschland.  
Untersucht wird der Zusammenhang zwischen der regionalen Elektrofahrzeugquote und verschiedenen sozioökonomischen, demografischen und strukturellen Merkmalen.

Das Projekt ist aus einer vorhergehenden Projektarbeit entstanden, in der ursprünglich spezifische universitätsinterne Daten analysiert werden sollten. Da diese Daten nicht zugänglich waren, wurde der Fokus bewusst auf frei verfügbare amtliche Statistikdaten verlagert. Ziel war es, eine methodisch saubere, nachvollziehbare und reproduzierbare Analyse auf Basis öffentlicher Daten durchzuführen.

---

## Zielsetzung

Ziel des Projekts ist es,

- Zusammenhänge zwischen der Verbreitung von Elektrofahrzeugen und regionalen Strukturmerkmalen sichtbar zu machen,
- diese Zusammenhänge zunächst explorativ über Korrelationen zu untersuchen,
- ausgewählte Befunde anschließend vertiefend mittels Regressionsmodellen zu analysieren,
- und die Ergebnisse anschaulich über kartenbasierte Visualisierungen (GeoJSON) darzustellen.

Ein expliziter theoretischer Rahmen wurde bewusst nicht ausgearbeitet, um den Schwerpunkt klar auf Datenaufbereitung, Analyse und Visualisierung zu legen. Die Fragestellung und Motivation ergeben sich direkt aus der empirischen Ausgangslage.

---

## Datenquellen

Alle verwendeten Daten stammen aus offiziellen, offenen und öffentlich zugänglichen Quellen:

- Statistisches Bundesamt (Destatis)  
  insbesondere über GENESIS-Online sowie Zensus- und Regionalstatistiken
- Statistikportal.de  
  (Gemeinschaftsangebot der Statistischen Ämter des Bundes und der Länder)
- Kraftfahrt-Bundesamt (KBA)  
  insbesondere Fahrzeugbestandsdaten nach Kraftstoffarten auf Kreisebene

Die konkreten Tabellen, Zeitstände und Download-Links können den jeweiligen Notebooks entnommen und bei Bedarf ergänzt werden.

---

## Methodisches Vorgehen

Das methodische Vorgehen folgt einem klaren, datengetriebenen Ablauf:

1. Zusammenführung heterogener amtlicher Datensätze auf Kreisebene  
2. Bereinigung und Harmonisierung unterschiedlicher Formate, Zeitstände und Klassifikationen  
3. Explorative Korrelationsanalyse zwischen Elektrofahrzeugquote und ausgewählten Variablen  
4. Auswahl relevanter Zusammenhänge zur weiterführenden Regressionsanalyse  
5. Visuelle Aufbereitung der Ergebnisse, insbesondere über thematische Karten auf Basis von GeoJSON  

Die Methodik wurde im Vorfeld abgestimmt und im Projektverlauf konsistent umgesetzt.

---

## Repository-Struktur und Notebooks

Die aktuelle Analyse basiert auf zwei zentralen Jupyter-Notebooks:

- **01_Datenladen_und_Harmonisierung.ipynb**  
  Enthält die vollständige Datenbeschaffung, Bereinigung, Harmonisierung und Zusammenführung aller verwendeten Datensätze.

- **02_Analyse_und_Visualisierung.ipynb**  
  Enthält die Korrelationsanalysen, Regressionsmodelle sowie die grafische und kartenbasierte Visualisierung der Ergebnisse.

Zusätzlich befinden sich im Repository ältere Entwurfsnotebooks, die frühere Visualisierungs- und Analyseansätze enthalten. Diese dienen lediglich der Nachvollziehbarkeit des Arbeitsprozesses und sind nicht Bestandteil der finalen Analyse.

Im Repository enthalten sind außerdem:

- das vollständige Paper als PDF,
- alle finalen Visualisierungen zusätzlich als Bilddateien.

--- unter deisem link:https://ws2526unirregesnburgvwlempirischeprojektarbeitsdashboardinter.streamlit.app/fazit 

einen presentations Anwendung als inter aktiver report der Code dafür ist in dem presentation_app Ordner

## Einsatz von KI-Werkzeugen

KI-basierte Werkzeuge wurden gezielt als unterstützende Hilfsmittel eingesetzt, nicht als Ersatz eigenständiger Analysearbeit. Sie kamen insbesondere zum Einsatz bei:

- dem Entwurf und der Strukturierung von Datenverarbeitungs-Pipelines,
- der Recherche und Identifikation relevanter Datensätze,
- dem Einlesen in thematisch verwandte Forschungsliteratur,
- sowie bei der Unterstützung von Code- und Visualisierungsentwürfen.

Verwendet wurden unter anderem:

- OpenAI-Modelle (ChatGPT, Codex-basierte Agenten)
- GitHub Copilot
- Google Gemini
- "Perplexity"

Ein wesentlicher Teil der Arbeit erfolgte über die Diktierfunktion von ChatGPT. Statt klassischem Prompting wurde überwiegend mit natürlicher Sprache, Kontextaufbau (Context Engineering) und frei formulierten Sprachnotizen gearbeitet, um Arbeitsziele, Analyseideen und gewünschte Verarbeitungsschritte zu erläutern. Dieser Ansatz ermöglichte eine sehr direkte und iterative Arbeitsweise.

Die finale Datenaufbereitung, Analyse und Modellierung wurde jedoch eigenständig umgesetzt und überprüft. Insbesondere bei größeren und komplexeren Datensätzen erwies sich manuelle Kontrolle und eigene Implementierung als notwendig, um Fehler und Inkonsistenzen zu vermeiden.

---

## Reproduzierbarkeit und Transparenz

Das Repository ist so aufgebaut, dass:

- alle Verarbeitungsschritte nachvollziehbar sind,
- die verwendeten Datenquellen klar benannt werden,
- Analysen und Visualisierungen reproduzierbar bleiben,
- und die Ergebnisse unabhängig überprüft werden können.

Das Projekt versteht sich ausdrücklich als empirische Analyse auf Basis offener Daten.

---

## Eigenständigkeitserklärung

Die in diesem Repository enthaltenen Analysen, Auswertungen und Darstellungen wurden eigenständig erstellt.  
KI-basierte Werkzeuge wurden unterstützend eingesetzt, insbesondere zur Recherche, Strukturierung und technischen Umsetzung, jedoch nicht zur automatisierten Erstellung der Analyseergebnisse oder zur Ersetzung eigener inhaltlicher Entscheidungen.

Die Verantwortung für Datenaufbereitung, methodische Entscheidungen, Auswertung und Interpretation liegt vollständig beim Autor.

---

## Hinweise

Die dargestellten Ergebnisse stellen keine kausalen Aussagen dar, sondern zeigen statistische Zusammenhänge im Sinne einer explorativen Analyse. Weiterführende Interpretationen bedürfen zusätzlicher theoretischer und methodischer Absicherung.
