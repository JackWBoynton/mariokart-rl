import os.path
import time

import memory_watcher
import menu_manager
import pad as Pad
import state as State
import state_manager
import stats as Stats

import pickle
import queue


pts = []
def find_dolphin_dir():
    """Attempts to find the dolphin user directory. None on failure."""
    return "/Users/jackboynton/Library/Application Support/Dolphin"

def write_locations(dolphin_dir, locations):
    """Writes out the locations list to the appropriate place under dolphin_dir."""
    path = dolphin_dir + '/MemoryWatcher/Locations.txt'
    with open(path, 'w') as f:
        f.write('\n'.join(locations))
        print(locations)
        dolphin_dir = find_dolphin_dir()
        if dolphin_dir is None:
            print('Could not detect dolphin directory.')
            return

def reset(pad):
    print("reset..")
    pad.reset() # release all
    time.sleep(1)

    pad.press_button(Pad.Button.START)
    pad.release_button(Pad.Button.START)
    pad.press_button(Pad.Button.D_DOWN)
    pad.release_button(Pad.Button.D_DOWN)
    pad.press_button(Pad.Button.A)
    pad.release_button(Pad.Button.A)

    time.sleep(10)

def tap(pad, button):
    pad.press_button(button)
    time.sleep(0.04)
    pad.release_button(button)

import threading
import subprocess

class Player(threading.Thread):

    def start_dolphin(self):
        self.dolphin = subprocess.Popen(["/Applications/Dolphin.app/Contents/MacOS/Dolphin", "-e", "/Users/jackboynton/mk.iso", "-s", "/Applications/Dolphin.app/Contents/MacOS/xasdf.sav", ">", "/dev/null"], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

    def __init__(self,):
        self.states = queue.LifoQueue()

    def parse_mw_update(self, state, res, sm):
        if res is not None and res != []:
            if isinstance(res[0], tuple) or isinstance(res, list):
                for r in res:
                    try:
                        sm.handle(r[0], r[1])
                    except Exception as e:
                        print(e) # loading sometimes takes longer and passes non-correct values at first...
            else:
                sm.handle(res)
        return


    def run(self):
        
        self.main()

    def starting_menu_logic(self, state, pad):
        if state.menu_identifier in [State.ScreenID.Emptyitseems, State.ScreenID.LOADING]:
            return
        elif state.menu_identifier == State.ScreenID.TitleScreen:
            tap(pad, Pad.Button.A)
        elif state.menu_identifier == State.ScreenID.SinglePlayerMenu:
            print("single player, pressing A")
            tap(pad, Pad.Button.A)
        elif state.menu_identifier == State.ScreenID.CharacterSelect:
            tap(pad, Pad.Button.A)
        elif state.menu_identifier == State.ScreenID.VehicleSelect:
            tap(pad, Pad.Button.A)
        elif state.menu_identifier == State.ScreenID.DriftSelect:
            tap(pad, Pad.Button.A)
        elif state.menu_identifier == State.ScreenID.CupSelect:
            tap(pad, Pad.Button.A)
        elif state.menu_identifier == State.ScreenID.CourseSelectsubscreen:
            tap(pad, Pad.Button.A)
        elif state.menu_identifier in [State.ScreenID.SelectGhosta, State.ScreenID.SelectGhostb]:
            tap(pad, Pad.Button.D_DOWN)
            tap(pad, Pad.Button.D_DOWN)
            tap(pad, Pad.Button.A)
            time.sleep(0.5)
            tap(pad, Pad.Button.A)
        return


    def _run(self, state, sm, mw, pad, stats):
        time.sleep(1)
        while True:
            res = next(mw)
            self.parse_mw_update(state, res, sm) # update state
            # if state.menu_identifier:
            #     # print(state.menu_identifier)
            #     self.starting_menu_logic(state, pad)
            
                    
            # self.states.put((state.players[0].xpos, state.players[0].ypos, state.players[0].zpos, state.players[0].speed, state.players[0].lap_completion, state.players[0].minutes, state.players[0].seconds, state.players[0].mushroom_boost))
            # if race_stage == 2 and state.stage != 2:
            #     print("finished?")
            #     # finished?
            #     sm.serialize2write()
            #     print("wrote controller data to controller_data.pkl")
            #     exit(0)
            # race_stage = state.stage


    def make_action(self, pad):
        exit(0) # unused
        print("sent A")
        pad.press_button(Pad.Button.A)

    def main(self):
        dolphin_dir = find_dolphin_dir()
        if dolphin_dir is None:
            print('Could not find dolphin config dir.')
            return

        state = State.State()
        sm = state_manager.StateManager(state)
        write_locations(dolphin_dir, sm.locations())

        stats = Stats.Stats()

        # fox = fox.Fox()

        try:
            print('Start dolphin now. Press ^C to stop p3.')
            pad_path = dolphin_dir + '/Pipes/p3'
            mw_path = dolphin_dir + '/MemoryWatcher/MemoryWatcher'
            print("time.sleep(1)")
            self.start_dolphin()
            a = input()
            with Pad.Pad(pad_path) as pad, memory_watcher.MemoryWatcher(mw_path) as mw:
                
                
                self._run(state, sm, mw, pad, stats)


        except KeyboardInterrupt:
            self.dolphin.kill()
            sm.serialize2write()
            with open("traj.pkl", "wb") as f:
                pickle.dump(pts, f)
            print('Stopped')
            print(stats)


player = Player()
player.run()