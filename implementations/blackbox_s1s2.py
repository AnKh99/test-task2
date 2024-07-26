from interfaces.i_blackbox import IBlackBox
import json
import os


# BlackboxS1S2 works with JSON files and expects S1 and S2 to be in the JSON file given to it
class BlackboxS1S2(IBlackBox):
    def get_return_code(self, absolute_path_to_file: str) -> int:

        self.counter += 1

        found_first_key = False

        return_flag = False
        with open(absolute_path_to_file, 'r') as input_file:
            for el in json.load(input_file):
                if el == self.s1_key:
                    found_first_key = True
                elif el == self.s2_key and found_first_key:
                    return_flag = True

        if self.cleanup:
            os.remove(absolute_path_to_file)
        return return_flag
