from abc import ABC, abstractmethod


class Bot(ABC):
    @abstractmethod
    def setup(self):
        pass

    def run(self):
        pass

    def teardown(self):
        pass
