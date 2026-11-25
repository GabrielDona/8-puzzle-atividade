from puzzle.base_search import BaseSearch
from puzzle.state import State
from puzzle.result import SearchResult

DEFAULT_DEPTH_LIMIT = 50


class DFS(BaseSearch):

    def __init__(self, depth_limit: int = DEFAULT_DEPTH_LIMIT):
        self.depth_limit = depth_limit

    def search(self, initial: State) -> SearchResult:
        result = SearchResult(solution=None, nodes_generated=1, max_frontier_size=1)
        frontier = [initial]                 
        best_depth = {initial.tiles: 0}       

        while frontier:
            node = frontier.pop()
            if node.is_goal:
                result.solution = node
                result.depth = node.cost
                return result
            if node.cost >= self.depth_limit: 
                continue
            result.nodes_expanded += 1
            for child in reversed(node.neighbors()):
                if best_depth.get(child.tiles, float("inf")) <= child.cost:
                    continue
                best_depth[child.tiles] = child.cost
                result.nodes_generated += 1
                frontier.append(child)
            result.max_frontier_size = max(result.max_frontier_size, len(frontier))

        return result
