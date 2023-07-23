# ----------
# User Instructions:
#
# Create a function compute_value which returns
# a grid of values. The value of a cell is the minimum
# number of moves required to get from the cell to the goal.
#
# If a cell is a wall or it is impossible to reach the goal from a cell,
# assign that cell a value of 99.
# ----------

grid = [
    [0, 1, 0, 0, 0, 0],
    [0, 1, 0, 0, 0, 0],
    [0, 1, 0, 0, 0, 0],
    [0, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 0],
]
goal = [len(grid) - 1, len(grid[0]) - 1]
cost = 1  # the cost associated with moving from a cell to an adjacent one

delta = [[-1, 0], [0, -1], [1, 0], [0, 1]]  # go up  # go left  # go down  # go right

delta_name = ["^", "<", "v", ">"]

g_pos_list = []


def compute_value(grid, goal, cost):
    value = [[99] * len(grid[0]) for i in range(len(grid))]
    current_pos = goal
    current_g = 0
    add_g(current_g, current_pos)
    grid[current_pos[0]][current_pos[1]] = 1
    value[current_pos[0]][current_pos[1]] = current_g
    while len(g_pos_list) != 0:
        current_g, current_pos[0], current_pos[1] = min_g()

        for direction in delta_name:
            if is_enabled_move(grid, current_pos, direction):
                shift = delta[delta_name.index(direction)]
                shifted_pos = [l + dl for l, dl in zip(current_pos, shift)]
                shifted_g = current_g + cost
                add_g(shifted_g, shifted_pos)
                grid[shifted_pos[0]][shifted_pos[1]] = 1
                value[shifted_pos[0]][shifted_pos[1]] = shifted_g

    return value


def is_enabled_move(grid, pos, direction):
    shift = delta[delta_name.index(direction)]
    pos = [l + dl for l, dl in zip(pos, shift)]

    y_enabled_flag = pos[0] >= 0 and pos[0] <= len(grid) - 1
    x_enabled_flag = pos[1] >= 0 and pos[1] <= len(grid[0]) - 1
    occupied_flag = False
    if y_enabled_flag and x_enabled_flag:
        occupied_flag = grid[pos[0]][pos[1]] != 1

    return occupied_flag


def add_g(g_value, pos):
    g_pos_list.append([g_value, pos[0], pos[1]])


def min_g():
    min_g = g_pos_list[0][0]
    min_index = 0
    for i, g_pos in enumerate(g_pos_list):
        if g_pos[0] < min_g:
            min_index = i
            min_g = g_pos[0]
    return g_pos_list.pop(min_index)


for row in compute_value(grid, goal, cost):
    print(row)
