from PyQt5.QtWidgets import (QFormLayout, QLineEdit, QComboBox,
                             QPushButton, QMessageBox, QDialog)
from PyQt5.QtGui import QDoubleValidator
from DataManager import DataManager


class LoginDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Login")
        self.setFixedSize(300, 200)
        self.setup_ui()
        self.set_style()

    def setup_ui(self):
        layout = QFormLayout()

        self.login = QLineEdit()
        self.password = QLineEdit()
        self.password.setEchoMode(QLineEdit.Password)

        layout.addRow("Login:", self.login)
        layout.addRow("Password:", self.password)

        self.login_btn = QPushButton("Login")
        self.login_btn.clicked.connect(self.authenticate)
        layout.addRow(self.login_btn)

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
            QLineEdit {
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

    def authenticate(self):
        data_manager = DataManager()
        if data_manager.authenticate_user(self.login.text(),
                                          self.password.text()):
            self.accept()
        else:
            QMessageBox.warning(self, "Error", "Invalid login or password!")