# import os
# import json
# import sys
#
#
# # blackbox algorithm
# def blackbox_algorithm_found_sequence(data: json) -> bool:
#
#     # try compile
#     # if fails -> return False
#     # if ok -> try test
#     # if test works -> return Ttrue
#     # if test does not work -> return False
#
#     found_M0 = False
#     found_M1 = False
#     found_M2 = False
#     found_M3 = False
#     found_M4 = False
#     for i, el in enumerate(data):
#         if el == 'M0':
#             found_M0 = i
#         if el == 'M1':
#             found_M1 = i
#         if el == 'M2':
#             found_M2 = i
#         if el == 'M3':
#             found_M3 = i
#         if el == 'M4':
#             found_M4 = i
#
#     if not found_M0 < found_M1 < found_M2 < found_M3 < found_M4:
#     # if found_M2 > found_M3:
#         return None
# 
#
#     first_key = "S1"
#     second_key = "S2"
#     found_first_key = False
#
#     for el in data:
#         if el == first_key:
#             found_first_key = True
#         elif el == second_key and found_first_key:
#             return True
#
#     return False
#
#
# if len(sys.argv) != 2:
#     raise Exception("Incorrect argv")
#
# with open(sys.argv[1]) as f:
#     json_data = json.load(f)
#     # for the initial_dataset.json is "all" should be before "things" for the dataset to be OK
#     sequence_found = blackbox_algorithm_found_sequence(json_data)
#     print("Found sequence: ", sequence_found)
#     if sequence_found == None:
#         print("ABOUT TO RETURN 0 : ")
#         sys.exit(0)
#     sys.exit(1 if sequence_found else 2)
