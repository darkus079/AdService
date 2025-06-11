from SortStrategy import SortStrategy
from typing import List, Dict


class SortContext:
    def __init__(self, strategy: SortStrategy):
        self.__strategy = strategy

    def set_strategy(self, strategy: SortStrategy):
        self.__strategy = strategy

    def sort_ads(self, ads: List[Dict]) -> List[Dict]:
        return self.__strategy.sort(ads)