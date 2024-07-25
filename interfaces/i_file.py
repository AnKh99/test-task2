import os
from time import gmtime, strftime


class IFile:
    # opens the given filename, fills up the map_of_data with index->line values.
    # indexes must be counted from 0.
    def __init__(self, input_filename: str, folder_to_work_in: str = 'files'):
        self.files_created_counter: int = 0
        self.first_filename = input_filename
        self.folder_to_work_in = folder_to_work_in
        # map of index -> line in the original file.
        # must be filled during object creation.
        self.map_of_data: dict[int, str] = {}

    # creates a file based on the given indexes;
    #  they are mapped based on the map_of_data filled in creation time.
    # should call check_indexes_validity!
    # 1) size of indexes should be the same as the original file size
    # 2) indexes should be unique
    # you can call get_new_file_output_target to get the target output file easily.
    # returns an absolute path of the created file
    def create_file(self, indexes: list) -> str:
        # self.files_created_counter += 1
        pass

    def check_indexes_validity(self, indexes: list):
        if len(indexes) != self.get_original_size():
            raise Exception("Incorrect sizes!!!!")
        if len(indexes) != len(set(indexes)):
            raise Exception("Incorrect indexes, duplicates found!")

    # creates a unique name for the file and returns an absolute path to it.
    def get_new_file_output_target(self):
        return os.path.abspath(
            os.path.join(os.curdir, self.folder_to_work_in,
                         self.first_filename.split('.')[0] + '___' + str(self.files_created_counter)
                         + '_' + strftime("%H_%M_%S", gmtime()) + '.' + self.first_filename.split('.')[1]))

    # returns the original size of the IFile instance
    def get_original_size(self):
        return len(self.map_of_data)

    def get_original_indexes(self):
        return list(range(self.get_original_size()))
