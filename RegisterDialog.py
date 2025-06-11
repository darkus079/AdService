from PyQt5.QtWidgets import (QFormLayout, QLineEdit, QComboBox, QPushButton,
                             QMessageBox, QDialog, QDateEdit)
from PyQt5.QtGui import QDoubleValidator
from PyQt5.QtCore import QDate
from DataManager import DataManager


class RegisterDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Register")
        self.setFixedSize(400, 400)
        self.setup_ui()
        self.set_style()

    def setup_ui(self):
        layout = QFormLayout()

        self.first_name = QLineEdit()
        self.last_name = QLineEdit()
        self.birth_date = QDateEdit()
        self.birth_date.setCalendarPopup(True)
        self.birth_date.setDate(QDate(2000, 1, 1))
        self.email = QLineEdit()
        self.login = QLineEdit()
        self.password = QLineEdit()
        self.password.setEchoMode(QLineEdit.Password)
        self.repeat_password = QLineEdit()
        self.repeat_password.setEchoMode(QLineEdit.Password)

        layout.addRow("First Name:", self.first_name)
        layout.addRow("Last Name:", self.last_name)
        layout.addRow("Birth Date:", self.birth_date)
        layout.addRow("Email:", self.email)
        layout.addRow("Login:", self.login)
        layout.addRow("Password:", self.password)
        layout.addRow("Repeat Password:", self.repeat_password)

        self.register_btn = QPushButton("Register")
        self.register_btn.clicked.connect(self.register)
        layout.addRow(self.register_btn)

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
            QLineEdit, QDateEdit {
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

    def register(self):
        data_manager = DataManager()

        if self.password.text() != self.repeat_password.text():
            QMessageBox.warning(self, "Error", "Passwords do not match!")
            return

        if not all(c.isalnum() for c in self.password.text()):
            QMessageBox.warning(self, "Error",
                                "Password can only contain letters and numbers!")
            return

        user_data = {
            'first_name': self.first_name.text(),
            'last_name': self.last_name.text(),
            'birth_date': self.birth_date.date().toString("yyyy-MM-dd"),
            'email': self.email.text(),
            'login': self.login.text(),
            'password': self.password.text()
        }

        if data_manager.register_user(user_data):
            QMessageBox.information(self, "Success",
                                    "Registration successful!")
            self.accept()
        else:
            QMessageBox.warning(self, "Error", "Login already exists!")