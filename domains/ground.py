from core.state import State, Unit, Resources


class GroundScenario:

    @staticmethod
    def create_defensive_scenario():
        friendly_units = [
            Unit("F1", fuel=80),
            Unit("F2", fuel=60),
            Unit("F3", fuel=40)
        ]

        enemy_units = [
            Unit("E1"),
            Unit("E2")
        ]

        resources = Resources(fuel=500, ammo=200)

        return State(friendly_units, enemy_units, resources)