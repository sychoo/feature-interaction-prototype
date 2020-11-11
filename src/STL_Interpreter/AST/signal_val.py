
from sys import stdout, path
path.append("..") # Adds higher directory to python modules path.

from tools import String_Builder
import exceptions
from val import Val
import json

# sample simplified signal
# {
#    "1": {
#     "content": {
#    },

#    "2": {
#      "content": {
#    }
# }

# in the case of enemy drone and ego drone
# "content" : {'Ego': {'current_coord': (1, 20)}, 'Enemy': {'current_coord': (0, 5)}

class Signal_Val(Val):
    def __init__(self, value, signal_dict=None, value_type="SIGNAL"):
        """user can initialize the signal_val object either by the JSON parsed value or by the signal dictionary (parsed JSON file to Python dictionary)"""
        self.value_type = value_type

        if value != None:
            # in the future, parse the value directory to JSON object in Python
            self.value = self.extract_json_from_signal(value)
        else:
            self.value = None


        # the internal signal representation
        if signal_dict != None:
            # case when user passed signal_dictionary to the parameter
            self.signal_dict = signal_dict
        else:
            # case when user didn't pass signal dictionary 
            self.signal_dict = self.parse_json(self.value)
            
        self.verify_signal_dict(self.signal_dict)

        # print(self.signal_dict)
        # print(self.get_time_bound(self.signal_dict))

    @staticmethod
    def get_new_signal_from_dict(signal_dict):
        """wrapper for constructor"""
        return Signal_Val(None, signal_dict, "SIGNAL")
        

    def __len__(self):
        return len(self.signal_dict)

    def get_signal_dict(self):
        # return the dictionary type of the signal
        return self.signal_dict

    @staticmethod
    def extract_json_from_signal(value):
        # get rid of the dollar "$" sign
        return value[1:-1]

    @staticmethod
    def parse_json(value):
        # parse the json-represented signal
        # the result is represented using a python dictionary
        return json.loads(value)

    def to_str(self):
        # display the time bound, the length and the internal representation of the signal
        # when printing it
        signal_time_bound = self.get_time_bound(self.signal_dict)
        sb = String_Builder()
        sb.append("SIGNAL")
        sb.append("[")
        sb.append(str(signal_time_bound[0]))
        sb.append(", ")
        sb.append(str(signal_time_bound[1]))
        sb.append("](")
        sb.append(str(len(self)))
        sb.append(") :: ")
        sb.append(str(self.signal_dict))

        return str(sb)

    def __str__(self):
        # abbreviated version of the Signal for the parser display
        signal_time_bound = self.get_time_bound(self.signal_dict)
        sb = String_Builder()
        sb.append("SIGNAL")
        sb.append("[")
        sb.append(str(signal_time_bound[0]))
        sb.append(", ")
        sb.append(str(signal_time_bound[1]))
        sb.append("](")
        sb.append(str(len(self)))
        sb.append(")")

        return str(sb)

    def verify_signal_dict(self, signal_dict):
        # make sure steps are continuous
        # (1) 1, 2, 3, 4 ... (for discrete signals)
        # (2) make sure signal is consistent across all times (have the same keys for the dict)
        time_begin, time_end, time_int_list = Signal_Val.get_time_bound(signal_dict)

        # make sure the duration of the time matches the length of the signal dictionary
        if time_end - time_begin == len(time_int_list) - 1 and \
            time_int_list == [x for x in range(time_begin, time_end + 1)]:
            pass
        else:
            # raise exceptions if there are time incontinuities
            raise exceptions.Invalid_Signal_Error("Signal \"" + str(self) + "\" is invalid because of time incontinuity")

    @staticmethod
    def get_time_bound(signal_dict):
        time_str_list = signal_dict.keys()
        time_int_list = [int(time_str) for time_str in time_str_list]
        time_int_list.sort()
        return (time_int_list[0], time_int_list[-1], time_int_list)

    def get_begin_time(self):
        return Signal_Val.get_time_bound(self.signal_dict)[0]
    
    def get_end_time(self):
        return Signal_Val.get_time_bound(self.signal_dict)[1]

    def get_duration(self):
        time_begin, time_end, time_int_list = Signal_Val.get_time_bound(self.signal_dict)
        return time_end - time_begin


    def slice_signal_by_time_interval(self, time_begin, time_end):
        """slice the signal based on the time interval (inclusive)
        returns
            Signal_Val: new signal value created from the signal dictionary sliced
        """
        # create a new dictionary
        new_dict = dict()

        for i in range(time_begin, time_end + 1):
            time_index = str(i)

            # append the usable signal
            new_dict.update({time_index : self.signal_dict[time_index]})

        return Signal_Val.get_new_signal_from_dict(new_dict)

    def slice_signal_by_time(self, time):
        """literally Slice the signal by time. return the new signal between sliced time interval

        returns
            Signal_Val: new signal value created from the signal dictionary sliced
        """
        # create a new dictionary
        new_dict = dict()

        time_index = str(time)

        # append the usable signal
        new_dict.update({time_index : self.signal_dict[time_index]})
        return Signal_Val.get_new_signal_from_dict(new_dict)
        
    def __str__(self):
        return str(self.signal_dict)