from SortStrategy import SortStrategy
from typing import List, Dict


class SortByPopularity(SortStrategy):
    def __init__(self, ascending=True):
        self.__ascending = ascending

    def sort(self, ads: List[Dict]) -> List[Dict]:
        return sorted(ads, key=lambda x: x['popularity'],
                      reverse=not self.__ascending)