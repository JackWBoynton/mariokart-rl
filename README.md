# Reinforcement Learning in Mario Kart Wii

## Requirements

* `gym`
* `numpy`
* `OpenGL` for vis
* `Pangolin` for vis: [Pangolin](https://github.com/JackWBoynton/pangolin)

## OpenAI Gym Environment

### Structure

* `mario-env`
  * `mario_env`
    * `envs`
      * `marioenv.py`
        * Main Gym environment
      * `memory_watcher.py`
        * Blocking memory watching script to monitor memory changes from Dolphin Emulator.
      * `trajectory.py`
        * Helper class to store trajectory information (x, y, z) from memory updates
      * `state.py`
        * Helper class to store enums for state inforation and State objects to store state information
      * `threaded_memory_watcher.py`
        * Threaded memory watching script (replaces `memory_watcher.py` and `state_manager.py`)
      * `state_manager.py`
        * Script to accept memory updates and parse them into proper numerical state information
      * `pangolin_handler.py`
        * Houses threaded Visualizer object to update a 3D plot of current trajectory and others. Requires [Pangolin](https://github.com/JackWBoynton/pangolin)
      * `pad.py`
        * Houses logic to send controller commands and hotkeys to Dolphin Emulator
      * `constants.py`
        * Configuration options

## TODO:

* 