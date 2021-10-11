# HAND-GESTURE-CONTROLLED-ROBOT
This project is all about creating a robot which can be controlled with hand gestures which have commands like rotate, move forward and backward, accelarate and stop.The project have two parts ➡
 1) Detection of Hand_Gesture using opencv library.
 2) Integrating Hand_Gesture to publish commands to robot.

# ALORITHM FOR DETECTION OF HAND_GESTURE
  1) Seperate out the skin color from the input frame (captured through attached camera) using HSV or other color format with upper and lower bound for skin color as per range.
  2) Removal of noise from image via dialation and errosion, and applying filters to smooothen the image.
  3) Finding the contour of the mask(seperated skin color mask) and drawing convex-hull.
  4)  

