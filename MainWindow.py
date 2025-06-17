from datetime import datetime
from typing import List, Dict
from PyQt5.QtWidgets import (QWidget, QStackedWidget, QVBoxLayout, QHBoxLayout,
                             QMainWindow, QPushButton, QListWidget, QComboBox,
                             QDialog, QMessageBox, QListWidgetItem, QLabel)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QColor, QPalette
from DataManager import DataManager
from SortContext import SortContext
from SortByName import SortByName
from SortByDate import SortByDate
from SortByCost import SortByCost
from SortByPopularity import SortByPopularity
from CreateAdDialog import CreateAdDialog
from EditAdDialog import EditAdDialog
from FilterDialog import FilterDialog
from LoginDialog import LoginDialog
from RegisterDialog import RegisterDialog


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ad Service")
        self.setMinimumSize(800, 600)
        self.data_manager = DataManager()
        self.sort_context = SortContext(SortByName())
        self.current_displayed_ads = []
        self.sort_ascending = True
        self.setup_ui()
        self.update_theme("#f5f5f5", "#333", "#2196F3")
        self.show_login()

    def setup_ui(self):
        self.central_widget = QStackedWidget()
        self.setCentralWidget(self.central_widget)

        self.login_screen = QWidget()
        login_layout = QVBoxLayout()

        self.welcome_label = QLabel("Welcome to Ad Service")
        self.welcome_label.setAlignment(Qt.AlignCenter)
        self.welcome_label.setFont(QFont("Arial", 18, QFont.Bold))

        btn_layout = QHBoxLayout()
        self.login_btn = QPushButton("Login")
        self.login_btn.clicked.connect(self.show_login_dialog)
        self.register_btn = QPushButton("Register")
        self.register_btn.clicked.connect(self.show_register_dialog)

        btn_layout.addWidget(self.login_btn)
        btn_layout.addWidget(self.register_btn)

        login_layout.addWidget(self.welcome_label)
        login_layout.addLayout(btn_layout)
        self.login_screen.setLayout(login_layout)

        self.main_screen = QWidget()
        main_layout = QVBoxLayout()

        header_layout = QHBoxLayout()
        self.greeting_label = QLabel()
        self.greeting_label.setFont(QFont("Arial", 14))
        self.logout_btn = QPushButton("Logout")
        self.logout_btn.clicked.connect(self.logout)
        header_layout.addWidget(self.greeting_label)
        header_layout.addStretch()
        header_layout.addWidget(self.logout_btn)

        self.ads_list = QListWidget()
        self.ads_list.itemDoubleClicked.connect(self.show_ad_details)

        controls_layout = QHBoxLayout()
        self.sort_combo = QComboBox()
        self.sort_combo.addItems(
            ["Sort by Name", "Sort by Date", "Sort by Cost",
             "Sort by Popularity"])
        self.sort_combo.currentIndexChanged.connect(self.update_sort_strategy)

        self.sort_direction_btn = QPushButton("Ascending")
        self.sort_direction_btn.clicked.connect(self.toggle_sort_direction)

        self.filter_btn = QPushButton("Filter Ads")
        self.filter_btn.clicked.connect(self.show_filter_dialog)

        self.create_ad_btn = QPushButton("Create New Ad")
        self.create_ad_btn.clicked.connect(self.show_create_ad_dialog)

        self.my_ads_btn = QPushButton("My Ads")
        self.my_ads_btn.setCheckable(True)
        self.my_ads_btn.clicked.connect(self.handle_my_ads)

        self.all_ads_btn = QPushButton("All Ads")
        self.all_ads_btn.setCheckable(True)
        self.all_ads_btn.setChecked(True)
        self.all_ads_btn.clicked.connect(self.handle_all_ads)

        controls_layout.addWidget(QLabel("Sort by:"))
        controls_layout.addWidget(self.sort_combo)
        controls_layout.addWidget(self.sort_direction_btn)
        controls_layout.addWidget(self.filter_btn)
        controls_layout.addWidget(self.create_ad_btn)
        controls_layout.addWidget(self.my_ads_btn)
        controls_layout.addWidget(self.all_ads_btn)

        main_layout.addLayout(header_layout)
        main_layout.addWidget(self.ads_list)
        main_layout.addLayout(controls_layout)
        self.main_screen.setLayout(main_layout)

        self.central_widget.addWidget(self.login_screen)
        self.central_widget.addWidget(self.main_screen)

    def update_theme(self, bg_color, text_color, accent_color):
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(bg_color))
        palette.setColor(QPalette.WindowText, QColor(text_color))
        palette.setColor(QPalette.Button, QColor(accent_color))
        palette.setColor(QPalette.ButtonText, QColor("white"))
        self.setPalette(palette)

        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {accent_color};
                color: white;
                border: none;
                padding: 8px 16px;
                font-size: 14px;
                border-radius: 4px;
            }}
            QPushButton:hover {{
                background-color: {QColor(accent_color).darker(120).name()};
            }}
            QListWidget {{
                background-color: white;
                border: 1px solid #ddd;
                border-radius: 4px;
            }}
        """)

    def show_login(self):
        self.central_widget.setCurrentWidget(self.login_screen)
        self.show()

    def show_main(self):
        user_data = self.data_manager.users[self.data_manager.current_user]
        self.greeting_label.setText(
            f"Welcome, {user_data['first_name']} {user_data['last_name']}!")
        self.handle_all_ads()
        self.central_widget.setCurrentWidget(self.main_screen)

    def show_login_dialog(self):
        dialog = LoginDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            self.show_main()

    def show_register_dialog(self):
        dialog = RegisterDialog(self)
        dialog.exec_()

    def show_create_ad_dialog(self):
        dialog = CreateAdDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            self.update_ads_list()

    def show_edit_ad_dialog(self, ad_data: Dict):
        dialog = EditAdDialog(ad_data, self)
        if dialog.exec_() == QDialog.Accepted:
            self.update_ads_list()

    def show_filter_dialog(self):
        dialog = FilterDialog(self)
        dialog.filters_reset.connect(self.handle_reset_filters)

        if dialog.exec_() == QDialog.Accepted:
            filters = dialog.get_current_filters()
            self.apply_filters(filters)

    def handle_reset_filters(self):
        if self.my_ads_btn.isChecked():
            self.handle_my_ads()
        else:
            self.handle_all_ads()

    def handle_all_ads(self):
        self.all_ads_btn.setChecked(True)
        self.my_ads_btn.setChecked(False)
        self.update_ads_list()

    def handle_my_ads(self):
        self.my_ads_btn.setChecked(True)
        self.all_ads_btn.setChecked(False)
        if hasattr(self, 'current_filters'):
            self.current_filters['owner_login'] = ''
        self.update_ads_list()

    def apply_filters(self, filters: Dict):
        if self.my_ads_btn.isChecked():
            base_ads = self.data_manager.get_user_ads()
        else:
            base_ads = self.data_manager.get_all_ads()

        filtered_ads = []
        for ad in base_ads:
            if self.my_ads_btn.isChecked() and ad.get(
                    'owner') != self.data_manager.current_user:
                continue

            if filters['owner_login'] and ad.get('owner') != filters[
                'owner_login']:
                continue

            if not filters['categories'] or ad.get('category') not in filters[
                'categories']:
                continue

            try:
                cost = float(ad.get('cost', 0))
                if not (filters['cost_range'][0] <= cost <=
                        filters['cost_range'][1]):
                    continue
            except ValueError:
                continue

            try:
                ad_date = datetime.strptime(ad.get('date', ''),
                                            "%Y-%m-%d %H:%M:%S").date()
                from_date = datetime.strptime(filters['date_range'][0],
                                              "%Y-%m-%d").date()
                to_date = datetime.strptime(filters['date_range'][1],
                                            "%Y-%m-%d").date()
                if not (from_date <= ad_date <= to_date):
                    continue
            except ValueError:
                continue

            filtered_ads.append(ad)

        self.current_displayed_ads = filtered_ads
        self.apply_current_sort()

    def toggle_sort_direction(self):
        self.sort_ascending = not self.sort_ascending
        self.sort_direction_btn.setText(
            "Ascending" if self.sort_ascending else "Descending")
        self.update_sort_strategy()

    def update_sort_strategy(self):
        index = self.sort_combo.currentIndex()
        if index == 0:
            strategy = SortByName(ascending=self.sort_ascending)
        elif index == 1:
            strategy = SortByDate(ascending=self.sort_ascending)
        elif index == 2:
            strategy = SortByCost(ascending=self.sort_ascending)
        elif index == 3:
            strategy = SortByPopularity(ascending=self.sort_ascending)

        self.sort_context.set_strategy(strategy)
        self.apply_current_sort()

    def apply_current_sort(self):
        if not self.current_displayed_ads:
            return

        sorted_ads = self.sort_context.sort_ads(self.current_displayed_ads)
        self.display_sorted_ads(sorted_ads)

    def display_sorted_ads(self, sorted_ads: List):
        self.ads_list.clear()
        try:
            for ad in sorted_ads:
                if not all(key in ad for key in ['name', 'cost', 'category']):
                    continue

                try:
                    item_text = f"{ad['name']} - ${float(ad['cost']):.2f} ({ad['category']})"
                    item = QListWidgetItem(item_text)
                    item.setData(Qt.UserRole, ad)

                    if ad.get('owner') == self.data_manager.current_user:
                        item.setForeground(QColor("#2196F3"))

                    self.ads_list.addItem(item)
                except (ValueError, KeyError) as e:
                    print(f"Error displaying ad: {e}")
                    continue
        except Exception as e:
            print(f"Error displaying sorted ads: {e}")
            self.ads_list.addItem("Error displaying ads")

    def update_ads_list(self):
        if hasattr(self, 'current_filters'):
            self.apply_filters(self.current_filters)
        elif self.my_ads_btn.isChecked():
            ads = self.data_manager.get_user_ads()
            self.display_ads(ads)
        else:
            ads = self.data_manager.get_all_ads()
            self.display_ads(ads)

    def show_ad_details(self, item):
        ad_data = item.data(Qt.UserRole)
        self.data_manager.increment_popularity(ad_data['id'])

        owner_login = ad_data.get('owner', '')
        owner_name = ""
        if owner_login in self.data_manager.users:
            user = self.data_manager.users[owner_login]
            owner_name = f"{user['first_name']} {user['last_name']}"

        details = QMessageBox()
        details.setWindowTitle(ad_data['name'])
        details.setText(f"""
            <b>Description:</b> {ad_data['description']}<br><br>
            <b>Owner:</b> {owner_name}<br>
            <b>Category:</b> {ad_data['category']}<br>
            <b>Cost:</b> ${ad_data['cost']}<br>
            <b>Posted:</b> {ad_data['date']}<br>
            <b>Popularity:</b> {ad_data['popularity']} views
        """)

        if ad_data['owner'] == self.data_manager.current_user:
            btn_edit = details.addButton("Edit", QMessageBox.ActionRole)
            btn_delete = details.addButton("Delete", QMessageBox.ActionRole)
            btn_close = details.addButton("Close", QMessageBox.RejectRole)

            details.exec_()

            if details.clickedButton() == btn_edit:
                self.show_edit_ad_dialog(ad_data)
            elif details.clickedButton() == btn_delete:
                self.delete_ad(ad_data['id'])
        else:
            details.exec_()

    def delete_ad(self, ad_id: str):
        reply = QMessageBox.question(
            self, 'Delete Ad', 'Are you sure you want to delete this ad?',
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            self.data_manager.delete_ad(ad_id)
            self.update_ads_list()

    def display_ads(self, ads: List):
        self.ads_list.clear()
        self.current_displayed_ads = ads.copy()

        try:
            if not ads:
                self.ads_list.addItem("No ads to display")
                return

            sorted_ads = self.sort_context.sort_ads(ads)

            for ad in sorted_ads:
                if not all(key in ad for key in ['name', 'cost', 'category']):
                    continue

                try:
                    item_text = f"{ad['name']} - ${float(ad['cost']):.2f} ({ad['category']})"
                    item = QListWidgetItem(item_text)
                    item.setData(Qt.UserRole, ad)

                    if ad.get('owner') == self.data_manager.current_user:
                        item.setForeground(QColor("#2196F3"))

                    self.ads_list.addItem(item)
                except (ValueError, KeyError) as e:
                    print(f"Error displaying ad: {e}")
                    continue
        except Exception as e:
            print(f"Error sorting ads: {e}")
            self.ads_list.addItem("Error displaying ads")

    def logout(self):
        self.data_manager.current_user = None
        self.show_login()