import Leap
import math
from ctypes import windll
import win32com.client


win32 = windll.user32

solidworks = win32com.client.Dispatch("SldWorks.Application")
part = solidworks.ActiveDoc
model = part.ActiveView

controller = Leap.Controller()
controller.set_policy_flags(Leap.Controller.POLICY_BACKGROUND_FRAMES)

while True:

    frame = controller.frame()

    if not frame.hands.is_empty:

        pitch = -1.0 * math.atan(frame.hands[0].palm_normal.z / frame.hands[0].palm_normal.y)

        if pitch < 0:

            pitch = abs(pitch) + 0.99*(1 - abs(pitch))
            model.ZoomByFactor(pitch)

        elif pitch > 0:

            pitch = 1 + 0.1*pitch
            model.ZoomByFactor(pitch)
