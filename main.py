import random
import numpy as np
import queue


# "a" signifies the agent
# "g" signifies the goal
# "0" signifies a wall
# "1" signifies no wall

class MazeEntry:
    def __init__(self, row, col, statusValue, cost=None, heuristic=None):
        self.row = row
        self.col = col
        self.cost = cost
        self.heuristic = heuristic
        self.status = statusValue
        self.parent = None

    def print(self):
        print("[" + str(self.row) + ", " + str(self.col) + "]")


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


def a_star(initial_position, goal_position, known_maze):
    initial_node = MazeEntry(initial_position[0], initial_position[1], "1", 0, manhattan_distance_heuristic(initial_position, goal_position))
    q = [initial_node]
    expandedList = {}
    while q:
        x = q[0]
        q.remove(x)
        if expandedList.setdefault((x.row, x.col)) is not None:
            continue
        expandedList[(x.row, x.col)] = True
        if x.row == goal_position[0] and x.col == goal_position[1]:
            path = [x]
            while x.parent is not None:
                x = x.parent
                path.append(x)
            path.reverse()
            # Passed - A Star Test (and thus findNeighbors is verified)
            #print("Path From A Star:")
            #for i in path:
            #    i.print()
            return True, path
        for i in findNeighbors([x.row, x.col], known_maze):
            if expandedList.setdefault((i.row, i.col)) is None:
                i.parent = x
                i.cost = x.cost + 1
                i.heuristic = manhattan_distance_heuristic([i.row, i.col], goal_position)
                q = addToQueue(q, i)
    return False, []


def walk(true_maze):
    known_maze = Maze(rows, cols, 0, true_maze.agent_row, true_maze.agent_col, true_maze.goal_row, true_maze.goal_col)
    print("Known Maze:")
    known_maze.print()
    current_position = [true_maze.agent_row, true_maze.agent_col]
    goal_position = [true_maze.goal_row, true_maze.goal_col]
    actual_path = [MazeEntry(current_position[0], current_position[1], "0")]
    success, planned_path = a_star(current_position, goal_position, known_maze)
    if not success:
        return False, []
    iteration = 0
    while not (current_position[0] == true_maze.goal_row and current_position[1] == true_maze.goal_col or iteration > 10):
        newWallFound = update_adjacent_spaces(current_position, true_maze, known_maze)
        if newWallFound:
            success, planned_path = a_star(current_position, goal_position, known_maze)
            if not success:
                return False, []
        planned_path.remove(planned_path[0])
        current_position[0] = planned_path[0].row
        current_position[1] = planned_path[0].col
        actual_path.append(MazeEntry(current_position[0], current_position[1], "0"))
        iteration += 1
    return True, actual_path


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


rows = 5
cols = 5
wallProbability = 0.5

true_maze = Maze(rows, cols, wallProbability)
print("True Maze:")
true_maze.print()

success, path = walk(true_maze)

print("Success Status: " + str(success))
print("Path:")
for i in path:
    i.print()

# Passed - Manhattan Test
#print("Manhattan Test:")
#print(manhattan_distance_heuristic([3,4],[0,4]))

# Passed - Add to Queue Test
#print("AddToQueue Test:")
#entry1 = MazeEntry(1,1,"1",0,1)
#entry2 = MazeEntry(2,2,"1",1,2)
#entry3 = MazeEntry(3,3,"1",2,3)
#entry4 = MazeEntry(4,4,"1",4,6)
#q = [entry1, entry2, entry3, entry4]
#q = addToQueue(q, MazeEntry(5,5,"1",1,3))
#for i in q:
#    i.print()