from typing import List
import copy


class Unit:
    def __init__(self, unit_id: str, fuel: float = 100):
        self.id = unit_id
        self.fuel = fuel

    def __repr__(self):
        return f"Unit(id={self.id}, fuel={self.fuel})"


class Resources:
    def __init__(self, fuel: float = 1000, ammo: int = 100):
        self.fuel = fuel
        self.ammo = ammo


class State:
    def __init__(self, friendly_units: List[Unit], enemy_units: List[Unit], resources: Resources):
        self.friendly_units = friendly_units
        self.enemy_units = enemy_units
        self.resources = resources

    def copy(self):
        return copy.deepcopy(self)

    def is_terminal(self):
        return len(self.enemy_units) == 0 or len(self.friendly_units) == 0

    def evaluate(self):
        return len(self.friendly_units) - len(self.enemy_units)