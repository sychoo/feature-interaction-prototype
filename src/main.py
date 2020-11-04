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
from signal_utils import Signal_Estimator, Robustness, Signal_Element
import STL

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

    is_execute_flight_mission = False

    if is_execute_flight_mission == True:
        ###### execute flight mission #####

        # init feature object
        mission_obj = Mission_Planner()

        # create a 21 x 21 map (odd number, with center)
        mission_obj.create_internal_map(21, 21)

        # link the map object to the drones
        ego_drone = EgoDrone(mission_obj.get_internal_map())
        enemy_drone = EnemyDrone(mission_obj.get_internal_map())

        # set the initial positions for teh ego drone and the enemy drone

        # default demo
        ego_drone.set_init_coord(Coord(0, 20))
        enemy_drone.set_init_coord(Coord(5, 5))

        # ego_drone.set_init_coord(Coord(2, 20))
        # enemy_drone.set_init_coord(Coord(1, 6))

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

    # default demo
    current_signal_element = Signal_Element(0, {"Ego": {"current_coord": Coord(1, 20), "init_coord": Coord(1, 20)}, "Enemy": {"current_coord": Coord(0, 5), "init_coord": Coord(0, 5)}})

    # modified demo
    # current_signal_element = Signal_Element(0, {"Ego": {"current_coord": Coord(2, 20), "init_coord": Coord(1, 20)}, "Enemy": {"current_coord": Coord(1, 6), "init_coord": Coord(0, 5)}})

    signal_estimator = Signal_Estimator(current_signal_element)

    # create identical maps for drones
    est_internal_map = Map(21, 21)

    est_ego_drone = EgoDrone(est_internal_map)
    est_enemy_drone = EnemyDrone(est_internal_map)

    # set the initial positions for teh ego drone and the enemy drone
    # find the initial location for the drones
    # ! no work around due to how flight mission/path is encoded
    # to-do: change how flight mission is encoded

    # ego_init_x = current_signal_element.get_signal_data_by_id_key(est_ego_drone.identifier, "init_coords")["x_cor"]
    # ego_init_y = current_signal_element.get_signal_data_by_id_key(est_ego_drone.identifier, "init_coords")["y_cor"]
    # enemy_init_x = current_signal_element.get_signal_data_by_id_key(est_enemy_drone.identifier, "init_coords")["x_cor"]
    # enemy_init_y = current_signal_element.get_signal_data_by_id_key(est_enemy_drone.identifier, "init_coords")["y_cor"]

    ego_init_coord = current_signal_element.get_signal_data_by_id_key(est_ego_drone.identifier, "init_coord")
    enemy_init_coord = current_signal_element.get_signal_data_by_id_key(est_enemy_drone.identifier, "init_coord")

    ego_current_coord = current_signal_element.get_signal_data_by_id_key(est_ego_drone.identifier, "current_coord")
    enemy_current_coord = current_signal_element.get_signal_data_by_id_key(est_enemy_drone.identifier, "current_coord")

    est_ego_drone.set_init_coord(ego_init_coord)
    est_enemy_drone.set_init_coord(enemy_init_coord)

    est_ego_drone.set_current_coord(ego_current_coord)
    est_enemy_drone.set_current_coord(enemy_current_coord)

    signal_estimator.add_drone(est_ego_drone)
    signal_estimator.add_drone(est_enemy_drone)

    # estimate the entirety of the mission, given the lookahead time
    signal_estimator.fixed_mission_estimate(23)

    # maybe change the time_span
    estimated_signal = signal_estimator.get_signal_estimation()

    # debugger, testing signal estimator
    print ("Estimated Signal: ")
    print(estimated_signal)



    # ideal function invocation
    # G[0, 10](distanceToBoundary > 3)

    stl_formula_1 = STL.Global(0, 23, STL.Primitives.Greater_Than(STL.Helper.Distance_To_Boundary(), 3)) # distance_to_boundary > 3.0
    # 0 - 6 false, 7 - 19 true, 20 - 23 false
    stl_formula_2 = STL.Global(0, 23, STL.Primitives.Greater_Than(STL.Helper.Distance_To_Enemy_Drone(), 3)) # distance_to_enemy > 3.0
    # 0 - 8 true, 9 - 23 false

    # evalute the STL formula with respect to the estimated signal
    print("distance to boundary > 3")
    print(stl_formula_1.eval(estimated_signal, {"internal_map": est_internal_map}))

    print()
    print("distance to enemy drone > 3")
    print(stl_formula_2.eval(estimated_signal))
    

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
    # robustness_stl_formula_1 = STL().evaluate_boundary_robustness(estimated_signal, 21, 21)
    # robustness_stl_formula_2 = STL().evaluate_enemy_robustness(estimated_signal, 21, 21)




    # debug
    # print("STL 1: " + str(robustness_stl_formula_1))
    # print("STL 2: " + str(robustness_stl_formula_2))

    # if robustness_stl_formula_1 < 0 and robustness_stl_formula_2 < 0:
    #     print("Detected conflicts between requirements!")
    # else:
    #     print("No conflict between requirements.")


    ##### /flight estimation testing #####

    # display the initial output to show the path

    # mission_obj.get_internal_map().visualize_output_map()
    # mission_obj.display_heatmap()


    # compute the static robustness score for map cells

    # mission_obj.compute_static_robustness()
    # mission_obj.compute_output()
    # mission_obj.display_heatmap()