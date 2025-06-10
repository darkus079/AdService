from abc import ABC, abstractmethod


class Manager(ABC):
    @abstractmethod
    def save(self):
        pass
    
    @abstractmethod
    def _load(self):
        pass
