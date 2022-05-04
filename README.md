# Reinforcement Learning v. Mario Kart Wii

## Requirements

* `gym`
* `numpy`
* `OpenGL` for vis
* `Pangolin` for vis: [Pangolin](https://github.com/JackWBoynton/pangolin)
* `Dolphin >= 5.0` [Dolphin Emulator](https://github.com/JackWBoynton/dolphin) (my fork required for hotkey automation)

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
* `dolphin_configs`
  * `Dolphin.ini` -> `~/Library/Application Support/Dolphin/Config/`
  * `GCPadNew.ini` -> `~/Library/Application Support/Dolphin/Config/`
  * `Hotkeys.ini` -> `~/Library/Application Support/Dolphin/Config/`
  * `Profiles/*` -> `~/Library/Application Support/Dolphin/Config/`

### Monitored RAM Locations

PAL Version of MKwii
| Address | Offset   | Description |
| --- | -----------  | ----------- |
| 0x809C18F8 | 0x2B  |  Stage Data (0: intro-camera, 1: race-countdown, 2: racing) |
| 0x809BD70C | 0x61  |  Moving Direction (1: forward, 2: backward) |
| 0x809BD70C | 0x3C  |  Steering Direction (0: left, 7: straight, 14: right) |
| 0x809BD70C | 0x63  |  Use Item (0: No, 1: Yes) |
| 0x809BD70C | 0x4B  |  DPad (8: Up, 16: Down, 32: Left, 64: Right) |
| 0x809BD730 | 0x111 |  Current Lap (int) |
| 0x809BD730 | 0x112 |  Maximum Lap (int) |
| 0x809BD730 | 0xFC  |  Max Lap Completion (float 1.5 -> halfway through first lap etc.)  |
| 0x809BD730 | 0xF8  |  Current Lap Completion (float 1.5 -> halfway through first lap etc.)  |
| 0x809C2EF8 | 0x40 + 0x0  |  X Position (float)  |
| 0x809C2EF8 | 0x40 + 0x4  |  Y Position (float)  |
| 0x809C2EF8 | 0x40 + 0x8  |  Z Position (float)  |
| 0x809C2EF8 | 0x40 - 0x160  |  Previous X Position (float)  |
| 0x809C2EF8 | 0x40 - 0x160 + 0x4 |  Previous Y Position (float)  |
| 0x809C2EF8 | 0x40 - 0x160 + 0x8 |  Previous Z Position (float)  |
| 0x809BD730 | 0x1B9 |  Minutes  |
| 0x809BD730 | 0x1BA |  Seconds  |
| 0x809BD730 | 0x1BC |  Third-Seconds  |

[MarioKart Wii Symbol Map](https://docs.google.com/spreadsheets/d/1gA5WmnEbPAeA1Lq4XUJg9qDwawky9hpNUv2n1wWRwno/edit#gid=1610171642)

### Usage

Environment Variables:

* Set `DOLPHIN_CONF_DIR` to the Dolphin Emulator User directory (MacOS : `~/Library/Application Support/Dolphin`)
* Set `DOLPHIN_DIR` to the location of the Dolphin Binary (ex: `dolphin/build/Binaries/Dolphin.app/Contents/MacOS/Dolphin`)
* Set `MK_ISO` to the location of the game iso

In-Progress:

* `CENTER_TRAJ` 3D trajectory for driving on the centerline (`centerline_traj.npy`)
* `LEFT_TRAJ` 3D trajectory for driving on the left side of the track (`lefttraj.npy`)
* `RIGHT_TRAJ` 3D trajectory for driving on the right side of the track (`righttraj.npy`)

```bash
python3 -m pip install -e mario-env
```

```python3
import gym
import mario_env

env_id = "MarioEnv-v0"

env = gym.make(env_id)
env.reset()
```

## TODO

* Use trajectories of edges of the road to determine if kart is on the track or not
  * It seems that the x, z coordinates correspond to the 2D movement along the track and y is the elevation
* Save trajectories for offline visualization
* Update Dolphin Emulator to allow for unix fifo pipe frame dumps
  * Train object detection model to detect obstacles in the road for grand prix races
