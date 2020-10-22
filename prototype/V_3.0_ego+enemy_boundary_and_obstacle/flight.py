# flight.py
# file to control the flight (runtime) modules
# visualization of the software

# Tue Oct  6 23:00:38 EDT 2020
# Designed with ❤️ by Simon Chu

import math
import numpy as np

from path_utils import Path
from map_utils import Map_Cell, Map

# import seaborn visualization library
import seaborn as sns
sns.set_theme()
import matplotlib.pyplot as plt

# main object for Feature Interaction problem
class Mission_Planner:
    def __init__(self):
        self.drones = []

    def run(self, steps):
        # make sure there are drones available
        if not hasattr(self, "drones"):
            raise RuntimeError("drone variable has not been initialized.")
        if len(self.drones) <= 0:
            raise RuntimeError("drone variable is empty. Please add drones to the mission planner.")
        
        # intialize the flight path variable to support real-time flight path visualization
        # support multiple drone
        drone_identifier_list = []

        for drone in self.drones:
            drone_identifier_list.append(drone.get_identifier())
            
        # pass the drone identifier list and the internal map associated with drone[0]
        # assume all drones has the same associated internal map
        # the drone internal map is for getting the width and height of the map to plot the dynamic chart
        self.flight_path = Path(drone_identifier_list, self.drones[0].get_internal_map())

        # when step is 0, all drones are at the initial location
        for drone in self.drones:
            self.flight_path.add_coords_x_y(drone.get_identifier(), drone.get_x_cor(), drone.get_y_cor())

        total_steps = steps
        steps = 1

        while steps <= total_steps:
            # intialize response_data to a dictionary
            # re-initialize everytime the loop runs
            response_data = dict()

            ##### execution time #####
            for drone in self.drones:
                # execute the next step of the drone movement
                drone.next_step()

                # emit response data after each execution
                # note that it is crucial to make identifiers unique to appropriately receive the response data
                # response_data = {"Ego": ... "Enemy": ...}
                response_data[drone.get_identifier()] = drone.emit_response_data()
            ##### /execution time #####
             


            ##### data processing #####
            # write the step data to the response_data
            response_data["step"] = steps

            # decrement the step
            steps += 1

             # write the robustness score to the map
            self.write_robustness_score_to_map(response_data)

            # record the path, and update it in real time
            self.flight_path.add_coords(response_data)
            ##### /data processing #####



            ##### post-execution time #####
            # broadcast the response data back to the drones
            for drone in self.drones:
                drone.receive_response_data(response_data)
            ##### /post-execution time #####
        # self.flight_path.display_coords()

    def get_flight_path(self):
        if hasattr(self, "flight_path"):
            return self.flight_path
        else:
            raise RuntimeError("flight_path variable has not been initialized.")
        
    def write_robustness_score_to_map(self, response_data):
        # write the robustness score back to the map
        ego_map_cell = response_data["Ego"]["current_map_cell"]
        enemy_map_cell = response_data["Enemy"]["current_map_cell"]
        
        self.compute_dynamic_robustness(ego_map_cell, enemy_map_cell)

    def add_drone(self, new_drone):
        # add new drones to the MissionPlanner
        self.drones.append(new_drone)

    # round the float value to the nearest integer value
    def round(self, float_value):
        return int(float_value + 0.5)

    def create_internal_map(self, width, height):
        self.internal_map = Map(width, height)

    def get_internal_map(self):
        if hasattr(self, "internal_map"):
            return self.internal_map
        else:
            raise RuntimeError("map variable has not been initialized.")



    # compute the static robustness of the map based on obstacles and boundaries
    # right now boundaries only
    # compute it for all cells
    def compute_static_robustness(self):
        # set the minimum safety distance to the boundary
        min_safety_distance_boundary = 3.0

        # parameter for robustness score penalization
        alpha = 32

        # compute min and max robustness for scaling
        # maybe adjust the min/max robustness score to the actual min/max robustness score in the future
        # robustness_min = -1 * min_safety_distance_boundary
        # robustness_max = max(self.internal_map.get_width(), self.internal_map.get_height()) / 2 - 1

        # set the boundary of the map
        top_boundary_y = 0
        left_boundary_x = 0
        right_boundary_x = self.internal_map.get_width() - 1
        bottom_boundary_y = self.internal_map.get_height() - 1

        # store the raw robustness values for analyzing min and max robustness
        raw_robustness_value_list = []

        # first robustness loop. Calculate the raw robustness score
        for map_cell in self.get_internal_map().get_flattened_internal_map():
            x_cor = map_cell.get_x_cor()
            y_cor = map_cell.get_y_cor()

            distance_to_top = y_cor - top_boundary_y
            distance_to_bottom = bottom_boundary_y - y_cor
            distance_to_left = x_cor - left_boundary_x
            distance_to_right = right_boundary_x - x_cor

            min_distance_to_boundary = min(distance_to_top, distance_to_bottom, distance_to_left, distance_to_right)

            raw_robustness_value = min_distance_to_boundary - min_safety_distance_boundary

            raw_robustness_value_list.append(raw_robustness_value)

            # store the raw robustness value to the map cell for future analysis
            map_cell.set_attribute("static_robustness_score_raw", raw_robustness_value)



        # compute the min and max robustness scores
        robustness_min = min(raw_robustness_value_list)
        robustness_max = max(raw_robustness_value_list)



        # second loop, scale and penalize robustness scores
        for map_cell in self.get_internal_map().get_flattened_internal_map():
            raw_robustness_value = map_cell.get_attribute("static_robustness_score_raw")

            # scale the robustness value to a scale of -1 to 1 (inclusive)
            scaled_robustness_value = 0

            if raw_robustness_value < 0:
                scaled_robustness_value = (raw_robustness_value - robustness_min) / (-1 * robustness_min) - 1
            else:
                scaled_robustness_value = raw_robustness_value / robustness_max

            # penalize negative robustness scores
            penalized_robustness_value = 0

            if raw_robustness_value < 0:
                penalized_robustness_value = raw_robustness_value - (alpha**(-raw_robustness_value - 1)/(alpha - 1))
            else:
                penalized_robustness_value = raw_robustness_value
            
            map_cell.set_attribute("static_robustness_score_scaled", scaled_robustness_value)
            map_cell.set_attribute("static_robustness_score_penalized", penalized_robustness_value)


    # compute the dynamic robustness based on the location of the enemy drone
    # compute it for all cells
    def compute_dynamic_robustness(self, ego_map_cell, enemy_map_cell):
        # alpha = 32

        min_safety_distance_enemy_drone = 3.0

        x_cor_enemy = enemy_map_cell.x()
        y_cor_enemy = enemy_map_cell.y()

        x_cor_ego = ego_map_cell.x()
        y_cor_ego = ego_map_cell.y()
        # robustness_value = 0

        # robustness_min = -1 * min_safety_distance_enemy_drone
        # robustness_max = max(self.internal_map.get_width(), self.internal_map.get_height()) / 2 - 1

        # store the raw robustness values
        raw_robustness_value_list = []

        # for map_cell in self.get_internal_map().get_flattened_internal_map():
        # x_cor = map_cell.get_x_cor()
        # y_cor = map_cell.get_y_cor()

        distance_to_enemy_drone = math.sqrt((x_cor_ego - x_cor_enemy)**2 + (y_cor_ego - y_cor_enemy)**2)
        raw_robustness_value = distance_to_enemy_drone - min_safety_distance_enemy_drone

        # # by default set to empty list []
        # # original_dynamic_robustness_score_raw = []
        # if (map_cell.has_attribute("dynamic_robustness_score_raw")):
            # original_dynamic_robustness_score_raw = map_cell.get_attribute("dynamic_robustness_score_raw")

        # store the list of raw robustness scores in the map cell
        # original_dynamic_robustness_score_raw.append(raw_robustness_value)
        ego_map_cell.set_attribute("dynamic_robustness_score_raw", raw_robustness_value)

        # append the robustness value to the list
        # raw_robustness_value_list.append(raw_robustness_value)



        # compute the max and min robustness value
        # robustness_max = max(raw_robustness_value_list)
        # robustness_min = min(raw_robustness_value_list)


        # Scale and Penalization
        # for map_cell in self.get_internal_map().get_flattened_internal_map():
        #     # obtain the raw robustness value from the map cell
        #     raw_robustness_value = map_cell.get_attribute("dynamic_robustness_score_raw")[-1]

        #     original_dynamic_robustness_score_scaled = []
        #     if (map_cell.has_attribute("dynamic_robustness_score_scaled")):
        #         original_dynamic_robustness_score_scaled = map_cell.get_attribute("dynamic_robustness_score_scaled")
            
        #     original_dynamic_robustness_score_penalized = []
        #     if (map_cell.has_attribute("dynamic_robustness_score_penalized")):
        #         original_dynamic_robustness_score_penalized = map_cell.get_attribute("dynamic_robustness_score_penalized")

        #     # scale the robustness value
        #     if raw_robustness_value < 0:
        #         scaled_robustness_value = (raw_robustness_value - robustness_min) / (-1 * robustness_min) - 1
        #     else:
        #         scaled_robustness_value = raw_robustness_value / robustness_max


        #     # penalize negative robustness scores
        #     penalized_robustness_value = 0

        #     if raw_robustness_value < 0:
        #         penalized_robustness_value = raw_robustness_value - (alpha**(-raw_robustness_value - 1)/(alpha - 1))
        #     else:
        #         penalized_robustness_value = raw_robustness_value

        #     # append the computed values to the corresponding cells
        #     original_dynamic_robustness_score_scaled.append(scaled_robustness_value)
        #     original_dynamic_robustness_score_penalized.append(penalized_robustness_value)

        #     map_cell.set_attribute("dynamic_robustness_score_scaled", original_dynamic_robustness_score_scaled)
        #     map_cell.set_attribute("dynamic_robustness_score_penalized", original_dynamic_robustness_score_penalized)




    # compute the dynamic robustness based on the location of the enemy drone
    # compute it for all cells
    def compute_dynamic_robustness_comprehensive(self, enemy_map_cell):
        alpha = 32

        min_safety_distance_enemy_drone = 3.0

        x_cor_enemy = enemy_map_cell.get_x_cor()
        y_cor_enemy = enemy_map_cell.get_y_cor()

        # robustness_value = 0

        # robustness_min = -1 * min_safety_distance_enemy_drone
        # robustness_max = max(self.internal_map.get_width(), self.internal_map.get_height()) / 2 - 1

        # store the raw robustness values
        raw_robustness_value_list = []

        for map_cell in self.get_internal_map().get_flattened_internal_map():
            x_cor = map_cell.get_x_cor()
            y_cor = map_cell.get_y_cor()

            distance_to_enemy_drone = math.sqrt((x_cor - x_cor_enemy)**2 + (y_cor - y_cor_enemy)**2)
            raw_robustness_value = distance_to_enemy_drone - min_safety_distance_enemy_drone

            # by default set to empty list []
            original_dynamic_robustness_score_raw = []
            if (map_cell.has_attribute("dynamic_robustness_score_raw")):
                original_dynamic_robustness_score_raw = map_cell.get_attribute("dynamic_robustness_score_raw")

            # store the list of raw robustness scores in the map cell
            original_dynamic_robustness_score_raw.append(raw_robustness_value)
            map_cell.set_attribute("dynamic_robustness_score_raw", original_dynamic_robustness_score_raw)

            # append the robustness value to the list
            raw_robustness_value_list.append(raw_robustness_value)



        # compute the max and min robustness value
        robustness_max = max(raw_robustness_value_list)
        robustness_min = min(raw_robustness_value_list)



        for map_cell in self.get_internal_map().get_flattened_internal_map():
            # obtain the raw robustness value from the map cell
            raw_robustness_value = map_cell.get_attribute("dynamic_robustness_score_raw")[-1]

            original_dynamic_robustness_score_scaled = []
            if (map_cell.has_attribute("dynamic_robustness_score_scaled")):
                original_dynamic_robustness_score_scaled = map_cell.get_attribute("dynamic_robustness_score_scaled")
            
            original_dynamic_robustness_score_penalized = []
            if (map_cell.has_attribute("dynamic_robustness_score_penalized")):
                original_dynamic_robustness_score_penalized = map_cell.get_attribute("dynamic_robustness_score_penalized")

            # scale the robustness value
            if raw_robustness_value < 0:
                scaled_robustness_value = (raw_robustness_value - robustness_min) / (-1 * robustness_min) - 1
            else:
                scaled_robustness_value = raw_robustness_value / robustness_max


            # penalize negative robustness scores
            penalized_robustness_value = 0

            if raw_robustness_value < 0:
                penalized_robustness_value = raw_robustness_value - (alpha**(-raw_robustness_value - 1)/(alpha - 1))
            else:
                penalized_robustness_value = raw_robustness_value

            # append the computed values to the corresponding cells
            original_dynamic_robustness_score_scaled.append(scaled_robustness_value)
            original_dynamic_robustness_score_penalized.append(penalized_robustness_value)

            map_cell.set_attribute("dynamic_robustness_score_scaled", original_dynamic_robustness_score_scaled)
            map_cell.set_attribute("dynamic_robustness_score_penalized", original_dynamic_robustness_score_penalized)

    # control the output (data) on the heatmap
    def compute_output(self):

        # # use the static robustness score
        # for map_cell in self.get_internal_map().get_flattened_internal_map():
        #     map_cell.set_output(map_cell.get_attribute("static_robustness_score_scaled"))


        # use the dynamic robustness score
        for map_cell in self.get_internal_map().get_flattened_internal_map():
            if map_cell.has_attribute("dynamic_robustness_score_raw"):
                map_cell.set_output(map_cell.get_attribute("dynamic_robustness_score_raw"))
            else:
                map_cell.set_output(0)

        # fragmented heat map (a particular state in the process)
        # use the static robustness score
        # for map_cell in self.get_internal_map().get_flattened_internal_map():
            # map_cell.set_output(map_cell.get_attribute("dynamic_robustness_score_scaled")[23] * 0.5 + map_cell.get_attribute("static_robustness_score_scaled") * 0.5)

        # min robustness (without boundary)
        # for map_cell in self.get_internal_map().get_flattened_internal_map():
            # scaled
            # map_cell.set_output(min(map_cell.get_attribute("dynamic_robustness_score_scaled")))

            # penalized
            # map_cell.set_output(min(map_cell.get_attribute("dynamic_robustness_score_penalized")))

        # min robustness (with boundary)
        # for map_cell in self.get_internal_map().get_flattened_internal_map():
            # scaled
            # map_cell.set_output(min(map_cell.get_attribute("dynamic_robustness_score_scaled")) * 0.5 + map_cell.get_attribute("static_robustness_score_scaled") * 0.5)

            # penalized
            # map_cell.set_output(min(map_cell.get_attribute("dynamic_robustness_score_penalized")) * 0.5 + map_cell.get_attribute("static_robustness_score_penalized") * 0.5)

        # max robustness (without boundary)
        # for map_cell in self.get_internal_map().get_flattened_internal_map():
            # scaled
            # map_cell.set_output(max(map_cell.get_attribute("dynamic_robustness_score_scaled")))

            # penalized
            # map_cell.set_output(max(map_cell.get_attribute("dynamic_robustness_score_penalized")))
        
        # max robustness (with boundary)
        # for map_cell in self.get_internal_map().get_flattened_internal_map():
            # scaled
            # map_cell.set_output(max(map_cell.get_attribute("dynamic_robustness_score_scaled")) * 0.5 + map_cell.get_attribute("static_robustness_score_scaled") * 0.5)

            # penalized
            # map_cell.set_output(max(map_cell.get_attribute("dynamic_robustness_score_penalized")) * 0.5 + map_cell.get_attribute("static_robustness_score_penalized") * 0.5)

        # average (without boundary)
        # for map_cell in self.get_internal_map().get_flattened_internal_map():
            # scaled
            # map_cell.set_output(statistics.mean(map_cell.get_attribute("dynamic_robustness_score_scaled")))
            # map_cell.set_output(statistics.mean(map_cell.get_attribute("dynamic_robustness_score_penalized")))
        
        # average (with boundary)
        # for map_cell in self.get_internal_map().get_flattened_internal_map():
            # map_cell.set_output(statistics.mean(map_cell.get_attribute("dynamic_robustness_score_penalized")) * 0.5 + map_cell.get_attribute("static_robustness_score_penalized") * 0.5)

    # display the heatmap using seaborn library
    # use function used in previous program

    # How to draw blank heatmaps?
    # https://seaborn.pydata.org/generated/seaborn.heatmap.html
    def display_heatmap(self):
        data = self.get_internal_map().get_output_map()

        # use zeros like and ones like to display the data
        # mask = np.ones_like(data)
        # mask[np.triu_indices_from(mask)] = True
        # mask[10][1] = False # Do not display 10, 1

        ax = sns.heatmap(data, cmap="Spectral")
        # ax = sns.heatmap(data, mask=mask, cmap="Spectral")
        # ax = sns.heatmap(data, cmap="coolwarm")

        # configure the heatmap interface
        plt.tick_params(axis='both', which='major', labelsize=10, labelbottom = False, bottom=False, top = False, labeltop=True, length=0)
        plt.show()

    