# Fahrzeug-Cockpit (Virtuelles Tachometer)

## Beschreibung
Dieses Projekt ist eine einfache Simulation eines Fahrzeug-Cockpits mit zwei Tachometern:
- **Geschwindigkeitstacho:** Zeigt die aktuelle Geschwindigkeit in km/h groß und mittig an.
- **Drehzahlmesser (RPM):** Zeigt die aktuelle Drehzahl des Motors an.

Die Werte werden simuliert und automatisch aktualisiert. Beim Erhöhen der Geschwindigkeit wechselt das System automatisch die Gänge und passt die Drehzahl an.

## Technische Details
- Programmiert mit **Python** und **PySide6** (Qt for Python)
- Nutzt **QPainter** zur grafischen Darstellung der Tachometer
- Enthält eine **Animation** für sanfte Zeigerbewegungen
- Automatische Gangwahl mit Anpassung der Drehzahl
- GUI-Anordnung mit **QHBoxLayout** und **QVBoxLayout**

## Hinweis zur Entwicklung
Dieses Projekt wurde mit erheblicher Unterstützung von Künstlicher Intelligenz entwickelt. Die Struktur wurde durch KI generiert, aber manuell verbessert, um lesbareren Code und sinnvollere Variablennamen zu gewährleisten.

## Voraussetzungen
- Python 3.x
- PySide6 (`pip install PySide6`)

## Verwendung
Starte das Programm mit:
```bash
python gauge.py
```

Das Fenster zeigt die Simulation eines Fahrzeugs, das beschleunigt, Gänge wechselt und die Drehzahl anpasst.

