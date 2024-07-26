import algo
from implementations.file_json import FileJSON
from implementations.file_makefile import FileMakefile
from implementations.blackbox_makefile import BlackboxMakefile
from implementations.blackbox_s1s2 import BlackboxS1S2

import glob
import os
import argparse


def json_mode(initial_filename, work_folder, s1_key, s2_key, cleanup):
    print("JSON mode")
    file_interactor = FileJSON(initial_filename, work_folder)
    blackbox = BlackboxS1S2(s1_key, s2_key, self_cleanup=cleanup)
    algo.start_algorithm(file_interactor, blackbox)
    print("TOTAL COUNTER: ", blackbox.get_counter())

def makefile_mode(initial_filename, work_folder, s1_key, s2_key, cleanup, blackbox_path):
    print("Makefile mode")
    file_interactor = FileMakefile(initial_filename, work_folder)    
    blackbox = BlackboxMakefile(s1_key, s2_key, self_cleanup=cleanup, blackbox_path=blackbox_path)
    algo.start_algorithm(file_interactor, blackbox)
    print("TOTAL COUNTER: ", blackbox.get_counter())

    # Cleanup (BE CAREFUL, removes ALL in work_folder except initial_filename)
    # files = glob.glob(os.path.join(os.curdir, work_folder, '*'))
    # for f in files:
    #     if os.path.basename(f) != initial_filename:
    #         os.remove(f)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run algorithm with specified parameters")
    parser.add_argument('--mode', type=str, required=True, help='Application mode (e.g., json or makefile)')
    parser.add_argument('--initial_filename', type=str, required=True, help='The initial filename (e.g., makefile_test.am, initial_big_data.json')
    parser.add_argument('--work_folder', type=str, required=True, help='The working folder where temporary files are stored')
    parser.add_argument('--s1_key', type=str, required=True, help='The key representing S1 (e.g., S1, S1.cpp) for blackbox')
    parser.add_argument('--s2_key', type=str, required=True, help='The key representing S2 (e.g., S2, S2.cpp) for blackbox')
    parser.add_argument('--blackbox_path', type=str, required=False, help='Path to checker bash file')
    parser.add_argument('--cleanup', action='store_true', required=False, help='If set, will clean up the work folder after processing')

    args = parser.parse_args()

    if args.mode == "json":
        json_mode(args.initial_filename, args.work_folder, args.s1_key, args.s2_key, args.cleanup)
    elif args.mode == "makefile":
        makefile_mode(args.initial_filename, args.work_folder, args.s1_key, args.s2_key, args.cleanup, args.blackbox_path)
    else:
        raise Exception("Wrong application mode")