import sys
import math
import Leap
import ctypes
import win32api
import win32con
import time
import matplotlib.pyplot as plt
import numpy as np
win32 = ctypes.windll.user32


class PalmRecorder(Leap.Listener):
    def __init__(self):
        time.clock()
        Leap.Listener.__init__(self)

        self.times = np.array([])

        self.pitches = np.array([])
        self.rolls = np.array([])

        self.x = 0
        self.y = 0

        self.x_max = win32.GetSystemMetrics(0) - 1
        self.y_max = win32.GetSystemMetrics(1) - 1

        self.grip_strength_limit = 0.98
        self.scroll_up_limit = 0.175
        self.scroll_down_limit = -0.2

    def on_connect(self, controller):
        print "Connected"

    def on_frame(self, controller):

        frame = controller.frame()

        if not frame.hands.is_empty:

            roll = math.atan(frame.hands[0].palm_normal.x/frame.hands[0].palm_normal.y)
            pitch = math.atan(frame.hands[0].palm_normal.z/frame.hands[0].palm_normal.y) * -1

            self.times = np.append(self.times, time.clock())
            self.pitches = np.append(self.pitches, pitch)
            self.rolls = np.append(self.rolls, roll)

            x_movement = 8 * roll
            y_movement = 8 * pitch

            self.x = self.x + x_movement
            self.y = self.y + y_movement

            if self.x > self.x_max:
                self.x = self.x_max
            elif self.x < 0.0:
                self.x = 0.0

            if self.y > self.y_max:
                self.y = self.y_max
            elif self.y < 0.0:
                self.y = 0.0

            win32.SetCursorPos(int(self.x), int(self.y))

            if frame.hands[0].pinch_strength > self.grip_strength_limit:

                win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, int(self.x), int(self.y), 0, 0)
                win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, int(self.x), int(self.y), 0, 0)

                time.sleep(0.2)


def main():

    listener = PalmRecorder()

    controller = Leap.Controller()
    controller.set_policy_flags(Leap.Controller.POLICY_BACKGROUND_FRAMES)
    controller.add_listener(listener)

    print "Press Enter to exit..."
    sys.stdin.readline()

    fig, axs = plt.subplots(2)
    fig.set_size_inches(8, 5)

    axs[0].plot(listener.times, listener.pitches)
    axs[0].set_ylabel("Pitch [rad]")
    axs[0].set_xlabel("Time [s]")

    axs[1].plot(listener.times, listener.rolls)
    axs[1].set_ylabel("Roll [rad]")
    axs[1].set_xlabel("Time [s]")

    plt.subplots_adjust(hspace=0.35)
    plt.show()

    controller.remove_listener(listener)


main()
