import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QHBoxLayout, QVBoxLayout, QWidget, QLabel
from PySide6.QtGui import QPainter, QPen, QFont, QColor
from PySide6.QtCore import Qt, QTimer, QVariantAnimation
import math
import random

class Tachometer(QWidget):
    def __init__(self, anzeige_name, min_wert=0, max_wert=220, start_wert=0, parent=None):
        super().__init__(parent)
        self.anzeige_name = anzeige_name  # Name der Anzeige (z. B. Speed oder RPM)
        self.min_wert = min_wert  # Minimaler Wert
        self.max_wert = max_wert  # Maximaler Wert
        self.aktueller_wert = float(start_wert) if start_wert is not None else 0.0  # Aktueller Wert
        self.ziel_wert = float(start_wert) if start_wert is not None else 0.0  # Zielwert für die Animation
        self.einheit = "km/h" if anzeige_name == "Geschwindigkeit" else "RPM"  # Einheit für Anzeige
        self.setFixedSize(320, 340)
        
        # Animationssteuerung für flüssige Zeigerbewegungen
        self.animation = QVariantAnimation()
        self.animation.setDuration(500)
        self.animation.setStartValue(self.aktueller_wert)
        self.animation.setEndValue(self.aktueller_wert)
        self.animation.valueChanged.connect(self.setze_wert)

    def setze_wert(self, wert):
        if wert is not None:
            self.aktueller_wert = max(self.min_wert, min(self.max_wert, wert))
            self.update()
    
    def aktualisiere_wert(self, wert):
        if wert is not None:
            wert = max(self.min_wert, min(self.max_wert, wert))
            self.animation.setStartValue(self.aktueller_wert)
            self.animation.setEndValue(wert)
            self.animation.start()
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Hintergrund zeichnen
        painter.setPen(Qt.NoPen)
        painter.setBrush(Qt.black)
        painter.drawEllipse(10, 10, 300, 300)
        
        # Innerer Kreis zur Deko
        painter.setBrush(QColor(80, 80, 80))
        painter.drawEllipse(90, 90, 140, 140)
        
        # Zeigerbewegung berechnen
        if self.aktueller_wert is not None:
            winkel = (self.aktueller_wert - self.min_wert) / (self.max_wert - self.min_wert) * 270 - 135
            x = 160 + 140 * math.cos(math.radians(winkel))
            y = 160 + 140 * math.sin(math.radians(winkel))
            painter.setPen(QPen(Qt.red, 4))
            painter.drawLine(160 + 75 * math.cos(math.radians(winkel)), 160 + 75 * math.sin(math.radians(winkel)), x, y)
        
        # Schriftart und Farbe setzen
        font = QFont()
        painter.setPen(Qt.white)
        
        # Geschwindigkeit in der Mitte groß anzeigen
        if self.anzeige_name == "Geschwindigkeit":
            font.setPointSize(42)
            painter.setFont(font)
            painter.drawText(self.width()//2 - 35, self.height()//2 - 10, f"{int(self.aktueller_wert)}")
            font.setPointSize(18)
            painter.setFont(font)
            painter.drawText(self.width()//2 - 15, self.height()//2 + 20, "km/h")
        # Drehzahl kleiner anzeigen
        elif self.anzeige_name == "RPM":
            font.setPointSize(32)
            painter.setFont(font)
            painter.drawText(self.width()//2 - 35, self.height()//2 - 10, f"{int(self.aktueller_wert)}")
            font.setPointSize(18)
            painter.setFont(font)
            painter.drawText(self.width()//2 - 15, self.height()//2 + 20, "RPM")

class FahrzeugCockpit(QMainWindow):
    aktueller_gang = 1  # Variable für den aktuellen Gang

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Fahrzeug-Cockpit")
        self.setFixedSize(1200, 400)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        haupt_layout = QHBoxLayout()
        self.central_widget.setLayout(haupt_layout)

        # Drehzahlmesser (RPM) links
        rpm_layout = QVBoxLayout()
        self.rpm_tacho = Tachometer("RPM", min_wert=0, max_wert=8000, start_wert=800)
        rpm_layout.addWidget(self.rpm_tacho, alignment=Qt.AlignBottom)
        
        # Geschwindigkeitstacho rechts
        speed_layout = QVBoxLayout()
        self.speed_tacho = Tachometer("Geschwindigkeit", min_wert=0, max_wert=220, start_wert=0)
        speed_layout.addWidget(self.speed_tacho, alignment=Qt.AlignBottom)
        
        # Platzhalter für Navi o. Ä.
        platzhalter = QLabel("Navigation Platzhalter")
        platzhalter.setAlignment(Qt.AlignCenter)
        platzhalter.setStyleSheet("background-color: gray; color: white; font-size: 16px;")
        platzhalter.setFixedSize(520, 320)
        
        haupt_layout.addLayout(rpm_layout)
        haupt_layout.addWidget(platzhalter, alignment=Qt.AlignVCenter)
        haupt_layout.addLayout(speed_layout)
        
        # Timer für Simulation
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.simuliere_fahrt)
        self.timer.start(100)
        
        self.geschwindigkeit = 0
        self.drehzahl = 800
    
    def simuliere_fahrt(self):
        # Geschwindigkeit erhöhen
        if self.geschwindigkeit < 100:
            self.geschwindigkeit += random.uniform(0.5, 2.5)
            self.drehzahl = max(800, min(8000, 800 + (self.geschwindigkeit * 60)))
        
        vorheriger_gang = FahrzeugCockpit.aktueller_gang
        
        # Ganglogik
        if self.geschwindigkeit < 20:
            FahrzeugCockpit.aktueller_gang = 1
        elif self.geschwindigkeit < 40:
            FahrzeugCockpit.aktueller_gang = 2
        elif self.geschwindigkeit < 60:
            FahrzeugCockpit.aktueller_gang = 3
        elif self.geschwindigkeit < 80:
            FahrzeugCockpit.aktueller_gang = 4
        elif self.geschwindigkeit < 100:
            FahrzeugCockpit.aktueller_gang = 5
        else:
            FahrzeugCockpit.aktueller_gang = 6
        
        # Falls der Gang sich ändert, Drehzahl senken
        if FahrzeugCockpit.aktueller_gang != vorheriger_gang:
            self.drehzahl = max(800, self.drehzahl - 1500)
        
        self.speed_tacho.aktualisiere_wert(self.geschwindigkeit)
        self.rpm_tacho.aktualisiere_wert(self.drehzahl)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    fenster = FahrzeugCockpit()
    fenster.show()
    sys.exit(app.exec())
