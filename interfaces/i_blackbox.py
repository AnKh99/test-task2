import os


# Blackbox algorithm that returns a specific code (0/1 are supported, others - unknown)
class IBlackBox:

    def __init__(self, self_cleanup=False):
        self.cleanup = self_cleanup
        self.counter: int = 0

    # checking the blackbox with given file.
    # removes it if self.cleanup is true
    def get_return_code(self, absolute_path_to_file: str) -> int:
        # self.counter += 1
        pass

    def get_counter(self) -> int:
        return self.counter
