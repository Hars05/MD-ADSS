from collections import deque


class BFSSearch:
    def __init__(self, max_depth=3):
        self.max_depth = max_depth
        self.stats = {"nodes_expanded": 0}

    def search_all_paths(self, state, depth=3):
        queue = deque([(state, [], 0)])
        paths = []

        while queue:
            current_state, actions, d = queue.popleft()

            if d >= depth:
                paths.append(actions)
                continue

            self.stats["nodes_expanded"] += 1

            # Dummy branching
            for i in range(2):
                new_actions = actions + [f"BFS_Action_{d}_{i}"]
                queue.append((current_state, new_actions, d + 1))

        return paths

    def _get_stats(self):
        return self.stats