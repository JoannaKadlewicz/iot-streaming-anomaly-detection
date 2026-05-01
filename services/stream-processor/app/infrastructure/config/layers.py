from enum import Enum


class Layer(str, Enum):
    BRONZE = "bronze"
    SILVER = "silver"
    GOLD = "gold"

    def __str__(self) -> str:
        return self.value