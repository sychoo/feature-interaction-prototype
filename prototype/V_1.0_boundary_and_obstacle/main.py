# Designed by Simon Chu
# Thu Sep 24 11:55:14 EDT 2020

# calculate robustness value using distance to boundary and distance to obstacle (whichever has the least robustness)

# using seaborn and matplotlib library for data visualization (heatmap)
import math
import numpy as np
import seaborn as sns
sns.set_theme()
import matplotlib.pyplot as plt

# parameter to adjust
x_length = 20 # length of map
y_length = 20 # height of map

# minimal safety distance is 3.0 by default
minimal_safety_distance = 3.0 # the minimal safety distance between the drone and the boundary
exists_obstacle = True # set whether the obstracle exists
obstacle_locs = [(4, 6), (20, 40), (30, 30), (30, 31), (31, 30), (31, 31), (40, 20)] # the coordinates of the obstacles relatively to the boundary

# function to calculate the robustness value based on the current cell coordinates
def robustness(x, y, x_length, y_length):
    top_boundary_y = 0
    left_boundary_x = 0
    right_boundary_x = x_length - 1
    bottom_boundary_y = y_length - 1
    
    distance_to_top = y - top_boundary_y
    distance_to_bottom = bottom_boundary_y - y
    distance_to_left = x - left_boundary_x
    distance_to_right = right_boundary_x - x

    min_distance_to_boundary = min(distance_to_top, distance_to_bottom, distance_to_left, distance_to_right)
    min_distance_to_collision = 0

    # find the minimal distance to the obstacle
    if (exists_obstacle):
        min_distance_to_obstacle = max(x_length, y_length)
        for coord in obstacle_locs:
            distance_to_obstacle = math.sqrt((x - coord[0])**2 + (y - coord[1])**2)
            if distance_to_obstacle < min_distance_to_obstacle:
                min_distance_to_obstacle = distance_to_obstacle

        min_distance_to_collision = min(min_distance_to_obstacle, min_distance_to_boundary)
    else:
        min_distance_to_collision = min_distance_to_boundary

    robustness_value = min_distance_to_collision - minimal_safety_distance

    # scale the robustness value to a scale of -1 to 1 (inclusive)
    robustness_min = -1 * minimal_safety_distance
    robustness_max = max(x_length, y_length) / 2 - 1
    scaled_robustness_value = 0

    if robustness_value < 0:
        scaled_robustness_value = (robustness_value - robustness_min) / (-1 * robustness_min) - 1
    else:
        scaled_robustness_value = robustness_value / robustness_max

    # penalize negative robustness scores
    alpha = 32
    penalized_robustness_value = 0

    if robustness_value < 0:
       penalized_robustness_value = robustness_value - (alpha**(-robustness_value - 1)/(alpha - 1))
    else:
        penalized_robustness_value = robustness_value
    
    # return penalized_robustness_value
    return scaled_robustness_value

# STL requirement: the distance between the drone and the boundary to an unsafe region must be at least 3.0 meters
# p(fi, s, t) represents how far beyond 3.0 meters the drone is able to maintain its distance

# initialize a 2D array
data = [ [0 for _ in range(x_length) ] for _ in range(y_length)]

for y in range(y_length):
    for x in range(x_length):
        data[y][x] = robustness(x, y, x_length, y_length)

# data = [[1,2,3,4,5],[5,4,3,2,1]]

# Note that data drawn on the graph starts with the Top-Left corner of the graph (Origin)

# seaborn color palettes
# http://seaborn.pydata.org/tutorial/color_palettes.html
# ax = sns.heatmap(data, cmap="YlGnBu")

# Heatmaps
# https://seaborn.pydata.org/generated/seaborn.heatmap.html

# annotated heatmap
# ax = sns.heatmap(data, cmap="coolwarm_r", annot=True, fmt=".1f")

# non-annotated heatmap
# ax = sns.heatmap(data, cmap="coolwarm_r")

ax = sns.heatmap(data, cmap="Spectral")

plt.tick_params(axis='both', which='major', labelsize=10, labelbottom = False, bottom=False, top = False, labeltop=True, length=0)
plt.show()
