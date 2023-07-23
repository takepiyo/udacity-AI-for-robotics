# --------------
# USER INSTRUCTIONS
#
# Write a function called stochastic_value that
# returns two grids. The first grid, value, should
# contain the computed value of each cell as shown
# in the video. The second grid, policy, should
# contain the optimum policy for each cell.
#
# --------------
# GRADING NOTES
#
# We will be calling your stochastic_value function
# with several different grids and different values
# of success_prob, collision_cost, and cost_step.
# In order to be marked correct, your function must
# RETURN (it does not have to print) two grids,
# value and policy.
#
# When grading your value grid, we will compare the
# value of each cell with the true value according
# to this model. If your answer for each cell
# is sufficiently close to the correct answer
# (within 0.001), you will be marked as correct.

delta = [[-1, 0], [0, -1], [1, 0], [0, 1]]  # go up  # go left  # go down  # go right

delta_name = ["^", "<", "v", ">"]  # Use these when creating your policy grid.

# ---------------------------------------------
#  Modify the function stochastic_value below
# ---------------------------------------------


def stochastic_value(grid, goal, cost_step, collision_cost, success_prob):
    failure_prob = (
        1.0 - success_prob
    ) / 2.0  # Probability(stepping left) = prob(stepping right) = failure_prob
    value = [
        [collision_cost for col in range(len(grid[0]))] for row in range(len(grid))
    ]
    policy = [[" " for col in range(len(grid[0]))] for row in range(len(grid))]

    change = True
    while change:
        # for row in policy:
        #     print(row)
        change = False
        for y in range(len(grid)):
            for x in range(len(grid[0])):
                if x == goal[1] and y == goal[0]:
                    if value[y][x] > 0.0:
                        value[y][x] = 0.0
                        policy[y][x] = "*"
                        change = True

                elif grid[y][x] == 0:
                    for i in range(len(delta)):
                        v = 0
                        if is_collision(y, x, delta[i % len(delta)]):
                            v += success_prob * value[y + delta[i][0]][x + delta[i][1]]
                        else:
                            v += success_prob * collision_cost
                        if is_collision(y, x, delta[(i + 1) % len(delta)]):
                            v += (
                                failure_prob
                                * value[y + delta[(i + 1) % len(delta)][0]][
                                    x + delta[(i + 1) % len(delta)][1]
                                ]
                            )
                        else:
                            v += failure_prob * collision_cost
                        if is_collision(y, x, delta[(i - 1) % len(delta)]):
                            v += (
                                failure_prob
                                * value[y + delta[(i - 1) % len(delta)][0]][
                                    x + delta[(i - 1) % len(delta)][1]
                                ]
                            )
                        else:
                            v += failure_prob * collision_cost
                        v += cost_step

                        if v < value[y][x]:
                            value[y][x] = v
                            policy[y][x] = delta_name[i]
                            change = True
    return value, policy


def is_collision(y, x, shift):
    if (
        y + shift[0] >= 0
        and y + shift[0] < len(grid)
        and x + shift[1] >= 0
        and x + shift[1] < len(grid[0])
    ):
        if grid[y + shift[0]][x + shift[1]] == 0:
            return True
    return False


# ---------------------------------------------
#  Use the code below to test your solution
# ---------------------------------------------

grid = [
    [0, 0, 0, 1, 0, 0, 0],
    [0, 1, 0, 0, 0, 1, 0],
    [0, 1, 1, 0, 1, 1, 0],
    [0, 1, 1, 1, 1, 1, 0],
    [0, 0, 0, 0, 0, 0, 0],
]
goal = [0, 6]
cost_step = 1
collision_cost = 100
success_prob = 0.8

value, policy = stochastic_value(grid, goal, cost_step, collision_cost, success_prob)
for row in value:
    print(row)
for row in policy:
    print(row)

# Expected outputs:
#
# [471.9397246855924, 274.85364957758316, 161.5599867065471, 0],
# [334.05159958720344, 230.9574434590965, 183.69314862430264, 176.69517762501977],
# [398.3517867450282, 277.5898270101976, 246.09263437756917, 335.3944132514738],
# [700.1758933725141, 1000, 1000, 668.697206625737]


#
# ['>', 'v', 'v', '*']
# ['>', '>', '^', '<']
# ['>', '^', '^', '<']
# ['^', ' ', ' ', '^']
