import sys
import Leap
import matplotlib.pyplot as plt
import time
import numpy as np


class HandRecorder(Leap.Listener):
    def __init__(self):
        time.clock()
        Leap.Listener.__init__(self)

        self.times = np.array([])

        self.positions_x = np.array([])
        self.positions_y = np.array([])
        self.positions_z = np.array([])

        self.speeds_x = np.array([])
        self.speeds_y = np.array([])
        self.speeds_z = np.array([])

    def on_connect(self, controller):
        print "Connected"

    def on_frame(self, controller):

        frame = controller.frame()

        if not frame.hands.is_empty and len(frame.hands) < 2:

            self.times = np.append(self.times, time.clock())

            self.positions_x = np.append(self.positions_x, frame.hands[0].palm_position[0])
            self.positions_y = np.append(self.positions_y, frame.hands[0].palm_position[1])
            self.positions_z = np.append(self.positions_z, frame.hands[0].palm_position[2])

            self.speeds_x = np.append(self.speeds_x, frame.hands[0].palm_velocity[0])
            self.speeds_y = np.append(self.speeds_y, frame.hands[0].palm_velocity[1])
            self.speeds_z = np.append(self.speeds_z, frame.hands[0].palm_velocity[2])


def main():

    listener = HandRecorder()
    controller = Leap.Controller()
    controller.add_listener(listener)

    print "Press Enter to exit..."
    sys.stdin.readline()

    fig, axs = plt.subplots(3)
    fig.set_size_inches(10, 7)

    axs[0].plot(listener.times, listener.positions_x)
    axs[0].set_ylabel("X [mm]")
    axs[0].set_xlabel("Time [s]")

    axs[1].plot(listener.times, listener.positions_y)
    axs[1].set_ylabel("Y [mm]")
    axs[1].set_xlabel("Time [s]")

    axs[2].plot(listener.times, listener.positions_z)
    axs[2].set_ylabel("Z [mm/s]")
    axs[2].set_xlabel("Time [s]")

    plt.subplots_adjust(hspace=0.35)

    fig2, axs2 = plt.subplots(3)
    fig2.set_size_inches(10, 7)

    axs2[0].plot(listener.times, listener.speeds_x)
    axs2[0].set_ylabel("X [mm/s]")
    axs2[0].set_xlabel("Time [s]")

    axs2[1].plot(listener.times, listener.speeds_y)
    axs2[1].set_ylabel("Y [mm/s]")
    axs2[1].set_xlabel("Time [s]")

    axs2[2].plot(listener.times, listener.speeds_z)
    axs2[2].set_ylabel("Z [mm/s]")
    axs2[2].set_xlabel("Time [s]")

    plt.subplots_adjust(hspace=0.35)
    plt.show()

    controller.remove_listener(listener)


main()
