import Leap
import win32com.client
import time


ppt = win32com.client.Dispatch("PowerPoint.Application").ActivePresentation
slides = ppt.SlideShowWindow.View

controller = Leap.Controller()
controller.set_policy_flags(Leap.Controller.POLICY_BACKGROUND_FRAMES)

while True:
    frame = controller.frame()

    if not frame.hands.is_empty:

        if frame.hands[0].grab_strength > 0.98 and frame.hands[0].is_right:
            slides.Next()
            time.sleep(1)

        if frame.hands[0].grab_strength > 0.98 and frame.hands[0].is_left:
            slides.Previous()
            time.sleep(1)
