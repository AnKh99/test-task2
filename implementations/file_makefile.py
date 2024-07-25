import os.path
import re
from os import path

from interfaces.i_file import IFile
import json


# Expects a MAKEFILE
class FileMakefile(IFile):
    def __init__(self, input_filename: str, folder_to_work_in: str):
        super().__init__(input_filename, folder_to_work_in)
        self.load_makefile()

    def load_makefile(self):
        file_path = os.path.abspath(os.path.join(os.curdir, self.folder_to_work_in, self.first_filename))
        with open(file_path, 'r') as file:
            self.original_content = file.read()
        
        # Extract libmlsimplus_la_SOURCES values
        pattern = r'libmlsimplus_la_SOURCES\s*=\s*\\([\s\S]*?)\n\w'
        match = re.search(pattern, self.original_content, re.MULTILINE)
        if match:
            sources_section = match.group(1)
            self.sources = [line.strip() for line in sources_section.split('\\') if line.strip()]
            self.map_of_data = {i: source for i, source in enumerate(self.sources)}
        else:
            raise ValueError("libmlsimplus_la_SOURCES not found in Makefile")

    def create_file(self, indexes: list):
        self.check_indexes_validity(indexes)

        absolute_file_path = self.get_new_file_output_target()
        if path.exists(absolute_file_path):
            raise Exception(f"File path {absolute_file_path} exists")

        # Generate new libmlsimplus_la_SOURCES content based on indexes
        new_sources = [self.map_of_data[i] for i in indexes]
        new_sources_content = 'libmlsimplus_la_SOURCES = \\\n' + ' \\\n'.join(new_sources) + '\n'

        # Replace the original libmlsimplus_la_SOURCES content with the new content
        new_content = re.sub(
            r'libmlsimplus_la_SOURCES\s*=\s*\\[\s\S]*?\n(\w|$)',
            new_sources_content + '\\1',
            self.original_content,
            flags=re.MULTILINE
        )

        os.makedirs(os.path.dirname(absolute_file_path), exist_ok=True)
        with open(absolute_file_path, 'w') as output_f:
            output_f.write(new_content)

        if not path.exists(absolute_file_path):
            raise Exception(f"File creation at {absolute_file_path} failed")

        self.files_created_counter += 1

        return absolute_file_path
