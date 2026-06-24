# qr-code-generator-app
The repository for my QR code generator app.
import sys
import os
import tempfile
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel,
    QLineEdit, QPushButton, QMessageBox, QHBoxLayout
)
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt
import qrcode
from PIL import Image

class QRGeneratorWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Générateur de QR Codes")
        self.setGeometry(300, 300, 800, 800)

        # Widgets
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("Entrez l'URL")

        self.create_button = QPushButton("Créer")
        self.create_button.clicked.connect(self.generate_qr)

        self.back_button = QPushButton("Retour")
        self.back_button.clicked.connect(self.show_url_form)
        self.back_button.hide()

        self.qr_label = QLabel()
        self.qr_label.setAlignment(Qt.AlignCenter)
        self.qr_label.hide()

        self.copy_button = QPushButton("Copier dans le presse-papiers")
        self.copy_button.clicked.connect(self.copy_to_clipboard)
        self.copy_button.hide()

        # Layout
        layout = QVBoxLayout()

        # Layout pour le formulaire
        form_layout = QVBoxLayout()
        form_layout.addWidget(self.url_input)
        form_layout.addWidget(self.create_button)

        # Layout pour le QR code
        qr_layout = QVBoxLayout()
        qr_layout.addWidget(self.qr_label)
        qr_layout.addWidget(self.copy_button)
        qr_layout.addWidget(self.back_button)

        # Ajouter les layouts au layout principal
        layout.addLayout(form_layout)
        layout.addLayout(qr_layout)

        # Widget central
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # Variable pour stocker le chemin temporaire
        self.temp_img_path = None

    def show_url_form(self):
        """Affiche le formulaire d'URL."""
        self.url_input.show()
        self.create_button.show()
        self.qr_label.hide()
        self.copy_button.hide()
        self.back_button.hide()

    def generate_qr(self):
        """Génère le QR code à partir de l'URL."""
        url = self.url_input.text().strip()
        if not url:
            QMessageBox.warning(self, "Erreur", "Veuillez entrer une URL.")
            return

        try:
            # Générer le QR code
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(url)
            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white")

            # Sauvegarder l'image temporairement
            self.temp_img_path = tempfile.NamedTemporaryFile(delete=False, suffix='.png').name
            img.save(self.temp_img_path)

            # Charger l'image dans le label
            pixmap = QPixmap(self.temp_img_path)
            self.qr_label.setPixmap(pixmap)
            self.qr_label.show()

            # Masquer le formulaire et afficher les boutons
            self.url_input.hide()
            self.create_button.hide()
            self.copy_button.show()
            self.back_button.show()

        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Échec de la génération du QR code : {e}")

    def copy_to_clipboard(self):
        """Copie l'image du QR code dans le presse-papiers."""
        if not self.temp_img_path or not os.path.exists(self.temp_img_path):
            QMessageBox.warning(self, "Erreur", "Aucune image à copier.")
            return

        try:
            # Charger l'image avec Qt
            image = QImage(self.temp_img_path)
            clipboard = QApplication.clipboard()
            clipboard.setImage(image)
            QMessageBox.information(self, "Succès", "QR code copié dans le presse-papiers !")
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Échec de la copie : {e}")

    def closeEvent(self, event):
        """Nettoyer le fichier temporaire à la fermeture."""
        if self.temp_img_path and os.path.exists(self.temp_img_path):
            try:
                os.remove(self.temp_img_path)
            except:
                pass
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = QRGeneratorWindow()
    window.show()
    sys.exit(app.exec_())
