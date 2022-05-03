
import threading 
from copy import deepcopy


from .state import State

import logging
logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-9s) %(message)s',)

class FrameThread(threading.Thread):
    def __init__(self,frames_loc="/Users/jackboynton/Library/Application Support/Dolphin/Dump/Frames/"):
        super(MemoryWatcherThread, self).__init__(group=group, target=target, name=name)
        