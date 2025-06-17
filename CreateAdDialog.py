from PyQt5.QtWidgets import (QFormLayout, QLineEdit, QComboBox,
                             QPushButton, QMessageBox, QDialog)
from PyQt5.QtGui import QDoubleValidator
from DataManager import DataManager


class CreateAdDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Create New Ad")
        self.setFixedSize(400, 300)
        self.setup_ui()
        self.set_style()

    def setup_ui(self):
        layout = QFormLayout()

        self.name = QLineEdit()
        self.description = QLineEdit()
        self.cost = QLineEdit()
        self.cost.setValidator(QDoubleValidator(0, 999999, 2, self))
        self.category = QComboBox()
        self.category.addItems(
            ["Electronics", "Clothing", "Furniture", "Vehicles", "Other"])

        layout.addRow("Name:", self.name)
        layout.addRow("Description:", self.description)
        layout.addRow("Cost ($):", self.cost)
        layout.addRow("Category:", self.category)

        self.create_btn = QPushButton("Create")
        self.create_btn.clicked.connect(self.create_ad)
        layout.addRow(self.create_btn)

        self.setLayout(layout)

    def set_style(self):
        self.setStyleSheet("""
            QDialog {
                background-color: #f5f5f5;
            }
            QLabel {
                font-size: 14px;
                color: #333;
            }
            QLineEdit, QComboBox {
                padding: 8px;
                border: 1px solid #ddd;
                border-radius: 4px;
                font-size: 14px;
                background-color: white;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 10px;
                font-size: 14px;
                border-radius: 4px;
                margin-top: 10px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)

    def create_ad(self):
        try:
            cost = float(self.cost.text())
            if cost < 0:
                QMessageBox.warning(self, "Error", "Cost cannot be negative!")
                return
        except ValueError:
            QMessageBox.warning(self, "Error",
                                "Please enter a valid number for cost!")
            return

        if not self.name.text():
            QMessageBox.warning(self, "Error ", "Name cannot be empty!")
            return

        ad_data = {
            'name': self.name.text(),
            'description': self.description.text(),
            'cost': f"{cost:.2f}",
            'category': self.category.currentText()
        }

        DataManager().add_ad(ad_data)
        self.accept()