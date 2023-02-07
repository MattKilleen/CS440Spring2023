import random

# "a" signifies the agent
# "g" signifies the goal
# 0 signifies a wall
# 1 signifies no wall

def generate_random_maze(rows, cols):
    maze = [[random.choice([0, 1]) for j in range(cols)] for i in range(rows)]
    agent_row = random.randint(0, rows-1)
    agent_col = random.randint(0, cols-1)
    goal_row = random.randint(0, rows-1)
    goal_col = random.randint(0, cols-1)
    maze[agent_row][agent_col] = "a"
    maze[goal_row][goal_col] = "g"
    return maze, agent_row, agent_col, goal_row, goal_col

rows = 10
cols = 10
maze, agent_row, agent_col, goal_row, goal_col = generate_random_maze(rows, cols)

for row in maze:
    print(row)

def a_star(inital_position, goal_position, maze):
    pass
