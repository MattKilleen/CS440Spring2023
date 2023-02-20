import random, sys

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
        return(str(self.row) + "," + str(self.col))


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
def forward_a_star_walk(true_maze):
    # In addition to the true maze which we are to navigate though, create a known_maze,
    # representing the maze as the agent knows it. The agent does not initially know the maze,
    # other than its starting point and the goal point. It initially assumes that no spaces contain walls.
    known_maze = Maze(rows, cols, 0, true_maze.agent_row, true_maze.agent_col, true_maze.goal_row, true_maze.goal_col)
        #print("Known Maze:")
        #known_maze.print()

    # Initialize the current position of the agent and its goal
    current_position = [true_maze.agent_row, true_maze.agent_col]
    goal_position = [true_maze.goal_row, true_maze.goal_col]

    # Initialize a list to hold the actual path that the agent has followed.
    # It begins by only containing a MazeEntry object representing its starting point
    actual_path = [MazeEntry(current_position[0], current_position[1], "0")]

    # Use A* search to generate a planned path to the goal based on the current state of the known_maze
    success, planned_path = forward_a_star(current_position, goal_position, known_maze)

    # If no path could be found, return false, indicating failure, and an empty list
    if not success:
        return False, []

    # Iterate until the goal has been reached
    while not (current_position[0] == true_maze.goal_row and current_position[1] == true_maze.goal_col):
        # Search for any new walls adjacent to the agent in the true maze and update the known_maze
        newWallFound = update_adjacent_spaces(current_position, true_maze, known_maze)

        # If a new wall was found, use A* search to regenerate the planned path based on the new state of the known_maze
        # If no path can be found, return false, indicating failure, and an empty list
        if newWallFound:
            success, planned_path = forward_a_star(current_position, goal_position, known_maze)
            if not success:
                return False, []

        # Remove the current element of the planned path and update the current position of the agent for the next iteration
        planned_path.remove(planned_path[0])
        current_position[0] = planned_path[0].row
        current_position[1] = planned_path[0].col

        # Add the updated current position of the agent to the actual path
        actual_path.append(MazeEntry(current_position[0], current_position[1], "0"))

    # If we break from the while loop (the agent reached the goal), return true, indicating success,
    # and the actual path followed by the agent
    return True, actual_path

def backwards_a_star_walk(true_maze):
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
    actual_path = [MazeEntry(goal_position[0], goal_position[1], "0")]

    # Use A* search to generate a planned path to the goal based on the current state of the known_maze
    success, planned_path = backwards_a_star(current_position, goal_position, known_maze)

    # If no path could be found, return false, indicating failure, and an empty list
    if not success:
        return False, []

    # Iterate until the goal has been reached
    while not (goal_position[0] == true_maze.goal_row and goal_position[1] == true_maze.goal_col):
        # Search for any new walls adjacent to the agent in the true maze and update the known_maze
        newWallFound = update_adjacent_spaces(goal_position, true_maze, known_maze)

        # If a new wall was found, use A* search to regenerate the planned path based on the new state of the known_maze
        # If no path can be found, return false, indicating failure, and an empty list
        if newWallFound:
            success, planned_path = backwards_a_star(current_position, goal_position, known_maze)
            if not success:
                return False, []

        # Remove the current element of the planned path and update the current position of the agent for the next iteration
        planned_path.remove(planned_path[0])
        goal_position[0] = planned_path[0].row
        goal_position[1] = planned_path[0].col

        # Add the updated current position of the agent to the actual path
        actual_path.append(MazeEntry(current_position[0], current_position[1], "0"))

    # If we break from the while loop (the agent reached the goal), return true, indicating success,
    # and the actual path followed by the agent
    return True, actual_path

# Update the spaces in the known_maze which are adjacent to current_position
# by assigning them the values of the corresponding spaces in the true_maze.
# This allows the agent to update its understanding of where walls are in the maze.
# If a new wall is detected, return true, indicating that regenerating the planned path is necessary.
# Otherwise, return false.
def update_adjacent_spaces(current_position, true_maze, known_maze):
    newWallFound = False
    if current_position[0] != 0:
        if true_maze.content[(current_position[0] - 1, current_position[1])].status == "0" and known_maze.content[(current_position[0] - 1, current_position[1])].status == "1":
            known_maze.content[(current_position[0] - 1, current_position[1])].status = "0"
            newWallFound = True
    if current_position[0] != true_maze.rows - 1:
        if true_maze.content[(current_position[0] + 1, current_position[1])].status == "0" and known_maze.content[(current_position[0] + 1, current_position[1])].status == "1":
            known_maze.content[(current_position[0] + 1, current_position[1])].status = "0"
            newWallFound = True
    if current_position[1] != 0:
        if true_maze.content[(current_position[0], current_position[1] - 1)].status == "0" and known_maze.content[(current_position[0], current_position[1] - 1)].status == "1":
            known_maze.content[(current_position[0], current_position[1] - 1)].status = "0"
            newWallFound = True
    if current_position[1] != true_maze.cols - 1:
        if true_maze.content[(current_position[0], current_position[1] + 1)].status == "0" and known_maze.content[(current_position[0], current_position[1] + 1)].status == "1":
            known_maze.content[(current_position[0], current_position[1] + 1)].status = "0"
            newWallFound = True
    return newWallFound


# Perform A* search on the known maze, beginning at initial_position, and targeting goal_position
def forward_a_star(initial_position, goal_position, known_maze):
    # create the initial node in the tree based on the initial_position
    initial_node = MazeEntry(initial_position[0], initial_position[1], "1", 0, manhattan_distance_heuristic(initial_position, goal_position))

    # initialize the queue with only the initial_node
    q = [initial_node]

    # initialize the list of expanded nodes (implemented using a dictionary)
    expandedList = {}

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

        # If this node is the goal, return True, indicating success, as well as the path,
        # Which is obtaining by following the parents of each node, up the tree
        if x.row == goal_position[0] and x.col == goal_position[1]:
            path = [x]
            while x.parent is not None:
                x = x.parent
                path.append(x)
            path.reverse()
            # Passed - A Star Test (and thus findNeighbors is verified)
            # print("Path From A Star:")
            # for i in path:
            #    i.print()
            return True, path

        # Find the neighbors of the current node, and for each neighbor, create a MazeEntry object to represent it,
        # and add it to the queue in order of increasing cost + heuristic
        for i in findNeighbors([x.row, x.col], known_maze):
            if expandedList.setdefault((i.row, i.col)) is None:
                i.parent = x
                i.cost = x.cost + 1
                i.heuristic = manhattan_distance_heuristic([i.row, i.col], goal_position)
                q = addToQueue(q, i)

    # If we exited from the while loop, meaning that the queue became empty without finding the goal,
    # return false, indicating failure, and an empty list
    return False, []

def backwards_a_star(initial_position, goal_position, known_maze):
    # create the initial node in the tree based on the initial_position
    initial_node = MazeEntry(goal_position[0], goal_position[1], "1", 0,
                             manhattan_distance_heuristic(goal_position, initial_position))

    # initialize the queue with only the initial_node
    q = [initial_node]

    # initialize the list of expanded nodes (implemented using a dictionary)
    expandedList = {}

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

        # If this node is the goal, return True, indicating success, as well as the path,
        # Which is obtaining by following the parents of each node, up the tree
        if x.row == initial_position[0] and x.col == initial_position[1]:
            path = [x]
            while x.parent is not None:
                x = x.parent
                path.append(x)
            path.reverse()
            # Passed - A Star Test (and thus findNeighbors is verified)
            # print("Path From A Star:")
            # for i in path:
            #    i.print()
            return True, path

        # Find the neighbors of the current node, and for each neighbor, create a MazeEntry object to represent it,
        # and add it to the queue in order of increasing cost + heuristic
        for i in findNeighbors([x.row, x.col], known_maze):
            if expandedList.setdefault((i.row, i.col)) is None:
                i.parent = x
                i.cost = x.cost + 1
                i.heuristic = manhattan_distance_heuristic([i.row, i.col], initial_position)
                q = addToQueue(q, i)


# Find all neighbors of a node based on its current position and the content of the known maze
# Any neighbors which contain a wall are ignored
def findNeighbors(current_position, known_maze):
    neighbors = []
    if current_position[0] != 0 and known_maze.content[(current_position[0] - 1, current_position[1])].status != "0":
        neighbors.append(MazeEntry(current_position[0] - 1, current_position[1], "1"))
    if current_position[0] != known_maze.rows - 1 and known_maze.content[(current_position[0] + 1, current_position[1])].status != "0":
        neighbors.append(MazeEntry(current_position[0] + 1, current_position[1], "1"))
    if current_position[1] != 0 and known_maze.content[(current_position[0], current_position[1] - 1)].status != "0":
        neighbors.append(MazeEntry(current_position[0], current_position[1] - 1, "1"))
    if current_position[1] != known_maze.cols - 1 and known_maze.content[(current_position[0], current_position[1] + 1)].status != "0":
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
def addToQueue(q, node):
    j = len(q)
    q_new = []
    for i in range(len(q)):
        nodeValue = node.cost + node.heuristic
        entryValue = q[i].cost + q[i].heuristic
        if nodeValue < entryValue:
            j = i
            break
    for i in range(0, j):
        q_new.append(q[i])
    q_new.append(node)
    for i in range(j+1, len(q)+1):
        q_new.append(q[i-1])
    return q_new


# PRINTS THE VISUAL PATH
def printPath(maze, path):
    row = []
    for i in range(maze.rows):
        strRow = ""
        for j in range(maze.cols):
            if(maze.content[(i, j)].status == "1"):
                strRow += "░"
            if(maze.content[(i, j)].status == "0"):
                strRow += "█"
            if(maze.content[(i, j)].status == "A"):
                strRow += "A"
            if(maze.content[(i, j)].status == "G"):
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
        row[x] = row[x][:yCoords[index]] + "▒" + row[x][yCoords[index] + 1:]

    for i in row:
        print(i)



rows = 15
cols = 35
wallProbability = 0.25

#true_maze = Maze(rows, cols, wallProbability)
#print("True Maze:")
#true_maze.print()

#success, path = walk(true_maze)

#print("Success Status: " + str(success))
#print("Path:")
#for i in path:
#    i.print()

#path_maze = true_maze
#print("\n\nVISUALIZED PATH:")
#printPath(path_maze, path)

mazes = []
paths = []

successes = 0

orig_stdout = sys.stdout
with open("mazes.txt", "w") as f:
    for x in range(0, 50):
        sys.stdout = f
        true_maze = Maze(rows, cols, wallProbability)
        print("\nMAZE " + str(x))
        print("START: (" + str(true_maze.agent_row) + ", " + str(true_maze.agent_col) + ")")
        print("GOAL: (" + str(true_maze.goal_row) + ", " + str(true_maze.goal_col) + ")\n")
        success, path = forward_a_star_walk(true_maze)
        successBackStar, pathBackStar = backwards_a_star_walk(true_maze)
        print("Forward A*: ")
        printPath(true_maze, path)
        print("Backward A*: ")
        printPath(true_maze, pathBackStar)
        print("\n(Success: " + str(success) + ")\n\n--------")
        if (success):
            successes += 1
        if(successBackStar):
            success += 1
        mazes.append(true_maze)
        paths.append(paths)

    print("\n\nSolved Mazes: " + str(successes))
    sys.stdout = orig_stdout
