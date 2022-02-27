import sys
import Leap
import matplotlib.pyplot as plt
import time
import numpy as np


class DeformableObjectRecorder(Leap.Listener):
    def __init__(self):
        time.clock()
        Leap.Listener.__init__(self)

        self.times = np.array([])

        self.positions_x = np.array([])
        self.positions_y = np.array([])
        self.positions_z = np.array([])

    def on_connect(self, controller):
        print "Connected"

    def on_frame(self, controller):

        frame = controller.frame()
        index_finger = frame.fingers.finger_type(Leap.Finger.TYPE_INDEX)[0]
        index_finger_position = index_finger.stabilized_tip_position

        if not frame.hands.is_empty and len(frame.hands) < 2:

            self.times = np.append(self.times, time.clock())

            self.positions_x = np.append(self.positions_x, index_finger_position[0])
            self.positions_y = np.append(self.positions_y, index_finger_position[1])
            self.positions_z = np.append(self.positions_z, index_finger_position[2])


def main():
    
    listener = DeformableObjectRecorder()
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
    axs[2].set_ylabel("Z [mm]")
    axs[2].set_xlabel("Time [s]")

    plt.subplots_adjust(hspace=0.35)
    plt.show()

    controller.remove_listener(listener)


main()
