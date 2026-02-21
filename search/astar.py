import heapq


class AStarSearch:
    def __init__(self, max_depth=5):
        self.max_depth = max_depth
        self.stats = {"nodes_expanded": 0}

    def heuristic(self, state):
        return -state.evaluate()

    def find_top_k_plans(self, state, k=3, depth=3):
        heap = []
        heapq.heappush(heap, (0, [], state))

        results = []

        while heap and len(results) < k:
            cost, actions, current_state = heapq.heappop(heap)
            self.stats["nodes_expanded"] += 1

            if len(actions) >= depth:
                results.append((actions, current_state, -cost))
                continue

            for i in range(2):
                new_actions = actions + [f"AStar_Action_{len(actions)}_{i}"]
                new_cost = cost + 1
                heapq.heappush(heap, (new_cost, new_actions, current_state))

        return results

    def _get_stats(self):
        return self.stats