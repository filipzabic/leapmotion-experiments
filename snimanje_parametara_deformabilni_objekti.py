import sys
import Leap
import matplotlib.pyplot as plt
import time
import numpy as np


class SnimacDeformabilnihObjekata(Leap.Listener):
    def __init__(self):
        time.clock()
        Leap.Listener.__init__(self)

        self.vremena = np.array([])

        self.pozicije_x = np.array([])
        self.pozicije_y = np.array([])
        self.pozicije_z = np.array([])

    def on_connect(self, controller):
        print "Spojen"

    def on_frame(self, controller):

        frame = controller.frame()
        kaziprst = frame.fingers.finger_type(Leap.Finger.TYPE_INDEX)[0]
        pozicija_kaziprsta = kaziprst.stabilized_tip_position

        if not frame.hands.is_empty and len(frame.hands) < 2:

            self.vremena = np.append(self.vremena, time.clock())

            self.pozicije_x = np.append(self.pozicije_x, pozicija_kaziprsta[0])
            self.pozicije_y = np.append(self.pozicije_y, pozicija_kaziprsta[1])
            self.pozicije_z = np.append(self.pozicije_z, pozicija_kaziprsta[2])


def main():
    listener = SnimacDeformabilnihObjekata()
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
    axs[2].set_ylabel("Z [mm]")
    axs[2].set_xlabel("Vrijeme [s]")

    plt.subplots_adjust(hspace=0.35)
    plt.show()

    controller.remove_listener(listener)


main()
