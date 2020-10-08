from p1_support import load_level, show_level, save_level_costs
from math import inf, sqrt
from heapq import heappop, heappush


def dijkstras_shortest_path(initial_position, destination, graph, adj):
    """ Searches for a minimal cost path through a graph using Dijkstra's algorithm.

    Args:
        initial_position: The initial cell from which the path extends.
        destination: The end location for the path.
        graph: A loaded level, containing walls, spaces, and waypoints.
        adj: An adjacency function returning cells adjacent to a given cell as well as their respective edge costs.

    Returns:
        If a path exits, return a list containing all cells from initial_position to destination.
        Otherwise, return None.

    """
    priQ = [(0, initial_position)]

    #came from dictionary
    cellFrom = {initial_position:None}

    #variable to keep track of cost cost so far
    costs = {initial_position:0}

    #main dijkstra's loop
    while len(priQ) != 0:
        #curr = (col, row)
        curr = heappop(priQ)

        if curr[1] == destination:
            #get list of values 
            tmp = curr[1]
            li = [tmp]
            #shorten by enumeration?
            while cellFrom[tmp] != None:
                tmp = cellFrom[tmp]
                li.append(tmp)
            return li

        #i = ((col, row), cost)
        for i in adj(graph, curr[1]):
            new_cost = costs[curr[1]] + i[1]
            if i[0] not in costs or new_cost < costs[i[0]]:
                costs[i[0]] = new_cost
                priority = new_cost
                heappush(priQ, i[::-1])     #reverse so queue detects distance first (position, distance)
                cellFrom[i[0]] = curr[1]
            
        
    return None


def dijkstras_shortest_path_to_all(initial_position, graph, adj):
    """ Calculates the minimum cost to every reachable cell in a graph from the initial_position.

    Args:
        initial_position: The initial cell from which the path extends.
        graph: A loaded level, containing walls, spaces, and waypoints.
        adj: An adjacency function returning cells adjacent to a given cell as well as their respective edge costs.

    Returns:
        A dictionary, mapping destination cells to the cost of a path from the initial_position.
    """
    pass


def navigation_edges(level, cell):
    """ Provides a list of adjacent cells and their respective costs from the given cell.

    Args:
        level: A loaded level, containing walls, spaces, and waypoints.
        cell: A target location.

    Returns:
        A list of tuples containing an adjacent cell's coordinates and the cost of the edge joining it and the
        originating cell.

        E.g. from (0,0):
            [((0,1), 1),
             ((1,0), 1),
             ((1,1), 1.4142135623730951),
             ... ]
    """
    toCheck = [
        (cell[0]-1, cell[1]-1), #top left
        (cell[0], cell[1]-1),   #top
        (cell[0]+1, cell[1]-1), #top right
        (cell[0]-1, cell[1]),   #left
        (cell[0]+1, cell[1]),   #right
        (cell[0]-1, cell[1]+1), #bottom left
        (cell[0], cell[1]+1),   #bottom
        (cell[0]+1, cell[1]+1)  #bottom right
    ]
    diags = [
        (cell[0]-1, cell[1]-1), #top left
        (cell[0]+1, cell[1]-1), #top right
        (cell[0]-1, cell[1]+1), #bottom left
        (cell[0]+1, cell[1]+1)  #bottom right
    ]
    diagFlag = False
    nextSpaces = []

    for i in toCheck:
        if i in diags:
            diagFlag = True

        #check 8 cells around
        if i in level['spaces']:
            if not(diagFlag):
                cost = (0.5 * (level['spaces'][cell])) + (0.5 * (level['spaces'][i]))
            else:
                cost = ((0.5 * sqrt(2)) * level['spaces'][cell]) + ((0.5 * sqrt(2)) * level['spaces'][i])
            
            nextSpaces.append((i, cost))
        diagFlag = False


    return nextSpaces


def test_route(filename, src_waypoint, dst_waypoint):
    """ Loads a level, searches for a path between the given waypoints, and displays the result.

    Args:
        filename: The name of the text file containing the level.
        src_waypoint: The character associated with the initial waypoint.
        dst_waypoint: The character associated with the destination waypoint.

    """

    # Load and display the level.
    level = load_level(filename)
    show_level(level)

    # Retrieve the source and destination coordinates from the level.
    src = level['waypoints'][src_waypoint]
    dst = level['waypoints'][dst_waypoint]

    # Search for and display the path from src to dst.
    path = dijkstras_shortest_path(src, dst, level, navigation_edges)
    if path:
        show_level(level, path)
    else:
        print("No path possible!")


def cost_to_all_cells(filename, src_waypoint, output_filename):
    """ Loads a level, calculates the cost to all reachable cells from 
    src_waypoint, then saves the result in a csv file with name output_filename.

    Args:
        filename: The name of the text file containing the level.
        src_waypoint: The character associated with the initial waypoint.
        output_filename: The filename for the output csv file.

    """
    
    # Load and display the level.
    level = load_level(filename)
    show_level(level)

    # Retrieve the source coordinates from the level.
    src = level['waypoints'][src_waypoint]
    
    # Calculate the cost to all reachable cells from src and save to a csv file.
    costs_to_all_cells = dijkstras_shortest_path_to_all(src, level, navigation_edges)
    save_level_costs(level, costs_to_all_cells, output_filename)


if __name__ == '__main__':
    filename, src_waypoint, dst_waypoint = 'example.txt', 'a','e'

    #TESTING navigation_edges
    print("********************* navigation_edges TEST *************************")
    level = load_level(filename)
    show_level(level)
    #print("Walls: \n", level['waypoints'],
    #   "\n Spaces:\n ", level['spaces'],
    #   "\n waypoints: \n", level['waypoints'])
    neibs = navigation_edges(level, (3,10))
    print("NEIGHBORS OF (2,1): \n" , neibs)

    #TESTING dijkstras_shortest_path (a -> e)
    print("\n********************* djik_short_path/test_route TEST *************************")
    test_route(filename, "b", "e")

    # Use this function call to find the route between two waypoints.
    #test_route(filename, src_waypoint, dst_waypoint)

    # Use this function to calculate the cost to all reachable cells from an origin point.
    #cost_to_all_cells(filename, src_waypoint, 'my_costs.csv')
