
import threading 
from copy import deepcopy

from .memory_watcher import MemoryWatcher
from .state_manager import StateManager
from .state import State

import logging
logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-9s) %(message)s',)

class MemoryWatcherThread(threading.Thread):
    """Adds MemoryWatcher changes to state asynchronously to allow for getting most up to date state at any given time.
    """

    def __init__(self, mem_path = "/Users/jackboynton/Library/Application Support/Dolphin/MemoryWatcher/MemoryWatcher", group=None, target=None, name=None,
                 args=(), kwargs=None):
        super(MemoryWatcherThread, self).__init__(group=group, target=target, name=name)
        self.state = State() # most recently updated state object
        self.previous_states = []
        self.state_manager = StateManager(self.state)
        self.memory_watcher = MemoryWatcher(mem_path)
        self.memory_watcher = self.memory_watcher.__enter__() # replaced with context
        logging.debug(f'init memory_watcher and state_manager inside MemoryWatcherThread')

    def run(self):
        logging.debug(f'previous_states: {str(len(self.previous_states))}')
        while True:
            new_state = next(self.memory_watcher) # observe change
            if new_state is not None and len(new_state):
                self.previous_states.append(deepcopy(self.state)) # add previous state to list before updating self.state
                if isinstance(new_state[0], tuple) or isinstance(new_state, list):
                    for r in new_state:
                        try:
                            self.state_manager.handle(r[0], r[1])
                        except Exception as e:
                            print(e) # loading sometimes takes longer and passes non-correct values at first...
                else: 
                    self.state_manager.handle(new_state) # handle single state change and update self.state
