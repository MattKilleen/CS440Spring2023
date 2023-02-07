from pyamaze import maze, agent


def create_maze(width, height):
    m = maze(width, height)
    m.CreateMaze(loopPercent=50)
    a = agent(m, filled=True, footprints=True)
    return m, a


def run_maze(m, a):
    m.tracePath({a: m.path})
    m.run()


m, a = create_maze(101, 101)
run_maze(m, a)


def a_star(inital_position, goal_position, maze):
    pass
