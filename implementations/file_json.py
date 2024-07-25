import os.path
from os import path

from interfaces.i_file import IFile
import json


# Expects a JSON with a list in it
# e.g. ["A", "B", "C", ..., "Z"]
class FileJSON(IFile):
    def __init__(self, input_filename: str, folder_to_work_in: str):
        super().__init__(input_filename, folder_to_work_in)
        with open(os.path.join(folder_to_work_in, input_filename), 'r') as input_f:
            list_of_elements = list(json.load(input_f))
            for i, el in enumerate(list_of_elements):
                self.map_of_data[i] = el
        # DEBUG
        # print("Mapped data: ", self.map_of_data)

    def create_file(self, indexes: list):
        self.check_indexes_validity(indexes)

        absolute_file_path = self.get_new_file_output_target()
        if path.exists(absolute_file_path):
            raise Exception(f"File path {absolute_file_path} exists")

        output_data = [self.map_of_data[i] for i in indexes]
        os.makedirs(os.path.dirname(absolute_file_path), exist_ok=True)
        with open(absolute_file_path, 'w') as output_f:
            json.dump(output_data, output_f)

        if not path.exists(absolute_file_path):
            raise Exception(f"File creation at {absolute_file_path} failed")

        self.files_created_counter += 1

        return absolute_file_path
