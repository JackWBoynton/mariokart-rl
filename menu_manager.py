import math

import pad

class MenuManager:
    def __init__(self):
        self.selected_fox = False

    def pick_fox(self, state, pad):
        if self.selected_fox:
            # Release buttons and lazilly rotate the c stick.
            pad.release_button(pad.Button.A)
            pad.tilt_stick(pad.Stick.MAIN, 0.5, 0.5)
            angle = (state.frame % 240) / 240.0 * 2 * math.pi
            pad.tilt_stick(pad.Stick.C, 0.4 * math.cos(angle) + 0.5, 0.4 * math.sin(angle) + 0.5)
        else:
            # Go to fox and press A
            target_x = -23.5
            target_y = 11.5
            dx = target_x - state.players[2].cursor_x
            dy = target_y - state.players[2].cursor_y
            mag = math.sqrt(dx * dx + dy * dy)
            if mag < 0.3:
                pad.press_button(pad.Button.A)
                self.selected_fox = True
            else:
                pad.tilt_stick(pad.Stick.MAIN, 0.5 * (dx / mag) + 0.5, 0.5 * (dy / mag) + 0.5)



    def start_sequence(self, state, pad):
        pad.press_button(pad.Button.A)
        

    def press_start_lots(self, state, pad):
        if state.frame % 2 == 0:
            pad.press_button(pad.Button.START)
        else:
            pad.release_button(pad.Button.START)