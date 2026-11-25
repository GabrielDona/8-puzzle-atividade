import heapq
from puzzle.base_search import BaseSearch
from puzzle.state import State
from puzzle.result import SearchResult


class AStar(BaseSearch):

    def heuristic(self, state: State) -> int:
        """Distância de Manhattan (admissível e consistente)."""
        total = 0
        for idx, tile in enumerate(state.tiles):
            if tile == 0:
                continue
            goal_idx = tile - 1
            total += abs(idx // 3 - goal_idx // 3) + abs(idx % 3 - goal_idx % 3)
        return total

    def search(self, initial: State) -> SearchResult:
        result = SearchResult(solution=None, nodes_generated=1, max_frontier_size=1)
        counter = 0                                   # desempate na heap
        frontier = [(self.heuristic(initial), counter, initial)]
        best_g = {initial.tiles: 0}

        while frontier:
            _, _, node = heapq.heappop(frontier)
            if node.cost > best_g[node.tiles]:
                continue
            if node.is_goal:
                result.solution = node
                result.depth = node.cost
                return result
            result.nodes_expanded += 1
            for child in node.neighbors():
                if child.cost < best_g.get(child.tiles, float("inf")):
                    best_g[child.tiles] = child.cost
                    counter += 1
                    result.nodes_generated += 1
                    heapq.heappush(frontier, (child.cost + self.heuristic(child), counter, child))
            result.max_frontier_size = max(result.max_frontier_size, len(frontier))

        return result
