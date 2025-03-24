from ..models.grid import Grid
from ..models.frontier import QueueFrontier
from ..models.solution import NoSolution, Solution
from ..models.node import Node


class BreadthFirstSearch:
    @staticmethod
    def search(grid: Grid) -> Solution:
        """Find path between two points in a grid using Breadth First Search

        Args:
            grid (Grid): Grid of points
            
        Returns:
            Solution: Solution found
        """
        # Initialize a node with the initial position
        node = Node("", grid.start, 0)

        # Initialize the explored dictionary to be empty
        explored = {} 
        
        # Add the node to the explored dictionary
        explored[node.state] = True
        
    
        # Initialize the frontier with the initial node
        # In this example, the frontier is a queue
        frontier = QueueFrontier()
        frontier.add(node)

        while True:

            #  Fail if the frontier is empty
            if frontier.is_empty():
                return NoSolution(explored)

            # Remove a node from the frontier
            node = frontier.remove()

            # BFS 
            # Get the neighbours of the current node
            successors = grid.get_neighbours(node.state)
            
            for key, value in successors.items():
                
                if value not in explored:
                    # Initialize the son node
                    new_node = Node("", value,
                                    node.cost + grid.get_cost(value),
                                    parent=node, action=key)

                    # Mark the successor as reached
                    explored[value] = True

                    # Return if the node contains a goal state
                    # In this example, the goal test is run
                    # before adding a new node to the frontier
                    if value == grid.end:
                        return Solution(new_node, explored)
                    
                    # Add the new node to the frontier
                    frontier.add(new_node)