import random

def generate_random_maze(rows, cols):
    maze = [[0 for j in range(cols)] for i in range(rows)]
    for i in range(rows):
        for j in range(cols):
            if i == 0 or i == rows-1 or j == 0 or j == cols-1:
                maze[i][j] = 0
            else:
                maze[i][j] = random.choice([0, 1])
    maze[1][1] = "a"
    maze[rows-2][cols-2] = "g"
    return maze

rows = 5
cols = 7
maze = generate_random_maze(rows, cols)
for row in maze:
    print(row)

def a_star(inital_position, goal_position, maze):
    pass
