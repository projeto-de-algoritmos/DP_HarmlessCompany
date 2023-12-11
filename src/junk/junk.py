import random

class Junk:
    def __init__(self, name, value, weight) -> None:
        self.name = name

        if isinstance(value, list):
            self.value = random.randint(value[0], value[1])
        else:
            self.value = value

        self.weight = weight

    def get_value(self):
        return self.value

    def get_weight(self):
        return self.weight

    def __str__(self) -> str:
        return f"{self.name:20} +${self.value:<6} -{self.weight}Kg"