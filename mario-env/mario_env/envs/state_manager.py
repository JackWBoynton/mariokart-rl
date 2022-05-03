
import struct
import time
import pickle
import numpy as np
from copy import deepcopy

import queue

from .state import State
from .state import PlayerType
from .state import Character
from .state import Menu, ScreenID
from .constants import *

POSMAP = {"xpos": (XMIN, XMAX), "ypos": (YMIN, YMAX), "zpos": (ZMIN, ZMAX)}

def norm(val, name):
    if "_" in name:
        name = name.split("_")[-1]

    mi, ma = POSMAP[name]
    return float((val - mi) / (ma - mi))  # [0, 1]


def int_handler(obj, name, shift=0, mask=0xFF, wrapper=None, default=None, que=None):
    """Returns a handler that sets an attribute for a given object.
    obj is the object that will have its attribute set. Probably a State.
    name is the attribute name to be set.
    shift will be applied before mask.
    Finally, wrapper will be called on the value if it is not None. If wrapper
    raises ValueError, sets attribute to default.
    This sets the attribute to default when called. Note that the actual final
    value doesn't need to be an int. The wrapper can convert int to whatever.
    This is particularly useful for enums.
    """

    def handle(value, addr):
        if mask == 0xFF:
            transformed = struct.unpack("B", value[:1])[0]  # convert first byte to int
        else:
            transformed = (struct.unpack(">i", value)[0] >> shift) & mask


        if isinstance(que, list):
            que.append((time.time_ns(), name, transformed))

        setattr(obj, name, generic_wrapper(transformed, wrapper, default))

    setattr(obj, name, default)
    return handle


def float_handler(obj, name, wrapper=None, default=0.0, que=None, mask=0xFFFFFF):
    """Returns a handler that sets an attribute for a given object.
    Similar to int_handler, but no mask or shift.
    """

    def handle(value, addr):
        try:
            if mask == 0xFFFF:
                as_float = np.frombuffer(value[:2], dtype=">f2")[0]
                print(as_float)
            else:
                as_float = struct.unpack(">f", value)[0]

            if name in ["xpos", "ypos", "zpos"] or (
                "_" in name and name.split("_")[-1] in ["xpos", "ypos", "zpos"]
            ):
                as_float = norm(as_float, name)

            if isinstance(que, list):
                que.append((time.time_ns(), name, as_float))
            setattr(obj, name, generic_wrapper(as_float, wrapper, default))
        except Exception as e:
            print(e, value, name)

    setattr(obj, name, default)
    return handle


def generic_wrapper(value, wrapper, default):
    if wrapper is not None:
        try:
            value = wrapper(value)
        except ValueError as e:
            print(e, value, default)
            value = default
    return value


def pointer_handler(obj, name, wrapper=None, default=0):
    def handle(value):
        as_pointer = int("".join(value), 16)
        setattr(obj, name, generic_wrapper(as_pointer, wrapper, default))

    setattr(obj, name, default)
    return handle


def add_address(x, y):
    """Returns a string representation of the sum of the two parameters.
    x is a hex string address that can be converted to an int.
    y is an int.
    """
    return "{0:08X}".format(int(x, 16) + y)


class StateManager:
    """Converts raw memory changes into attributes in a State object."""

    def __init__(self, state):
        """Pass in a State object. It will have its attributes zeroed."""

        self.controller_data = []
        self.state_data = []
        self.player_data = []

        self.state = state
        self.addresses = {}

        #### STATE

        RaceInfo = str(hex(0x809BD730))[2:]

        #### PLAYER

        playerbase = 0x809C18F8
        raceData2 = str(hex(0x809BD730))[2:] + " C" + " 0"
        PosPointer = str(hex(0x9C2EF8 + 0x80000000))[2:] + " 40"
        controllerData = str(hex(0x809BD70C))[2:]

        menu = str(hex(0x809C2850))[2:]  # correct

        self.addresses[menu + " 7"] = int_handler(
            self.state,
            "menu_identifier",
            mask=0xFF,
            que=self.state_data,
            wrapper=ScreenID,
            default=ScreenID.LOADING,
        )  # https://wiki.tockdom.com/wiki/List_of_Identifiers#Screen_Identifiers

        playerbase = str(hex(playerbase))[2:]

        self.addresses[RaceInfo + " 2B"] = int_handler(
            self.state, "stage", mask=0xFF, que=self.state_data
        )  # 0->introcamera or prerace, 1->countdown, 2-->race

        # controller inputs
        self.addresses[controllerData + " 61"] = int_handler(
            self.state, "acceleration", que=self.controller_data
        )  # 0->None, 1->forward, 2->backward
        self.addresses[controllerData + " 3C"] = int_handler(
            self.state, "steer", que=self.controller_data
        )  # 0->left, 7->straight, 14->right

        self.addresses[controllerData + " 63"] = int_handler(
            self.state, "item", que=self.controller_data
        )
        self.addresses[controllerData + " 4B"] = int_handler(
            self.state, "dpad", que=self.controller_data
        )  # 8->up, 16->down, 32->left, 64->right and combs

        # lap
        self.addresses[RaceInfo + " 111"] = int_handler(
            self.state, "current_lap", mask=0xFF, que=self.player_data
        )
        self.addresses[RaceInfo + " 112"] = int_handler(
            self.state, "max_lap", mask=0xFF, que=self.player_data
        )  # 127

        self.addresses[RaceInfo + " 127"] = int_handler(
            self.state, "state_flags", mask=0xFF, que=self.player_data
        )  # 1-> inrace, 5->driving wrong way,
        self.addresses[RaceInfo + " FC"] = float_handler(
            self.state, "max_lap_completion", que=self.player_data
        )  # 1.5 halfway through lap 1, 2.5 halfway through lap 2
        self.addresses[RaceInfo + " F8"] = float_handler(
            self.state, "current_lap_completion", que=self.player_data
        )  # 1.5 halfway through lap 1, 2.5 halfway through lap 2

        self.addresses[PosPointer + " 0"] = float_handler(
            self.state, "xpos", que=self.player_data
        )
        self.addresses[PosPointer + " 4"] = float_handler(
            self.state, "ypos", que=self.player_data
        )
        self.addresses[PosPointer + " 8"] = float_handler(
            self.state, "zpos", que=self.player_data
        )

        self.addresses[PosPointer + " -160"] = float_handler(
            self.state, "prev_xpos", que=self.player_data
        )
        self.addresses[PosPointer + " -160" + " 4"] = float_handler(
            self.state, "prev_ypos", que=self.player_data
        )
        self.addresses[PosPointer + " -160" + " 8"] = float_handler(
            self.state, "prev_zpos", que=self.player_data
        )

        # Below here doesn't work
        # self.addresses[playerbase + " 20" + " 10" + " 10" + " 21A"] = int_handler(player, "airtime", que=self.player_data)
        # self.addresses[playerbase + " 20" + " 10" + " 10" + " FE"] = int_handler(player, "mt_charge", que=self.player_data)
        # self.addresses[playerbase + " 20" + " 10" + " 10" + " 14C"] = int_handler(player, "ssmt_charge", que=self.player_data)
        # self.addresses[playerbase + " 20" + " 10" + " 10" + " 114"] = float_handler(player, "trick_boost", que=self.player_data)
        # self.addresses[playerbase + " 20" + " 10" + " 10" + " 110"] = float_handler(player, "mushroom_boost", que=self.player_data)
        # self.addresses[playerbase + " 20" + " 10" + " 10" + " 11C"] = float_handler(player, "mt_boost", que=self.player_data)
        # self.addresses[playerbase + " 20" + " 10" + " 10" + " 20"] = float_handler(player, "speed", mask=0xFFFF, que=self.player_data)

        # self.addresses[raceData2 + " 28"] = int_handler(player, "kpt", que=self.player_data)
        # self.addresses[raceData2 + " C"] = float_handler(player, "race_completion", que=self.player_data)
        # self.addresses[raceData2 + " 1C"] = float_handler(player, "lap_completion", que=self.player_data)

        # resume HERE

        self.addresses[RaceInfo + " 1B9"] = int_handler(
            self.state, "minutes", mask=0xFF, que=self.player_data
        )
        self.addresses[RaceInfo + " 1BA"] = int_handler(
            self.state, "seconds", mask=0xFF, que=self.player_data
        )
        self.addresses[RaceInfo + " 1BC"] = int_handler(
            self.state, "thirdseconds", mask=0xFF, que=self.player_data
        )

    def handle(self, address, value):
        """Convert the raw address and value into changes in the State."""

        if address not in self.addresses:
            return
        handlers = self.addresses[address]
        if isinstance(handlers, list):
            for handler in handlers:
                handler(value, address)
        else:
            handlers(value, address)

    def locations(self):
        """Returns a list of addresses for exporting to Locations.txt."""
        return self.addresses.keys()

    def serialize2write(self, filename):
        print("saving trajectories...")
        out = self.get_xyz_traj()
        np.save(filename, out)

    def get_xyz_traj(self):
        out = []
        pd = self.player_data
        for p in pd[::-1]:
            if p[1] in ["xpos", "ypos", "zpos"]:
                out.append((p[1], p[2]))
        return out
