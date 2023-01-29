from abc import ABC, abstractmethod
from typing import Tuple

class Decomposer(ABC):

    def __init__(self, seed: int) -> None:
        self.seed = seed

    @abstractmethod
    def to_space(self, i: int) -> Tuple[int, int, int]:
        ...

    @abstractmethod
    def to_plane(self, i: int) -> Tuple[int, int]:
        ...

    @property
    def name(self) -> str:
        raise NotImplemented("Please implement this for your class.")
