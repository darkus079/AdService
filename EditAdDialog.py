from PyQt5.QtWidgets import (QFormLayout, QLineEdit, QComboBox,
                             QPushButton, QMessageBox, QDialog)
from PyQt5.QtGui import QDoubleValidator
from DataManager import DataManager
from typing import Dict


class EditAdDialog(QDialog):
    def __init__(self, ad_data: Dict, parent=None):
        super().__init__(parent)
        self.ad_data = ad_data
        self.setWindowTitle("Edit Ad")
        self.setFixedSize(400, 300)
        self.setup_ui()
        self.set_style()

    def setup_ui(self):
        layout = QFormLayout()

        self.name = QLineEdit(self.ad_data['name'])
        self.description = QLineEdit(self.ad_data['description'])
        self.cost = QLineEdit()
        self.cost.setValidator(QDoubleValidator(0, 999999, 2, self))
        try:
            self.cost.setText(f"{float(self.ad_data['cost']):.2f}")
        except (ValueError, TypeError):
            self.cost.setText("0.00")
        self.category = QComboBox()
        self.category.addItems(
            ["Electronics", "Clothing", "Furniture", "Vehicles", "Other"])
        self.category.setCurrentText(self.ad_data['category'])

        layout.addRow("Name:", self.name)
        layout.addRow("Description:", self.description)
        layout.addRow("Cost ($):", self.cost)
        layout.addRow("Category:", self.category)

        self.save_btn = QPushButton("Save")
        self.save_btn.clicked.connect(self.save_ad)
        layout.addRow(self.save_btn)

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
                background-color: #2196F3;
                color: white;
                border: none;
                padding: 10px;
                font-size: 14px;
                border-radius: 4px;
                margin-top: 10px;
            }
            QPushButton:hover {
                background-color: #0b7dda;
            }
        """)

    def save_ad(self):
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
            QMessageBox.warning(self, "Error", "Name cannot be empty!")
            return

        updated_data = {
            'name': self.name.text(),
            'description': self.description.text(),
            'cost': f"{cost:.2f}",
            'category': self.category.currentText()
        }

        DataManager().update_ad(self.ad_data['id'], updated_data)
        self.accept()