this is a prototype using the boundary invariant

# Parameters that are interesting to adjust
- whether to return scaled_robustness_value or
  penalized_robustness_value
- minimal_safety_distance
- x_length and y_length (by default 50x50)
- whether there are obstacles and if so, specify the obstacle
  coordinates in obstacle_locs

# to do
- put a slider for different parameters
  - such as minimal safety distance
  - x_length = y_length, adjustment
  - enter obstacles
  - alpha (higher alpha values result in steeper exponential for the
    requirements of the autonomous drone
