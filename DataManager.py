from Manager import Manager
from UserManager import UserManager
from AdManager import AdManager
from typing import List, Dict


class DataManager:
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance._initialize()
        return cls.__instance

    def _initialize(self):
        self.__user_manager = UserManager()
        self.__ad_manager = AdManager()

    @property
    def users(self) -> List:
        return self.__user_manager.users

    @property
    def current_user(self) -> str:
        return self.__user_manager.current_user

    @current_user.setter
    def current_user(self, val: str | None):
        self.__user_manager.current_user = val

    @property
    def ads(self) -> List:
        return self.__ad_manager.ads

    def get_user_ads(self) -> List[Dict]:
        return self.__ad_manager.get_user_ads(self.current_user)

    def register_user(self, user_data: Dict) -> bool:
        return self.__user_manager.register_user(user_data)

    def authenticate_user(self, login: str, password: str) -> bool:
        return self.__user_manager.authenticate_user(login, password)

    def add_ad(self, ad_data: Dict):
        self.__ad_manager.add_ad(self.current_user, ad_data)

    def update_ad(self, ad_id: str, ad_data: Dict):
        self.__ad_manager.update_ad(ad_id, ad_data)

    def delete_ad(self, ad_id: str):
        self.__ad_manager.delete_ad(ad_id)

    def increment_popularity(self, ad_id: str):
        self.__ad_manager.increment_popularity(ad_id)

    def get_user_ads(self) -> List[Dict]:
        return self.__ad_manager.get_user_ads(self.current_user)

    def get_all_ads(self) -> List[Dict]:
        return self.__ad_manager.get_all_ads()