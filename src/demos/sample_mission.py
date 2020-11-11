# 2020-11-10 21:58:48

# imported modules
import parser # for parsing the mathematical formulas
import math # for math calculations
import statistics # for statistical analysis (mean, variance, etc)
import numpy as np # numpy for array generations
import sys

sys.path.append("..") # Adds higher directory to python modules path.

# import from my support libaries
from map_utils import Map, Map_Cell, Coord
from drone_utils import EgoDrone, EnemyDrone
from flight import Mission_Planner
from signal_utils import Signal_Estimator, Robustness, Signal_Element
import STL

def main():

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

    # default demo
    ego_drone.set_init_coord(Coord(0, 20))
    enemy_drone.set_init_coord(Coord(5, 5))

    # ego_drone.set_init_coord(Coord(2, 20))
    # enemy_drone.set_init_coord(Coord(1, 6))

    # add enemy drone and ego drone
    mission_obj.add_drone(ego_drone)
    mission_obj.add_drone(enemy_drone)

    # start the feature object, with step number = 23
    mission_obj.run(5)

    # animate the flight path
    mission_obj.get_flight_path().animate()

    ###### /execute flight mission #####

if __name__ == "__main__":
    main()