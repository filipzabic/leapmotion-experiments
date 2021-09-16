import sys
import Leap
import matplotlib.pyplot as plt
import time
import numpy as np


class SnimacRuku(Leap.Listener):
    def __init__(self):
        time.clock()
        Leap.Listener.__init__(self)

        self.vremena = np.array([])

        self.pozicije_x = np.array([])
        self.pozicije_y = np.array([])
        self.pozicije_z = np.array([])

        self.brzine_x = np.array([])
        self.brzine_y = np.array([])
        self.brzine_z = np.array([])

    def on_connect(self, controller):
        print "Spojen"

    def on_frame(self, controller):

        frame = controller.frame()

        if not frame.hands.is_empty and len(frame.hands) < 2:

            self.vremena = np.append(self.vremena, time.clock())

            self.pozicije_x = np.append(self.pozicije_x, frame.hands[0].palm_position[0])
            self.pozicije_y = np.append(self.pozicije_y, frame.hands[0].palm_position[1])
            self.pozicije_z = np.append(self.pozicije_z, frame.hands[0].palm_position[2])

            self.brzine_x = np.append(self.brzine_x, frame.hands[0].palm_velocity[0])
            self.brzine_y = np.append(self.brzine_y, frame.hands[0].palm_velocity[1])
            self.brzine_z = np.append(self.brzine_z, frame.hands[0].palm_velocity[2])


def main():
    listener = SnimacRuku()
    controller = Leap.Controller()
    controller.add_listener(listener)

    print "Pritisni Enter za izlaz..."
    sys.stdin.readline()

    fig, axs = plt.subplots(3)
    fig.set_size_inches(10, 7)

    axs[0].plot(listener.vremena, listener.pozicije_x)
    axs[0].set_ylabel("X [mm]")
    axs[0].set_xlabel("Vrijeme [s]")

    axs[1].plot(listener.vremena, listener.pozicije_y)
    axs[1].set_ylabel("Y [mm]")
    axs[1].set_xlabel("Vrijeme [s]")

    axs[2].plot(listener.vremena, listener.pozicije_z)
    axs[2].set_ylabel("Z [mm/s]")
    axs[2].set_xlabel("Vrijeme [s]")

    plt.subplots_adjust(hspace=0.35)

    fig2, axs2 = plt.subplots(3)
    fig2.set_size_inches(10, 7)

    axs2[0].plot(listener.vremena, listener.brzine_x)
    axs2[0].set_ylabel("X [mm/s]")
    axs2[0].set_xlabel("Vrijeme [s]")

    axs2[1].plot(listener.vremena, listener.brzine_y)
    axs2[1].set_ylabel("Y [mm/s]")
    axs2[1].set_xlabel("Vrijeme [s]")

    axs2[2].plot(listener.vremena, listener.brzine_z)
    axs2[2].set_ylabel("Z [mm/s]")
    axs2[2].set_xlabel("Vrijeme [s]")

    plt.subplots_adjust(hspace=0.35)
    plt.show()

    controller.remove_listener(listener)


main()
