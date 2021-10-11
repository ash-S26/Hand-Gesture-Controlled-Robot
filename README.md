# HAND-GESTURE-CONTROLLED-ROBOT
________________________________
This project is all about creating a robot which can be controlled with hand gestures which have commands like rotate, move forward and backward, accelarate and stop.The project have two parts ➡
 1) Detection of Hand_Gesture using opencv library.
 2) Integrating Hand_Gesture to publish commands to robot.

# DEPENDENCIES/PAKAGES
________________________
 1) Image processing library opencv 
 2) ROS(Robot operating system , version-noetic)
 3) Gazebo (if not installed along with ROS)
 4) pakages :-
   - ros_controll {To be cloned in catkin_ws}
   - Join_state_controller (if not included in ros_controll) {To be cloned in src folder of catkin_ws}
   - Turtlebot3 pakage - (https://emanual.robotis.com/docs/en/platform/turtlebot3/simulation/#gazebo-simulation) {To be cloned in src folder of catkin_ws}
         


# ALORITHM
____________

 # ALORITHM FOR DETECTION OF HAND_GESTURE
   1) Seperate out the skin color from the input frame (captured through attached camera) using HSV or other color format with upper and lower bound for skin color as per range.
   2) Removal of noise from image via dialation and errosion, and applying filters to smooothen the image.
   3) Finding the contour of the mask(seperated skin color mask) and drawing convex-hull.
   4) Using the various properties for seperation various Hand_Gestures(In this project we will use Indian-sign-language as Hand_Gesture- 1,2,3..) like-
      - Finding the extreme most points of contours and computing angle between bottommost and other extreme points and using the values in if loop.
      - Finding the corner points of hull.
      - Finding number of lines in contour of specific gesture.
      - Area of contour for different gestures.
   
 # ALGORITHM FOR ROBOT
   For this project we used ROS noetic, turtlesim and turtlebot3.
   1) We used gazebo for simulation.
   2) We used ros-topic /cmd_vel for publishing velocity message to robot in gazebo simulation.
 
 # INTEGRATION
   Finally we publish angular and linear velocity as per motion we want on specific Hand_Gesture.
   
# HOW TO RUN THE CODE 
________________________
  1) git clone 
  2) export TURTLEBOT3_MODEL=burger
  3) roslaunch turtlebot3_gazebo turtlebot3_empty_world.launch
  4) python3 Hand_Gestur_Controlled_Robot.py {Finally run the code by navigating to directory where you cloned and then to where is code Hand_Gestur_Controlled_Robot.py}
  5) Or you can run code from any code editor.
  
# RESULTS 
__________

  
