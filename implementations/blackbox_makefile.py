from interfaces.i_blackbox import IBlackBox
import os
import subprocess


# BlackboxMakefile works with MAKEFILE files and expects S1 and S2 to be in the file given to it
class BlackboxMakefile(IBlackBox):
    def get_return_code(self, absolute_path_to_file: str) -> int:
        self.counter += 1

        result = subprocess.run(['bash', self.blackbox_path, absolute_path_to_file, self.s1_key, self.s2_key],
                                capture_output=True, text=True)

        if self.cleanup:
            os.remove(absolute_path_to_file)

        return result.returncode == 0     
        
