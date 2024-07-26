# Blackbox algorithm that returns a specific code (0/1 are supported, others - unknown)
class IBlackBox:

    def __init__(self, s1_key="S1", s2_key="S2", self_cleanup=False, blackbox_path=""):
        self.blackbox_path = blackbox_path
        self.s1_key = s1_key
        self.s2_key = s2_key
        self.cleanup = self_cleanup
        self.counter: int = 0

    # checking the blackbox with given file.
    # removes it if self.cleanup is true
    def get_return_code(self, absolute_path_to_file: str) -> int:
        # self.counter += 1
        pass

    def get_counter(self) -> int:
        return self.counter
