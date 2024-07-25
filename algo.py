import os
import json
import random
import sys
import subprocess
import time
import queue

from interfaces.i_file import IFile
from interfaces.i_blackbox import IBlackBox


def get_sublists(data: list, current_split: int = 2):
    sublists = []
    sublist_size = len(data) // current_split
    remainder = len(data) % current_split
    start_idx = 0

    for i in range(current_split):
        sublist_end = start_idx + sublist_size + (1 if i < remainder else 0)
        sublists.append(data[start_idx:sublist_end])
        start_idx = sublist_end

    return sublists
    # if len(data) <= current_split:
    #     return [[el] for el in data]
    # piece_size = (len(data) + 1) // current_split
    # return_lists = []
    # for i in range(current_split):
    #     return_lists.append(data[i * piece_size:i * piece_size + piece_size])
    # return return_lists


def rearrange_sublist_in_beginning(sub_list: list, full_list: list):
    return sub_list + sorted(list(set(full_list) - set(sub_list)))


def fill_up_to_global_blackbox_size(sub_list: list, global_size: int):
    return sub_list + sorted(list(set(list(range(global_size))) - set(sub_list)))


def magic_binary_shuffler(indexes: list, file_interactor: IFile, blackbox: IBlackBox, max_depth=30):
    if len(indexes) == 2:
        print("FOUND S1 and S2: ", indexes)
        return indexes
    current_depth = 0

    print()
    # print("current indexes: ", indexes)

    queue = [indexes]

    previous_result = None
    new_result = None

    while len(queue) != 0 and current_depth < max_depth:
        # Getting the current indexes to test
        current_list_of_indexes_to_test = queue.pop(0)
        # Preparing the other indexes for the blackbox
        # Elements must be prepared for the blackbox, which expect a list of elements with constant size
        #  (same as number of elements in the map_of_data)
        # Putting currently tested elements in the beginning
        S1S2_combined = rearrange_sublist_in_beginning(current_list_of_indexes_to_test, indexes)
        to_be_tested_indexes = fill_up_to_global_blackbox_size(S1S2_combined, file_interactor.get_original_size())

        print("current pop from the queue: ", current_list_of_indexes_to_test)
        print("S1S2_combined: ", S1S2_combined)
        print("indexes that will be tested: ", to_be_tested_indexes)

        # if to_be_tested_indexes[0] in already_tried_first_indexes and len(already_tried_first_indexes) > 1:
        #     sub_lists = get_sublists(current_list_of_indexes_to_test, 4)
        #     queue.extend(sub_lists)
        #     continue

        created_test_file = file_interactor.create_file(to_be_tested_indexes)
        print("Created test file: ", created_test_file)
        if not previous_result:
            new_result = previous_result = blackbox.get_return_code(created_test_file)
        else:
            new_result = blackbox.get_return_code(created_test_file)
        print("new_result previous result: ", new_result, ', ', previous_result)
        if new_result == previous_result:
            # Splitting the list_of_indexes_to_test into 4 pieces
            sub_lists = get_sublists(current_list_of_indexes_to_test, 4)
            queue.extend(sub_lists)
        else:
            previous_result = new_result
            # Empty the queue
            queue = []
            # If result changed with this instance of sub list, it means that it has S2 in it
            S2_narrowed_down = current_list_of_indexes_to_test
            S1_narrowed_down = list(set(S1S2_combined) - set(S2_narrowed_down))
            S1_len = len(S1_narrowed_down)
            print("S1 narrowed down: ", S1_narrowed_down)
            print("S1_len: ", S1_len)
            print("S2 narrowed down: ", S2_narrowed_down)

            BS_depth = 0
            while new_result == previous_result and BS_depth < max_depth:
                BS_depth += 1
                offset = S1_len - S1_len // (2 ** BS_depth)
                print("offset: ", offset)
                new_list_to_test = S1_narrowed_down[:offset] + S2_narrowed_down + S1_narrowed_down[offset:]
                new_list_to_test = fill_up_to_global_blackbox_size(new_list_to_test,
                                                                   file_interactor.get_original_size())
                print("new_list_to_test: ", new_list_to_test)
                new_file = file_interactor.create_file(new_list_to_test)
                new_result = blackbox.get_return_code(new_file)
            if BS_depth >= max_depth:
                print("TOO DEEP (BS FOR S1 DEPTH)!!!!!!!!!!! ABORTING THE EXECUTION!!!!!!!!!!!!!!!!!")
                exit(-1)
            # If this point was reached, it means that the smallest piece that contains S1 was deduced
            # [0, 1, S1, 3, 4, 5, 6, 7, S2, 9] -> [S2, 9] [0, 1, ... 7] -> [0, 1, S1, 3] [S2, 9], [4, 5, 6, 7] ->
            # S1 is in the [0, 1, S1, 3] -> start again with [0, 1, S1, 3, S2, 9]
            pre_last_offset = S1_len - S1_len // (2 ** (BS_depth - 1))
            last = S1_len - S1_len // (2 ** BS_depth)
            print("pre_last_offset: ", pre_last_offset)
            print("last offset: ", last)
            print(
                f"\nABOUT TO CALL MAGIC BINARY SHUFFLER AGAIN WITH : {S1_narrowed_down[pre_last_offset: last] + S2_narrowed_down}\n\n\n\n")
            return magic_binary_shuffler(S1_narrowed_down[pre_last_offset: last] + S2_narrowed_down, file_interactor,
                                         blackbox, max_depth)
    current_depth += 1
    if current_depth >= max_depth:
        print("TOO DEEP (current_depth)!!!!!!!!!!! ABORTING THE EXECUTION!!!!!!!!!!!!!!!!!")
    exit(-1)


def start_algorithm(file_interactor: IFile, blackbox: IBlackBox):
    initial_indexes: list = file_interactor.get_original_indexes()
    return magic_binary_shuffler(initial_indexes, file_interactor, blackbox)
