import random, sys, time


# "A" signifies the agent
# "G" signifies the goal
# "0" signifies a wall
# "1" signifies no wall

# MazeEntry Class - a single location within a Maze
# row, col - position in Maze
# cost - cost up to that point in the Maze
# heuristic - estimate of remaining cost to get to goal
# status - whether the MazeEntry is a wall, no wall, agent start point, or goal
# parent - the parent of the MazeEntry in the tree when performing A* search
class MazeEntry:
    def __init__(self, row, col, status, cost=None, heuristic=None):
        self.row = row
        self.col = col
        self.cost = cost
        self.heuristic = heuristic
        self.status = status
        self.parent = None

    def print(self):
        print("[" + str(self.row) + ", " + str(self.col) + "]")

    def get(self):
        return (str(self.row) + "," + str(self.col))


# Maze Class - the entire maze
# content - a dictionary containing all MazeEntry objects within the Maze
# rows, cols - dimensions of the maze
# agent_row, agent_col - starting coordinates for the agent
# goal_row, goal_col - coordinates for the goal
class Maze:
    def __init__(self, rows, cols, wallProbability, agent_row=None, agent_col=None, goal_row=None, goal_col=None):
        self.content = {}
        self.rows = rows
        self.cols = cols
        if agent_row is None:
            self.agent_row = random.randint(0, rows - 1)
        else:
            self.agent_row = agent_row
        if agent_col is None:
            self.agent_col = random.randint(0, cols - 1)
        else:
            self.agent_col = agent_col
        if goal_row is None:
            self.goal_row = random.randint(0, rows - 1)
        else:
            self.goal_row = goal_row
        if goal_col is None:
            self.goal_col = random.randint(0, cols - 1)
        else:
            self.goal_col = goal_col
        for i in range(rows):
            for j in range(cols):
                if (i != self.agent_row or j != self.agent_col) and (i != self.goal_row or j != self.goal_col):
                    randomNumber = random.random()
                    if randomNumber > wallProbability:
                        wallStatus = "1"
                    else:
                        wallStatus = "0"
                    self.content[(i, j)] = MazeEntry(i, j, wallStatus)
        self.content[(self.agent_row, self.agent_col)] = MazeEntry(self.agent_row, self.agent_col, "A")
        self.content[(self.goal_row, self.goal_col)] = MazeEntry(self.goal_row, self.goal_col, "G")

    def print(self):
        for i in range(self.rows):
            row = []
            for j in range(self.cols):
                row.append(self.content[(i, j)].status)
            print(row)


# Navigate through the maze
def forward_a_star_walk_favor_high_g_values(true_maze):
    total_expand = 0

    # In addition to the true maze which we are to navigate though, create a known_maze,
    # representing the maze as the agent knows it. The agent does not initially know the maze,
    # other than its starting point and the goal point. It initially assumes that no spaces contain walls.
    known_maze = Maze(rows, cols, 0, true_maze.agent_row, true_maze.agent_col, true_maze.goal_row, true_maze.goal_col)
    # print("Known Maze:")
    # known_maze.print()

    # Initialize the current position of the agent and its goal
    current_position = [true_maze.agent_row, true_maze.agent_col]
    goal_position = [true_maze.goal_row, true_maze.goal_col]

    # Initialize a list to hold the actual path that the agent has followed.
    # It begins by only containing a MazeEntry object representing its starting point
    actual_path = [MazeEntry(current_position[0], current_position[1], "0")]

    # Use A* search to generate a planned path to the goal based on the current state of the known_maze
    success, planned_path, expanded = forward_a_star_favor_high_g_values(current_position, goal_position, known_maze)

    total_expand += expanded

    # If no path could be found, return false, indicating failure, and an empty list
    if not success:
        return False, [], total_expand

    # Iterate until the goal has been reached
    while not (current_position[0] == true_maze.goal_row and current_position[1] == true_maze.goal_col):
        # Search for any new walls adjacent to the agent in the true maze and update the known_maze
        newWallFound = update_adjacent_spaces(current_position, true_maze, known_maze)
        print("-" * 100)
        printPath(known_maze, planned_path)
        print("-" * 100)

        # If a new wall was found, use A* search to regenerate the planned path based on the new state of the known_maze
        # If no path can be found, return false, indicating failure, and an empty list
        if newWallFound:
            success, planned_path, expanded = forward_a_star_favor_high_g_values(current_position, goal_position, known_maze)
            print("-" * 100)
            printPath(known_maze, planned_path)
            print("-" * 100)
            if not success:
                total_expand += expanded
                return False, [], total_expand

        # Remove the current element of the planned path and update the current position of the agent for the next iteration
        planned_path.remove(planned_path[0])
        current_position[0] = planned_path[0].row
        current_position[1] = planned_path[0].col

        # Add the updated current position of the agent to the actual path
        actual_path.append(MazeEntry(current_position[0], current_position[1], "0"))

    # If we break from the while loop (the agent reached the goal), return true, indicating success,
    # and the actual path followed by the agent
    total_expand += expanded
    return True, actual_path, total_expand


# Navigate through the maze
def forward_a_star_walk_favor_low_g_values(true_maze):
    total_expand = 0

    # In addition to the true maze which we are to navigate though, create a known_maze,
    # representing the maze as the agent knows it. The agent does not initially know the maze,
    # other than its starting point and the goal point. It initially assumes that no spaces contain walls.
    known_maze = Maze(rows, cols, 0, true_maze.agent_row, true_maze.agent_col, true_maze.goal_row, true_maze.goal_col)
    # print("Known Maze:")
    # known_maze.print()

    # Initialize the current position of the agent and its goal
    current_position = [true_maze.agent_row, true_maze.agent_col]
    goal_position = [true_maze.goal_row, true_maze.goal_col]

    # Initialize a list to hold the actual path that the agent has followed.
    # It begins by only containing a MazeEntry object representing its starting point
    actual_path = [MazeEntry(current_position[0], current_position[1], "0")]

    # Use A* search to generate a planned path to the goal based on the current state of the known_maze
    success, planned_path, expanded = forward_a_star_favor_low_g_values(current_position, goal_position, known_maze)

    total_expand += expanded

    # If no path could be found, return false, indicating failure, and an empty list
    if not success:
        return False, [], total_expand

    # Iterate until the goal has been reached
    while not (current_position[0] == true_maze.goal_row and current_position[1] == true_maze.goal_col):
        # Search for any new walls adjacent to the agent in the true maze and update the known_maze
        newWallFound = update_adjacent_spaces(current_position, true_maze, known_maze)
        print("-" * 100)
        printPath(known_maze, planned_path)
        print("-" * 100)

        # If a new wall was found, use A* search to regenerate the planned path based on the new state of the known_maze
        # If no path can be found, return false, indicating failure, and an empty list
        if newWallFound:
            success, planned_path, expanded = forward_a_star_favor_low_g_values(current_position, goal_position, known_maze)
            print("-" * 100)
            printPath(known_maze, planned_path)
            print("-" * 100)
            if not success:
                total_expand += expanded
                return False, [], total_expand

        # Remove the current element of the planned path and update the current position of the agent for the next iteration
        planned_path.remove(planned_path[0])
        current_position[0] = planned_path[0].row
        current_position[1] = planned_path[0].col

        # Add the updated current position of the agent to the actual path
        actual_path.append(MazeEntry(current_position[0], current_position[1], "0"))

    # If we break from the while loop (the agent reached the goal), return true, indicating success,
    # and the actual path followed by the agent
    total_expand += expanded
    return True, actual_path, total_expand


def adaptive_a_star_walk(true_maze):
    total_expand = 0
    known_maze = Maze(rows, cols, 0, true_maze.agent_row, true_maze.agent_col, true_maze.goal_row, true_maze.goal_col)
    current_position = [true_maze.agent_row, true_maze.agent_col]
    goal_position = [true_maze.goal_row, true_maze.goal_col]
    actual_path = [MazeEntry(current_position[0], current_position[1], "0")]
    success, planned_path, expanded = adaptive_a_star(current_position, goal_position, known_maze)

    total_expand += expanded
    if not success:
        return False, [], total_expand

    # Iterate until the goal has been reached
    while not (current_position[0] == true_maze.goal_row and current_position[1] == true_maze.goal_col):
        # Search for any new walls adjacent to the agent in the true maze and update the known_maze
        newWallFound = update_adjacent_spaces(current_position, true_maze, known_maze)
        print("-" * 100)
        printPath(known_maze, planned_path)
        print("-" * 100)

        # If a new wall was found, use A* search to regenerate the planned path based on the new state of the known_maze
        # If no path can be found, return false, indicating failure, and an empty list
        if newWallFound:
            success, planned_path, expanded = adaptive_a_star(current_position, goal_position, known_maze)
            print("-" * 100)
            printPath(known_maze, planned_path)
            print("-" * 100)
            if not success:
                total_expand += expanded
                return False, [], total_expand

        # Remove the current element of the planned path and update the current position of the agent for the next iteration
        planned_path.remove(planned_path[0])
        current_position[0] = planned_path[0].row
        current_position[1] = planned_path[0].col

        # Add the updated current position of the agent to the actual path
        actual_path.append(MazeEntry(current_position[0], current_position[1], "0"))

    # If we break from the while loop (the agent reached the goal), return true, indicating success,
    # and the actual path followed by the agent
    total_expand += expanded
    return True, actual_path, total_expand


def backwards_a_star_walk(true_maze):
    # In addition to the true maze which we are to navigate though, create a known_maze,
    # representing the maze as the agent knows it. The agent does not initially know the maze,
    # other than its starting point and the goal point. It initially assumes that no spaces contain walls.
    known_maze = Maze(rows, cols, 0, true_maze.agent_row, true_maze.agent_col, true_maze.goal_row, true_maze.goal_col)
    # print("Known Maze:")
    # known_maze.print()

    total_expand = 0

    # Initialize the current position of the agent and its goal
    current_position = [true_maze.agent_row, true_maze.agent_col]
    goal_position = [true_maze.goal_row, true_maze.goal_col]

    # Initialize a list to hold the actual path that the agent has followed.
    # It begins by only containing a MazeEntry object representing its starting point
    actual_path = [MazeEntry(goal_position[0], goal_position[1], "0")]

    # Use A* search to generate a planned path to the goal based on the current state of the known_maze
    success, planned_path, expanded = backwards_a_star(current_position, goal_position, known_maze)

    total_expand += expanded

    # If no path could be found, return false, indicating failure, and an empty list
    if not success:
        return False, []

    # Iterate until the goal has been reached
    while not (goal_position[0] == true_maze.agent_row and goal_position[1] == true_maze.agent_col):
        # Search for any new walls adjacent to the agent in the true maze and update the known_maze
        newWallFound = update_adjacent_spaces(goal_position, true_maze, known_maze)
        print("-" * 100)
        printPath(known_maze, planned_path)
        print("-" * 100)

        # If a new wall was found, use A* search to regenerate the planned path based on the new state of the known_maze
        # If no path can be found, return false, indicating failure, and an empty list
        if newWallFound:
            try:
                success, planned_path, expanded = backwards_a_star(current_position, goal_position, known_maze)
                print("-" * 100)
                printPath(known_maze, planned_path)
                print("-" * 100)
            except:
                pass
            if not success:
                total_expand += expanded
                return False, [], total_expand

        # Remove the current element of the planned path and update the current position of the agent for the next iteration
        planned_path.remove(planned_path[0])
        goal_position[0] = planned_path[0].row
        goal_position[1] = planned_path[0].col

        # Add the updated current position of the agent to the actual path
        actual_path.append(MazeEntry(goal_position[0], goal_position[1], "0"))

    # If we break from the while loop (the agent reached the goal), return true, indicating success,
    # and the actual path followed by the agent
    total_expand += expanded
    return True, actual_path, total_expand


# Update the spaces in the known_maze which are adjacent to current_position
# by assigning them the values of the corresponding spaces in the true_maze.
# This allows the agent to update its understanding of where walls are in the maze.
# If a new wall is detected, return true, indicating that regenerating the planned path is necessary.
# Otherwise, return false.
def update_adjacent_spaces(current_position, true_maze, known_maze):
    newWallFound = False
    if current_position[0] != 0:
        if true_maze.content[(current_position[0] - 1, current_position[1])].status == "0" and known_maze.content[
            (current_position[0] - 1, current_position[1])].status == "1":
            known_maze.content[(current_position[0] - 1, current_position[1])].status = "0"
            newWallFound = True
    if current_position[0] != true_maze.rows - 1:
        if true_maze.content[(current_position[0] + 1, current_position[1])].status == "0" and known_maze.content[
            (current_position[0] + 1, current_position[1])].status == "1":
            known_maze.content[(current_position[0] + 1, current_position[1])].status = "0"
            newWallFound = True
    if current_position[1] != 0:
        if true_maze.content[(current_position[0], current_position[1] - 1)].status == "0" and known_maze.content[
            (current_position[0], current_position[1] - 1)].status == "1":
            known_maze.content[(current_position[0], current_position[1] - 1)].status = "0"
            newWallFound = True
    if current_position[1] != true_maze.cols - 1:
        if true_maze.content[(current_position[0], current_position[1] + 1)].status == "0" and known_maze.content[
            (current_position[0], current_position[1] + 1)].status == "1":
            known_maze.content[(current_position[0], current_position[1] + 1)].status = "0"
            newWallFound = True
    return newWallFound


# Perform A* search on the known maze, beginning at initial_position, and targeting goal_position
def forward_a_star_favor_high_g_values(initial_position, goal_position, known_maze):
    # create the initial node in the tree based on the initial_position
    initial_node = MazeEntry(initial_position[0], initial_position[1], "1", 0,
                             manhattan_distance_heuristic(initial_position, goal_position))

    # initialize the queue with only the initial_node
    q = [initial_node]

    # initialize the list of expanded nodes (implemented using a dictionary)
    expandedList = {}

    expanded = 0

    # Iterate as long as the queue is not empty
    while q:
        # Pop the first node off of the queue
        x = q[0]
        q.remove(x)

        # If this node has already been expanded, continue to the next iteration
        if expandedList.setdefault((x.row, x.col)) is not None:
            continue

        # Add this node to the expanded list
        expandedList[(x.row, x.col)] = True

        expanded += 1

        # If this node is the goal, return True, indicating success, as well as the path,
        # Which is obtaining by following the parents of each node, up the tree
        if x.row == goal_position[0] and x.col == goal_position[1]:
            path = [x]
            while x.parent is not None:
                x = x.parent
                path.append(x)
            path.reverse()
            # Passed - A Star Test (and thus findNeighbors is verified)
            # print("Path From Forwards A Star:")
            # for i in path:
            #   i.print()
            return True, path, expanded

        # Find the neighbors of the current node, and for each neighbor, create a MazeEntry object to represent it,
        # and add it to the queue in order of increasing cost + heuristic
        for i in findNeighbors([x.row, x.col], known_maze):
            if expandedList.setdefault((i.row, i.col)) is None:
                i.parent = x
                i.cost = x.cost + 1
                i.heuristic = manhattan_distance_heuristic([i.row, i.col], goal_position)
                q = addToQueueFavorHighGValues(q, i)

    # If we exited from the while loop, meaning that the queue became empty without finding the goal,
    # return false, indicating failure, and an empty list
    return False, [], expanded


# Perform A* search on the known maze, beginning at initial_position, and targeting goal_position
def forward_a_star_favor_low_g_values(initial_position, goal_position, known_maze):
    # create the initial node in the tree based on the initial_position
    initial_node = MazeEntry(initial_position[0], initial_position[1], "1", 0,
                             manhattan_distance_heuristic(initial_position, goal_position))

    # initialize the queue with only the initial_node
    q = [initial_node]

    # initialize the list of expanded nodes (implemented using a dictionary)
    expandedList = {}

    expanded = 0

    # Iterate as long as the queue is not empty
    while q:
        # Pop the first node off of the queue
        x = q[0]
        q.remove(x)

        # If this node has already been expanded, continue to the next iteration
        if expandedList.setdefault((x.row, x.col)) is not None:
            continue

        # Add this node to the expanded list
        expandedList[(x.row, x.col)] = True

        expanded += 1

        # If this node is the goal, return True, indicating success, as well as the path,
        # Which is obtaining by following the parents of each node, up the tree
        if x.row == goal_position[0] and x.col == goal_position[1]:
            path = [x]
            while x.parent is not None:
                x = x.parent
                path.append(x)
            path.reverse()
            # Passed - A Star Test (and thus findNeighbors is verified)
            # print("Path From Forwards A Star:")
            # for i in path:
            #   i.print()
            return True, path, expanded

        # Find the neighbors of the current node, and for each neighbor, create a MazeEntry object to represent it,
        # and add it to the queue in order of increasing cost + heuristic
        for i in findNeighbors([x.row, x.col], known_maze):
            if expandedList.setdefault((i.row, i.col)) is None:
                i.parent = x
                i.cost = x.cost + 1
                i.heuristic = manhattan_distance_heuristic([i.row, i.col], goal_position)
                q = addToQueueFavorLowGValues(q, i)

    # If we exited from the while loop, meaning that the queue became empty without finding the goal,
    # return false, indicating failure, and an empty list
    return False, [], expanded


# Perform A* search on the known maze, beginning at initial_position, and targeting goal_position
def adaptive_a_star(initial_position, goal_position, known_maze):
    # create the initial node in the tree based on the initial_position
    initial_node = MazeEntry(initial_position[0], initial_position[1], "1", 0,
                             manhattan_distance_heuristic(initial_position, goal_position))

    # initialize the queue with only the initial_node
    q = [initial_node]

    # initialize the list of expanded nodes (implemented using a dictionary)
    expandedList = {}

    expanded = 0

    # Iterate as long as the queue is not empty
    while q:
        # Pop the first node off of the queue
        x = q[0]
        q.remove(x)

        # If this node has already been expanded, continue to the next iteration
        if expandedList.setdefault((x.row, x.col)) is not None:
            continue

        # Add this node to the expanded list
        expandedList[(x.row, x.col)] = True

        expanded += 1

        # If this node is the goal, return True, indicating success, as well as the path,
        # Which is obtaining by following the parents of each node, up the tree
        if x.row == goal_position[0] and x.col == goal_position[1]:
            path = [x]
            while x.parent is not None:
                x = x.parent
                path.append(x)
            path.reverse()
            # Update Every Expanded Node According to Adaptive A* Search
            # By Overwriting It With an Identical Node But With Heuristic Defined as goal_cost - cost
            # (In Accordance With Adaptive A* Heuristic Update Equation)
            for i in expandedList:
                status = known_maze.content[(i[0], i[1])].status
                cost = known_maze.content[(i[0], i[1])].cost
                if cost is None:
                    cost = 0
                goal_cost = len(path) - 1
                known_maze.content[(i[0], i[1])] = MazeEntry(i[0], i[1], status, cost, goal_cost - cost)
            # Passed - A Star Test (and thus findNeighbors is verified)
            # print("Path From Forwards A Star:")
            # for i in path:
            #   i.print()
            return True, path, expanded

        # Find the neighbors of the current node, and for each neighbor, create a MazeEntry object to represent it,
        # and add it to the queue in order of increasing cost + heuristic
        for i in findNeighbors([x.row, x.col], known_maze):
            if expandedList.setdefault((i.row, i.col)) is None:
                i.parent = x
                i.cost = x.cost + 1
                if i.heuristic is None:
                    i.heuristic = manhattan_distance_heuristic([i.row, i.col], goal_position)
                q = addToQueueFavorHighGValues(q, i)

    # If we exited from the while loop, meaning that the queue became empty without finding the goal,
    # return false, indicating failure, and an empty list
    return False, [], expanded


def backwards_a_star(initial_position, goal_position, known_maze):
    # create the initial node in the tree based on the initial_position
    initial_node = MazeEntry(goal_position[0], goal_position[1], "1", 0,
                             manhattan_distance_heuristic(goal_position, initial_position))

    # initialize the queue with only the initial_node
    q = [initial_node]

    # initialize the list of expanded nodes (implemented using a dictionary)
    expandedList = {}

    expanded = 0

    # Iterate as long as the queue is not empty
    while q:
        # Pop the first node off of the queue
        x = q[0]
        q.remove(x)

        # If this node has already been expanded, continue to the next iteration
        if expandedList.setdefault((x.row, x.col)) is not None:
            continue

        # Add this node to the expanded list
        expandedList[(x.row, x.col)] = True
        expanded += 1

        # If this node is the goal, return True, indicating success, as well as the path,
        # Which is obtaining by following the parents of each node, up the tree
        if x.row == initial_position[0] and x.col == initial_position[1]:
            path = [x]
            while x.parent is not None:
                x = x.parent
                path.append(x)
            path.reverse()
            # Passed - A Star Test (and thus findNeighbors is verified)
            # print("Path From Backwards A Star:")
            #
            # for i in path:
            #   i.print()
            return True, path, expanded

        # Find the neighbors of the current node, and for each neighbor, create a MazeEntry object to represent it,
        # and add it to the queue in order of increasing cost + heuristic
        for i in findNeighbors([x.row, x.col], known_maze):
            if expandedList.setdefault((i.row, i.col)) is None:
                i.parent = x
                i.cost = x.cost + 1
                i.heuristic = manhattan_distance_heuristic([i.row, i.col], initial_position)
                q = addToQueueFavorHighGValues(q, i)

    # If we exited from the while loop, meaning that the queue became empty without finding the goal,
    # return false, indicating failure, and an empty list
    return False, [], expanded


# Find all neighbors of a node based on its current position and the content of the known maze
# Any neighbors which contain a wall are ignored
def findNeighbors(current_position, known_maze):
    neighbors = []
    if current_position[0] != 0 and known_maze.content[(current_position[0] - 1, current_position[1])].status != "0":
        neighbors.append(MazeEntry(current_position[0] - 1, current_position[1], "1"))
    if current_position[0] != known_maze.rows - 1 and known_maze.content[
        (current_position[0] + 1, current_position[1])].status != "0":
        neighbors.append(MazeEntry(current_position[0] + 1, current_position[1], "1"))
    if current_position[1] != 0 and known_maze.content[(current_position[0], current_position[1] - 1)].status != "0":
        neighbors.append(MazeEntry(current_position[0], current_position[1] - 1, "1"))
    if current_position[1] != known_maze.cols - 1 and known_maze.content[
        (current_position[0], current_position[1] + 1)].status != "0":
        neighbors.append(MazeEntry(current_position[0], current_position[1] + 1, "1"))
    return neighbors


# Compute the Manhattan distance heuristic for a node based on its position and the goal position
def manhattan_distance_heuristic(current_position, goal_position):
    if current_position[0] > goal_position[0]:
        x_distance = current_position[0] - goal_position[0]
    else:
        x_distance = goal_position[0] - current_position[0]
    if current_position[1] > goal_position[1]:
        y_distance = current_position[1] - goal_position[1]
    else:
        y_distance = goal_position[1] - current_position[1]
    return x_distance + y_distance


# Add a new node to the queue in order of increasing cost + heuristic
def addToQueueFavorHighGValues(q, node):
    j = len(q)
    q_new = []
    for i in range(len(q)):
        nodeValue = node.cost + node.heuristic
        entryValue = q[i].cost + q[i].heuristic
        # Favor higher cost (g-value)
        if nodeValue < entryValue or nodeValue == entryValue and node.cost > q[i].cost:
            j = i
            break
    for i in range(0, j):
        q_new.append(q[i])
    q_new.append(node)
    for i in range(j + 1, len(q) + 1):
        q_new.append(q[i - 1])
    return q_new


# Add a new node to the queue in order of increasing cost + heuristic
def addToQueueFavorLowGValues(q, node):
    j = len(q)
    q_new = []
    for i in range(len(q)):
        nodeValue = node.cost + node.heuristic
        entryValue = q[i].cost + q[i].heuristic
        # Favor lower cost (g-value)
        if nodeValue < entryValue or nodeValue == entryValue and node.cost < q[i].cost:
            j = i
            break
    for i in range(0, j):
        q_new.append(q[i])
    q_new.append(node)
    for i in range(j + 1, len(q) + 1):
        q_new.append(q[i - 1])
    return q_new


# PRINTS THE VISUAL PATH
def printPath(maze, path):
    row = []
    for i in range(maze.rows):
        strRow = ""
        for j in range(maze.cols):
            if (maze.content[(i, j)].status == "1"):
                strRow += " "
            if (maze.content[(i, j)].status == "0"):
                strRow += "#"
            if (maze.content[(i, j)].status == "A"):
                strRow += "A"
            if (maze.content[(i, j)].status == "G"):
                strRow += "G"
        row.append(strRow)

    xCoords = []
    yCoords = []
    for node in path[1:-1]:
        temp = node.get()
        x, y = map(int, temp.split(","))
        xCoords.append(x)
        yCoords.append(y)

    for index, x in enumerate(xCoords):
        row[x] = row[x][:yCoords[index]] + ":" + row[x][yCoords[index] + 1:]

    for i in row:
        print(i)


rows = 15
cols = 30
wallProbability = 0.25

# true_maze = Maze(rows, cols, wallProbability)
# print("True Maze:")
# true_maze.print()

# success, path = walk(true_maze)

# print("Success Status: " + str(success))
# print("Path:")
# for i in path:
#    i.print()

# path_maze = true_maze
# print("\n\nVISUALIZED PATH:")
# printPath(path_maze, path)

mazes = []
paths = []

successes = 0
total_mazes = 1000

total_fhexpand = 0
total_flexpand = 0
total_bexpand = 0
total_aexpand = 0

total_fhtime = 0
total_fltime = 0
total_btime = 0
total_atime = 0


orig_stdout = sys.stdout
with open("mazes.txt", "w") as f:
    sys.stdout = f
    for x in range(0, total_mazes):
        true_maze = Maze(rows, cols, wallProbability)
        print("\nMAZE " + str(x))
        print("START: (" + str(true_maze.agent_row) + ", " + str(true_maze.agent_col) + ")")
        print("GOAL: (" + str(true_maze.goal_row) + ", " + str(true_maze.goal_col) + ")\n")

        fhstart_time = time.time()
        print("\n(Forward Favoring High G Values)\n")
        fhsuccess, fhpath, fhexpand = forward_a_star_walk_favor_high_g_values(true_maze)
        print("\n(Forward Favoring High G Values Final Path)\n")
        printPath(true_maze, fhpath)
        total_fhtime += time.time() - fhstart_time
        total_fhexpand += fhexpand

        flstart_time = time.time()
        print("\n(Forward Favoring Low G Values)\n")
        flsuccess, flpath, flexpand = forward_a_star_walk_favor_low_g_values(true_maze)
        print("\n(Forward Favoring Low G Values Final Path)\n")
        printPath(true_maze, flpath)
        total_fltime += time.time() - flstart_time
        total_flexpand += flexpand

        bstart_time = time.time()
        print("\n(Backward)\n")
        bsuccess, bpath, bexpand = backwards_a_star_walk(true_maze)
        print("\n(Backward Final Path)\n")
        printPath(true_maze, bpath)
        total_btime += time.time() - bstart_time
        total_bexpand += bexpand

        astart_time = time.time()
        print("\n(Adaptive)\n")
        asuccess, apath, aexpand = adaptive_a_star_walk(true_maze)
        print("\n(Adaptive Final Path)\n")
        printPath(true_maze, apath)
        total_atime += time.time() - astart_time
        total_aexpand += aexpand

        print("Was maze a success: " + str(fhsuccess))
        print("Forward Expanded Nodes (Favoring High G Values): " + str(fhexpand) +
              " // Forward Expanded Nodes (Favoring Low G Values): " + str(flexpand) +
              " \nBackward Expanded Nodes: " + str(bexpand) +
              " // Adaptive Expanded Nodes: " + str(aexpand) + "\n--------")
        if fhsuccess or flsuccess or bsuccess or asuccess:
            successes += 1
        mazes.append(true_maze)
        paths.append(paths)

    print("\n\nSolved Mazes: " + str(successes))

    print("\n\nOverall Statistics:")
    print("Average Number of Expanded Cells per Maze for Forward Favoring High G Values = " + str(total_fhexpand / total_mazes))
    print("Average Time per Maze for Forward Favoring High G Values = " + str(total_fhtime / total_mazes) + " seconds")
    print("Average Number of Expanded Cells per Maze for Forward Favoring Low G Values = " + str(total_flexpand / total_mazes))
    print("Average Time per Maze for Forward Favoring Low G Values = " + str(total_fltime / total_mazes) + " seconds")
    print("Average Number of Expanded Cells per Maze for Backward = " + str(total_bexpand / total_mazes))
    print("Average Time per Maze for Backward = " + str(total_btime / total_mazes) + " seconds")
    print("Average Number of Expanded Cells per Maze for Adaptive = " + str(total_aexpand / total_mazes))
    print("Average Time per Maze for Adaptive = " + str(total_atime / total_mazes) + " seconds")

    sys.stdout = orig_stdout
