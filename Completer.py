
import re
import readline

RE_SPACE = re.compile('.*\s+$', re.M)

class Completer:

    def __init__(self):
        self.clear_complete_list()

    def set_complete_list(self, new_list):
        self.complete_list = new_list

    def clear_complete_list(self):
        self.complete_list = ['']
        
    def complete(self, text, state):
        for cmd in self.complete_list:
                if cmd.startswith(text):
                        if not state:
                                return cmd
                        else:
                                state -= 1
