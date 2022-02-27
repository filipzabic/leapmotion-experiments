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

        roll = math.atan(frame.hands[0].palm_normal.x/frame.hands[0].palm_normal.y)
        pitch = math.atan(frame.hands[0].palm_normal.z/frame.hands[0].palm_normal.y)

        x_movement = 0.001 * roll
        y_movement = 0.001 * pitch

        model.TranslateBy(x_movement, y_movement)
