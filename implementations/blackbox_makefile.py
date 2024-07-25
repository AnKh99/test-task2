from interfaces.i_blackbox import IBlackBox
import json
import os


# BlackboxMakefile works with MAKEFILE files and expects S1 and S2 to be in the file given to it
class BlackboxMakefile(IBlackBox):
    def get_return_code(self, absolute_path_to_file: str) -> int:
        self.counter += 1

        first_key = "S1.cpp"
        second_key = "S2.cpp"
        found_first_key = False

        return_flag = False
        with open(absolute_path_to_file, 'r') as input_file:
            for line in input_file:
                if first_key in line:
                    found_first_key = True
                elif second_key in line and found_first_key:
                    return_flag = True
                    break

        if self.cleanup:
            os.remove(absolute_path_to_file)
        return return_flag
