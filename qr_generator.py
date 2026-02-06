import sys
import qrcode
from PIL import Image
from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit,
    QPushButton, QFileDialog, QVBoxLayout, QMessageBox
)

from PySide6.QtGui import QPixmap
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt


class QRGenerator(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QR Code Generator with Logo")
        self.setFixedSize(600, 300)
        
        # 🎨 Modern Dark UI
        self.setStyleSheet("""
            QWidget {
                background-color: #0f172a;
                color: #e5e7eb;
                font-family: Segoe UI;
                font-size: 14px;
            }
            QLabel {
                font-size: 15px;
            }
            QLabell {
                font-size: 15px;
            }
            QLineEdit {
                padding: 12px 5px;
                border-radius: 10px;
                background-color: #020617;
                border: 1px solid #334155;
                color: white;
            }
            QPushButton {
                padding: 12px 25px;
                border-radius: 10px;
                background-color: #22c55e;
                color: black;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #16a34a;
            }
        """)

        layout = QVBoxLayout()
        layout.setSpacing(5)

        #icon
        image_label = QLabel()
        image_label.setAlignment(Qt.AlignCenter)
        pixmap = QPixmap("icon.png")
        image_label.setPixmap(
            pixmap.scaled(
                50, 50,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
        )

        # 🔤 Label
        self.label = QLabel("QR Generator")
        self.label.setAlignment(Qt.AlignCenter)

        # 🧾 Textbox
        self.input_link = QLineEdit()
        self.input_link.setPlaceholderText('Enter your link : "https://example.com"')

         # 🔤 Label
        self.label_test = QLabel("test")
        self.label_test.setAlignment(Qt.AlignLeft)

        # 🔘 Button: Insert Logo
        self.btn_insert_logo = QPushButton(" Insert Logo Image")
        self.btn_insert_logo.setIcon(QIcon("qr.png"))  # optional
        self.btn_insert_logo.clicked.connect(self.insert_logo)

        # 🔘 Button: Generate QR
        self.btn_generate = QPushButton(" Generate QR Code")
        self.btn_generate.setIcon(QIcon("qr.png"))  # optional
        self.btn_generate.clicked.connect(self.generate_qr)
        
         # 🔤 Label
       # 🔤 Label
        self.label_test = QLabel(" Copyright © 2026 CDDE v01.")
        self.label_test.setAlignment(Qt.AlignCenter)

        layout.addWidget(image_label)
        layout.addWidget(self.label)
        layout.addWidget(self.input_link)
        layout.addWidget(self.btn_insert_logo)
        layout.addStretch()
        layout.addWidget(self.btn_generate)
        layout.addWidget(self.label_test)
        self.setLayout(layout)

    def insert_logo(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Logo Image",
            "",
            "Image Files (*.png *.jpg *.bmp)"
        )
        if file_path:
            self.logo_path = file_path
            QMessageBox.information(self, "Logo Selected", f"Logo: {file_path}")

    def generate_qr(self):
        link = self.input_link.text().strip()
        if not link:
            QMessageBox.warning(self, "Error", "Please enter a link.")
            return

        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save QR Code",
            "qr_code.png",
            "PNG Files (*.png)"
        )
        if not file_path:
            return

        qr = qrcode.QRCode(
            version=4,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=12,
            border=2
        )
        qr.add_data(link)
        qr.make(fit=True)
        qr_img = qr.make_image(fill_color="black", back_color="white").convert("RGB")

        # embed logo if selected
        if self.logo_path:
            logo = Image.open(self.logo_path)

            # resize logo
            qr_width, qr_height = qr_img.size
            factor = 4  # logo size ratio
            logo_size = qr_width // factor
            logo = logo.resize((logo_size, logo_size))

            # center logo
            pos = ((qr_width - logo_size) // 2, (qr_height - logo_size) // 2)
            qr_img.paste(logo, pos, mask=logo if logo.mode == 'RGBA' else None)

        qr_img.save(file_path)
        QMessageBox.information(self, "Success", "QR Code generated successfully!")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = QRGenerator()
    window.show()
    sys.exit(app.exec())
