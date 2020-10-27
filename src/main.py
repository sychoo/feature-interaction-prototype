# Designed by Simon Chu
# Thu Sep 24 16:01:06 EDT 2020

# imported modules
import parser # for parsing the mathematical formulas
import math # for math calculations
import statistics # for statistical analysis (mean, variance, etc)
import numpy as np # numpy for array generations

# import from my support libaries
from map_utils import Map, Map_Cell, Coord
from drone_utils import EgoDrone, EnemyDrone
from flight import Mission_Planner
from signal_utils import Signal_Estimator, STL, Robustness, Signal_Element


if __name__ == "__main__":

    # Experiment 1: Fixed Mission, predict the safety of the flight given
    #
    # Interception
    #
    # - the flight mission
    # - the threat model of the enemy drone (chasing the ego drone)
    # - the starting positions of ego drone and enemy drones
    # 
    #
    # ego drone starting position:   (0, 20)
    # enemy drone starting position: (20, 20)
    # mission: x^2
    # requirement: only path of the ego drone is visible, and has robustness value
    # half static, half dynamic

    ###### execute flight mission #####

    # init feature object
    mission_obj = Mission_Planner()

    # create a 21 x 21 map (odd number, with center)
    mission_obj.create_internal_map(21, 21)

    # link the map object to the drones
    ego_drone = EgoDrone(mission_obj.get_internal_map())
    enemy_drone = EnemyDrone(mission_obj.get_internal_map())

    # set the initial positions for teh ego drone and the enemy drone
    ego_drone.set_init_coord(Coord(0, 20))
    enemy_drone.set_init_coord(Coord(5, 5))

    # add enemy drone and ego drone
    mission_obj.add_drone(ego_drone)
    mission_obj.add_drone(enemy_drone)

    # start the feature object, with step number = 23
    mission_obj.run(23)
   
    # animate the flight path
    mission_obj.get_flight_path().animate()

    ###### /execute flight mission #####


    ##### to do: estimate the signal in the execution loop, to deviate from the original flight mission
    ##### flight estimation testing #####
    # estimate flight path with the fixed mission (given start position, drones, and lookahead time)
    # current_signal = {"time": 0, "Ego": {"current_coords": (0, 20)}, "Enemy": {"current_coords": (0, 5)}}#Signal_Element()
    current_signal_element = Signal_Element(0, {"Ego": {"current_coords": {"x_cor": 0, "y_cor": 20}, "init_coords": {"x_cor": 0, "y_cor": 20}}, "Enemy": {"current_coords": {"x_cor": 0, "y_cor": 5}, "init_coords": {"x_cor": 0, "y_cor": 5}}})
    signal_estimator = Signal_Estimator(current_signal_element)

    # create identical maps for drones
    est_internal_map = Map(21, 21)

    est_ego_drone = EgoDrone(est_internal_map)
    est_enemy_drone = EnemyDrone(est_internal_map)

    # set the initial positions for teh ego drone and the enemy drone
    # find the initial location for the drones
    # ! no work around due to how flight mission/path is encoded
    # to-do: change how flight mission is encoded

    ego_init_x = current_signal_element.get_signal_data_by_id_key(est_ego_drone.identifier, "init_coords")["x_cor"]
    ego_init_y = current_signal_element.get_signal_data_by_id_key(est_ego_drone.identifier, "init_coords")["y_cor"]
    enemy_init_x = current_signal_element.get_signal_data_by_id_key(est_enemy_drone.identifier, "init_coords")["x_cor"]
    enemy_init_y = current_signal_element.get_signal_data_by_id_key(est_enemy_drone.identifier, "init_coords")["y_cor"]

    est_ego_drone.set_init_coord(Coord(ego_init_x, ego_init_y))
    est_enemy_drone.set_init_coord(Coord(enemy_init_x, enemy_init_y))

    signal_estimator.add_drone(est_ego_drone)
    signal_estimator.add_drone(est_enemy_drone)

    # estimate the entirety of the mission, given the lookahead time
    signal_estimator.fixed_mission_estimate(23)

    # maybe change the time_span
    estimated_signal = signal_estimator.get_signal_estimation()

    # debugger
    print(estimated_signal)



    # ideal function invocation
    # stl_formula_1 = STL() # distance_to_boundary > 3.0
    # stl_formula_2 = STL() # distance_to_enemy > 3.0

    # robustness_stl_formula_1 = Robustness(stl_formula_1, estimated_signal).evaluate()
    # robustness_stl_formula_2 = Robustness(stl_formula_2, estimated_signal)

    # print("STL 1: " + str(robustness_stl_formula_1))
    # print("STL 2: " + str(robustness_stl_formula_2))

    # if robustness_stl_formula_1 < 0 and robustness_stl_formula_2 < 0:
    #     print("Detected conflicts between requirements!")
    # else:
    #     print("No conflict between requirements.")



    # current work-around
    # evaluate the robustness of the signal with respect to the boundary

    # print("STL 1: " + str(robustness_stl_formula_1))
    # print("STL 2: " + str(robustness_stl_formula_2))
    robustness_stl_formula_1 = STL().evaluate_boundary_robustness(estimated_signal, 21, 21)
    robustness_stl_formula_2 = STL().evaluate_enemy_robustness(estimated_signal, 21, 21)

    print("STL 1: " + str(robustness_stl_formula_1))
    print("STL 2: " + str(robustness_stl_formula_2))

    if robustness_stl_formula_1 < 0 and robustness_stl_formula_2 < 0:
        print("Detected conflicts between requirements!")
    else:
        print("No conflict between requirements.")
    ##### /flight estimation testing #####

    # display the initial output to show the path

    # mission_obj.get_internal_map().visualize_output_map()
    # mission_obj.display_heatmap()


    # compute the static robustness score for map cells

    # mission_obj.compute_static_robustness()
    # mission_obj.compute_output()
    # mission_obj.display_heatmap()