import algo
from implementations.file_json import FileJSON
from implementations.blackbox_s1s2 import BlackboxS1S2

import glob
import os

if __name__ == "__main__":
    initial_filename = 'initial_big_data.json'
    work_folder = 'files'
    file_interactor = FileJSON(initial_filename, work_folder)
    blackbox = BlackboxS1S2(self_cleanup=True)
    algo.start_algorithm(file_interactor, blackbox)
    print("TOTAL COUNTER: ", blackbox.get_counter())

    # Cleanup (BE CAREFUL, removes ALL in work_folder except initial_filename)
    # files = glob.glob(os.path.join(os.curdir, work_folder, '*'))
    # for f in files:
    #     if os.path.basename(f) != initial_filename:
    #         os.remove(f)
