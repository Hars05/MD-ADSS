class ResourceAllocationCSP:

    @staticmethod
    def create_unit_assignment_problem(unit_ids, sectors, base_sector, min_base_defenders=1):
        return {
            "units": unit_ids,
            "sectors": sectors,
            "base": base_sector
        }

    @staticmethod
    def create_fuel_allocation_problem(unit_ids, total_fuel, min_fuel_per_unit):
        return {
            "units": unit_ids,
            "total_fuel": total_fuel,
            "min_per_unit": min_fuel_per_unit
        }


class BacktrackingSolver:
    def __init__(self):
        self.stats = {"assignments": 0}

    def solve(self, problem):
        self.stats["assignments"] += 1
        return {"solution": "dummy_assignment"}

    def get_stats(self):
        return self.stats