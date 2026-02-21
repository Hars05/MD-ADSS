from search.astar import AStarSearch
from adversarial.minimax import AlphaBetaSearch

class MDADSS:
    def __init__(self):
        self.astar = AStarSearch()
        self.alphabeta = AlphaBetaSearch()

    def generate_recommendations(self, state, top_k=1):
        # simplified for now
        action, value = self.alphabeta.search(state, state)
        return [{
            "rank": 1,
            "title": "ROBUST ACTION",
            "utility": value,
            "actions": [str(action)],
            "algorithm": "Alpha-Beta",
            "risk_level": "medium",
            "explanation": {
                "worst_case_value": value
            }
        }]

    def get_performance_stats(self):
        return {
            "astar": self.astar._get_stats(),
            "alphabeta": self.alphabeta.get_stats()
        }