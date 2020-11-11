# path_utils.py
# support the visualization of flight paths

# Wed Oct 21 09:21:40 EDT 2020
# Designed with ❤️ by Simon Chu

from itertools import count
# import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from map_utils import Coord
import numpy as np

ANIMATION_INTERVAL = 400 # default is 400ms


class Path:
    """
    Attributes:
        coord_list: dictionary that stores a list of flight path for different drones
                    indexed by the identifier of the drones
        message_list: list that stores messages broadcasted by ATC (Air Traffic Control)
    """
    # Note that drone map is needed to determine how big the graph is
    def __init__(self, drone_identifier_list, drone_internal_map):
        # stores a list of drone identifiers
        self.drone_identifier_list = drone_identifier_list

        # stores the internal map of the drone
        self.drone_internal_map = drone_internal_map

        # initialize message list
        self.message_list = list()

        # stores the list of coordinate dictionary
        # {"EnemyDrone": [(1, 1), (2, 2)], "EgoDrone": [(1, 2), (2, 2)]}
        #                 ------> tuple of integer
        self.coord_list = dict()

        # initialize the keys
        for drone_identifier in self.drone_identifier_list:
            self.coord_list[drone_identifier] = list()
        
    
    def add_coords(self, drone_identifier, coord):
        self.coord_list[drone_identifier].append(coord)

    def add_coords_by_shared_flight_data(self, shared_flight_data):
        # debug
        # print(str(shared_flight_data))

        # loop through all drones included in the flight path visualizer
        for drone_identifier in self.drone_identifier_list:
            drone_coord = shared_flight_data.get(drone_identifier).get_coord()
            self.coord_list[drone_identifier].append(drone_coord)

        # debug
        # print(self.coord_list)

    def add_message(self, message):
        """append message to self.message_list"""
        self.message_list.append(message)

    def add_message_by_shared_flight_data(self, shared_flight_data):
        """function to extract message from the "ATC" role in the shared_flight_data
        and append it to self.message_list
        """
        self.message_list.append(shared_flight_data.get("ATC").get_message())

    def add_coords_by_response_data(self, response_data):
        # extract "current_map_cell" key's value from the response_data
        for drone_identifier in self.drone_identifier_list:

            # obtain the current map cell from the response data based on the drone identifier
            response_current_map_cell = response_data[drone_identifier]["current_map_cell"]

            # append the current map cell to the list of coordinates
            # stores the list of coordinate dictionary
            # {"EnemyDrone": [(1, 1), (2, 2)], "EgoDrone": [(1, 2), (2, 2)]}
            #                 ------> tuple of integer
            # convert the list of map cells in self.coord_list to numeric values
            # self.coord_list[drone_identifier].append((response_current_map_cell.x(), response_current_map_cell.y()))
            self.coord_list[drone_identifier].append(response_current_map_cell.get_coord())
    
    def add_estimated_signal(self, estimated_signal):
        """set the estimated signal"""
        # if the estimate_signal class variable hasn't been initialized, initialize the variable
        # note that estimated signal is a list of dictionaries
        if not hasattr(self, "estimated_signal"):
            self.estimated_signal = list()

        # append the estimated signal to the self.estimated_signal
        self.estimated_signal.append(estimated_signal)


    def display_coords(self):
        # helper function to display the coordinates collected from the execution cycle
        print(self.coord_list)

    
    def linearize_coord_list(self):
        # function to linearize coord list
        # separate x and y coordinates
        self.coord_list_linearized = dict()
        for drone_identifier in self.drone_identifier_list:
            # initialize the dictionary
            # self.coord_list_linearized = {"EgoDrone": {"x_cor_data": [1, 2, 3], "y_cor_data": [1, 3, 4]}, "EnemyDrone"...}
            self.coord_list_linearized[drone_identifier] = dict()

            x_cor_data = []
            y_cor_data = []

            # separate x and y coordinates data
            for coords in self.coord_list[drone_identifier]:
                x_cor_data.append(coords.x())
                y_cor_data.append(coords.y())
            
            self.coord_list_linearized[drone_identifier]["x_cor_data"] = x_cor_data
            self.coord_list_linearized[drone_identifier]["y_cor_data"] = y_cor_data

    def linearize_estimated_signal(self):
        # estimated_signal_linearized is a list of dictionary
        # note that list is indexed by time
        self.estimated_signal_linearized = list() # dict()

        # loop through different times
        for time_index in range(0, len(self.estimated_signal)):
            # create a new list that holds the dictionary
            estimated_signal_linearized_dict = dict()

            # loop through drone identifiers
            for drone_identifier in self.drone_identifier_list:
                # initialize the dictionary
                # self.coord_list_linearized = {"EgoDrone": {"x_cor_data": [1, 2, 3], "y_cor_data": [1, 3, 4]}, "EnemyDrone"...}
                estimated_signal_linearized_dict[drone_identifier] = dict()

                # initialize the list containing the linearized x and y coordinate data
                x_cor_data = []
                y_cor_data = []

                # loop through the time (LOOKAHEAD time) for each drone identifier
                for time in range(self.estimated_signal[time_index].length()):
                    # print(type(self.estimated_signal))
                    # separate x and y coordinates data
                    # print(type(self.estimated_signal.signal_list[time]))
                    signal_element = self.estimated_signal[time_index].get_signal_element(time)

                    # get the coordinates from the signal_element
                    coords = signal_element.get_signal_data_by_id_key(drone_identifier, "current_coord")

                    # append the x y coordinate to x and y array, respectively
                    x_cor_data.append(coords.x())
                    y_cor_data.append(coords.y())
                    
                estimated_signal_linearized_dict[drone_identifier]["x_cor_data"] = x_cor_data
                estimated_signal_linearized_dict[drone_identifier]["y_cor_data"] = y_cor_data

            # add the dictionary to the list
            self.estimated_signal_linearized.append(estimated_signal_linearized_dict)     

        # return the list of linearized coordinates
        return self.estimated_signal_linearized

        # self.estimated_signal 
    def init_plot(self):
        # function to initialize the plot

        # use the style from fivethirtyeight.com
        plt.style.use('fivethirtyeight')
        
        # initialize graph identifier list as a class variable
        self.graph_identifier_list = list()

        # initialize different labels using different drone identifiers, including estimates
        for drone_identifier in self.drone_identifier_list:
        
            self.graph_identifier_list.append(drone_identifier)

        for drone_identifier in self.drone_identifier_list:
            self.graph_identifier_list.append(drone_identifier + " Estimate")
        
        print(self.graph_identifier_list)
        # intialize 4 lines in the plot (hardcoded)

        for graph_identifier in self.graph_identifier_list[0:2]:
            plt.plot([], [], label=graph_identifier)#,#linestyle="dashed")

        for graph_identifier in self.graph_identifier_list[2:4]:
            plt.plot([], [], label=graph_identifier,linestyle="dashed")

        # case when there is no estimated signal
        # for drone_identifier in self.drone_identifier_list:
            # plt.plot([], [], label=drone_identifier)

    # note that sometimes ego drone will fly first because enemy will not move without response data from the ego drone
    def animate(self):
        # initialize the plot
        self.init_plot()

        # linearized the coordinate data collected
        self.linearize_coord_list()


        # initialize the current step to 0
        self.current_step = 0

        # obtain the x max and y max of the map
        x_max = self.drone_internal_map.get_width()
        y_max = self.drone_internal_map.get_height()
        ax = plt.gca()

        ax.set_xlim(0, x_max)
        ax.set_ylim(y_max, 0)

        # set the coordinate system (top left as origin!)
        # this helper function will be executed everytime the plot refreshes
        def animate_helper(i):
            ax = plt.gca()

            # determine whether to display estimated signal by whether the class has the estimated_signal attribute
            is_display_estimated_signal = hasattr(self, "estimated_signal")

            if is_display_estimated_signal:
                # linearize the estimated signal for display
                self.linearize_estimated_signal()


            drone_count = 0
            drone_max = len(self.drone_identifier_list) # set number of drone path lines in the graph

            # make one line correspond to one drone
            for line in ax.lines:

                # case when signal need to be estimated
                if is_display_estimated_signal:
                    if self.current_step < len(self.estimated_signal_linearized):
                        # print(self.estimated_signal_linearized)

                        print("drone_count (estimate signal): " , drone_count)
                        print("current step : " + str(self.current_step))
                        print("length of estimated signal lineared : " + str(len(self.estimated_signal_linearized)))
                        # specify each of the line data (note that the order matters)
                        if drone_count < drone_max:
                            drone_identifier = self.drone_identifier_list[drone_count]
                            drone_count += 1
                            line.set_data(self.coord_list_linearized[drone_identifier]["x_cor_data"][0:self.current_step], self.coord_list_linearized[drone_identifier]["y_cor_data"][0:self.current_step])

                        elif drone_count >= drone_max and drone_count < drone_max * 2:
                            drone_identifier = self.drone_identifier_list[drone_count % drone_max]
                            line_identifier = drone_identifier + " Estimate"
                            drone_count += 1
                            line.set_data(self.estimated_signal_linearized[self.current_step][drone_identifier]["x_cor_data"], self.estimated_signal_linearized[self.current_step][drone_identifier]["y_cor_data"])

                        else:
                            # when exceeding the number of lines drawn, break the loop
                            break
                    


                
                else:
                    # default mode, no estimated signal
                    # print(self.estimated_signal_linearized)

                    print("drone_count: " , drone_count)
                    # specify each of the line data (note that the order matters)
                    if drone_count < drone_max:
                        drone_identifier = self.drone_identifier_list[drone_count]
                        drone_count += 1
                        line.set_data(self.coord_list_linearized[drone_identifier]["x_cor_data"][0:self.current_step], self.coord_list_linearized[drone_identifier]["y_cor_data"][0:self.current_step])

                    else:
                        # when exceeding the number of lines drawn, break the loop
                        break

            # # plot the estimation flight paths
            # # https://matplotlib.org/3.1.0/gallery/lines_bars_and_markers/linestyles.html
            # drone_count = 0 # reset drone_count variable
            # for line in ax.lines:
            #     if drone_count < drone_max:
            #         drone_identifier = self.drone_identifier_list[drone_count]
            #         line_identifier = drone_identifier + " Estimate"
            #         drone_count += 1
            #         line.set_data(self.estimated_signal_linearized[drone_identifier]["x_cor_data"], self.estimated_signal_linearized[drone_identifier]["y_cor_data"])



            # the visualizer will keep executing even after exceeding the limit
            # make sure to check bound
            if (self.current_step < len(self.message_list)):
                print("step = {0:3}".format(str(self.current_step)) + " message = " + self.message_list[self.current_step], flush=True)


            # increment current_step to get more data
            self.current_step += 1

            # print the step information during the visualization
            # print(self.current_step)
            # print(self.message_list)


        # start the animation
        animation = FuncAnimation(plt.gcf(), animate_helper, interval = ANIMATION_INTERVAL)

        plt.legend()
        plt.tight_layout()

        # make the label style consistent with the heatmap
        plt.tick_params(axis='both', which='major', labelsize=10, labelbottom = False, bottom=False, top = False, labeltop=True, length=0)

        # set the interval of both x and y axis to 1
        plt.xticks(np.arange(0, x_max, 1.0))
        plt.yticks(np.arange(0, y_max, 1.0))
        plt.show()