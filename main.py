import algo
from implementations.file_makefile import FileMakefile
from implementations.blackbox_makefile import BlackboxMakefile

import glob
import os

if __name__ == "__main__":
    initial_filename = 'makefile_test.am'
    work_folder = 'algorithm\\files'
    file_interactor = FileMakefile(initial_filename, work_folder)    
    blackbox = BlackboxMakefile(self_cleanup=False)
    algo.start_algorithm(file_interactor, blackbox)
    print("TOTAL COUNTER: ", blackbox.get_counter())

    # Cleanup (BE CAREFUL, removes ALL in work_folder except initial_filename)
    # files = glob.glob(os.path.join(os.curdir, work_folder, '*'))
    # for f in files:
    #     if os.path.basename(f) != initial_filename:
    #         os.remove(f)
