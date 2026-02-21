class MinimaxSearch:
    def __init__(self, max_depth=3):
        self.max_depth = max_depth
        self.stats = {"nodes_expanded": 0}

    def search(self, state, initial_state, depth=0, maximizing=True):
        if depth == self.max_depth or state.is_terminal():
            return None, state.evaluate()

        self.stats["nodes_expanded"] += 1

        if maximizing:
            best_value = float("-inf")
            best_action = None
            for i in range(2):
                action = f"Minimax_Action_{depth}_{i}"
                _, value = self.search(state, initial_state, depth + 1, False)
                if value > best_value:
                    best_value = value
                    best_action = action
            return best_action, best_value
        else:
            best_value = float("inf")
            for i in range(2):
                _, value = self.search(state, initial_state, depth + 1, True)
                best_value = min(best_value, value)
            return None, best_value

    def get_stats(self):
        return self.stats


class AlphaBetaSearch(MinimaxSearch):
    def search(self, state, initial_state, depth=0, maximizing=True, alpha=float("-inf"), beta=float("inf")):
        if depth == self.max_depth or state.is_terminal():
            return None, state.evaluate()

        self.stats["nodes_expanded"] += 1

        if maximizing:
            best_action = None
            value = float("-inf")
            for i in range(2):
                action = f"AlphaBeta_Action_{depth}_{i}"
                _, child_value = self.search(state, initial_state, depth + 1, False, alpha, beta)
                if child_value > value:
                    value = child_value
                    best_action = action
                alpha = max(alpha, value)
                if beta <= alpha:
                    break
            return best_action, value
        else:
            value = float("inf")
            for i in range(2):
                _, child_value = self.search(state, initial_state, depth + 1, True, alpha, beta)
                value = min(value, child_value)
                beta = min(beta, value)
                if beta <= alpha:
                    break
            return None, value