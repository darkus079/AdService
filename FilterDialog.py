from PyQt5.QtWidgets import (QFormLayout, QLineEdit, QComboBox,
                             QPushButton, QMessageBox, QDialog,
                             QVBoxLayout, QHBoxLayout,
                             QGroupBox, QGridLayout, QCheckBox,
                             QDoubleSpinBox, QAbstractSpinBox, QDateEdit)
from PyQt5.QtGui import QDoubleValidator
from PyQt5.QtCore import pyqtSignal, QDate
from DataManager import DataManager


class FilterDialog(QDialog):
    filters_reset = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Filter Ads")
        self.setFixedSize(500, 600)
        self.setup_ui()
        self.set_style()

    def setup_ui(self):
        layout = QVBoxLayout()

        user_group = QGroupBox("Filter by Owner")
        user_layout = QFormLayout()
        self.user_login = QLineEdit()
        self.user_login.setPlaceholderText("Enter user login")
        user_layout.addRow("User Login:", self.user_login)
        user_group.setLayout(user_layout)

        category_group = QGroupBox("Filter by Category")
        category_layout = QVBoxLayout()
        self.category_checks = []
        categories = ["Electronics", "Clothing", "Furniture", "Vehicles",
                      "Other"]

        grid_layout = QGridLayout()
        row, col = 0, 0
        for category in categories:
            check = QCheckBox(category)
            check.setChecked(True)
            self.category_checks.append(check)
            grid_layout.addWidget(check, row, col)
            col += 1
            if col > 1:
                col = 0
                row += 1

        category_layout.addLayout(grid_layout)
        category_group.setLayout(category_layout)

        cost_group = QGroupBox("Filter by Cost Range ($)")
        cost_layout = QFormLayout()

        self.min_cost = QDoubleSpinBox()
        self.min_cost.setRange(0, 9999999999)
        self.min_cost.setValue(0)
        self.min_cost.setSingleStep(10)
        self.min_cost.setDecimals(2)
        self.min_cost.setPrefix("$ ")
        self.min_cost.setButtonSymbols(QAbstractSpinBox.UpDownArrows)

        self.max_cost = QDoubleSpinBox()
        self.max_cost.setRange(0.01, 99999999999)
        self.max_cost.setValue(9999999999)
        self.max_cost.setSingleStep(10)
        self.max_cost.setDecimals(2)
        self.max_cost.setPrefix("$ ")
        self.max_cost.setButtonSymbols(QAbstractSpinBox.UpDownArrows)

        cost_layout.addRow("Minimum cost:", self.min_cost)
        cost_layout.addRow("Maximum cost:", self.max_cost)
        cost_group.setLayout(cost_layout)

        date_group = QGroupBox("Filter by Date Range")
        date_layout = QFormLayout()

        self.from_date = QDateEdit()
        self.from_date.setDate(QDate.currentDate().addDays(-30))
        self.from_date.setCalendarPopup(True)
        self.from_date.setDisplayFormat("MMM d, yyyy")

        self.to_date = QDateEdit()
        self.to_date.setDate(QDate.currentDate())
        self.to_date.setCalendarPopup(True)
        self.to_date.setDisplayFormat("MMM d, yyyy")

        date_layout.addRow("From date:", self.from_date)
        date_layout.addRow("To date:", self.to_date)
        date_group.setLayout(date_layout)
        layout.addWidget(user_group)

        button_layout = QHBoxLayout()
        self.reset_btn = QPushButton("Reset Filters")
        self.reset_btn.clicked.connect(self.reset_filters)
        self.apply_btn = QPushButton("Apply Filters")
        self.apply_btn.clicked.connect(self.accept)
        button_layout.addWidget(self.reset_btn)
        button_layout.addWidget(self.apply_btn)

        layout.addWidget(category_group)
        layout.addWidget(cost_group)
        layout.addWidget(date_group)
        layout.addLayout(button_layout)
        self.setLayout(layout)

    def reset_filters(self):
        for check in self.category_checks:
            check.setChecked(True)
        self.min_cost.setValue(0)
        self.max_cost.setValue(99999)
        self.from_date.setDate(QDate.currentDate().addDays(-30))
        self.to_date.setDate(QDate.currentDate())
        self.filters_reset.emit()

    def set_style(self):
        self.setStyleSheet("""
            QDialog {
                background-color: #f5f5f5;
                font-size: 14px;
            }
            QGroupBox {
                border: 1px solid #ddd;
                border-radius: 4px;
                margin-top: 10px;
                font-weight: bold;
                color: #333;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 3px;
                color: #333;
            }
            QCheckBox {
                spacing: 10px;
                padding: 8px;
                min-height: 20px;
                color: #333;
                font-size: 14px;
            }
            QDoubleSpinBox, QDateEdit, QLineEdit {
                padding: 8px;
                border: 1px solid #ddd;
                border-radius: 4px;
                min-width: 120px;
                min-height: 30px;
                background-color: white;
                color: #333;
                font-size: 14px;
            }
            QLabel {
                color: #333;
                font-size: 14px;
            }
            QPushButton {
                padding: 8px 16px;
                font-size: 14px;
                border-radius: 4px;
                min-width: 100px;
            }
            QPushButton#apply_btn {
                background-color: #4CAF50;
                color: white;
            }
            QPushButton#reset_btn {
                background-color: #f44336;
                color: white;
            }
        """)
        self.apply_btn.setObjectName("apply_btn")
        self.reset_btn.setObjectName("reset_btn")

    def get_current_filters(self):
        return {
            'categories': [check.text() for check in self.category_checks if check.isChecked()],
            'cost_range': (self.min_cost.value(), self.max_cost.value()),
            'date_range': (
                self.from_date.date().toString("yyyy-MM-dd"),
                self.to_date.date().toString("yyyy-MM-dd")
            ),
            'owner_login': self.user_login.text().strip()
        }