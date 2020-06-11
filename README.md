"Search my stuff robot"       
 ----------------------------------------------------------------- 

This code contains my entry for [the Devpost AWS Marketplace Developer Challenge](https://awsmarketplaceml.devpost.com/). 

## Goal

The goal of this project is to be able to tell a robot "Find my red shoes." and it will drive around the house, automatically mapping its environment and it will use [the GluonCV YOLOv3 Object Detector](https://aws.amazon.com/marketplace/pp/prodview-5jlvp43tsn3ny) to find what I'm looking for.

Right now, that's not how it works. I severely underestimated the effort in building an actual real working robot and making it intelligent.

So what is there:

* A tracked robot running a Raspberry Pi with a camera attached.
* The robot is connected to AWS RoboMaker through AWS GreenGrass.
* A simple web interface is available to see what the robot is seeing and to control it.
* A button will send the current camera image to SageMaker and report back what is visible on screen.

[![YouTube demo](http://img.youtube.com/vi/mj5foOQ_A78/0.jpg)](http://www.youtube.com/watch?v=mj5foOQ_A78 "Find my stuff Robot")

## AWS services used

The YOLO model is loaded into SageMaker and RoboMaker is used to manage the robot and simulate test scenarios.

## Complexity

As I mentioned before. This turned out to be much more complex.

* I had no idea what kind of battery to use, so the motor's are now badly underpowered. Turns out, simply choosing and ordering a good power system for a robot takes multiple days.
* The robot does not drive straight. Partly due to the battery issue, but also partly because I was naïve. I still need to get to the bottom of this, but I need some feedback mechanism so the robot knows it needs to correct its trajectory. It looks like encoders on the motors are the quickest fix.
* Although AWS RoboMaker and GreenGrass are awesome services and do a good job of making this a lot easier, it's still very complex. I also got the feeling RoboMaker is not a fully fleshed out service yet. [Sometimes its hard to get to the errors or logs](https://stackoverflow.com/questions/61124934/how-to-debug-aws-robomaker-launch-after-deployment) (or more likely, I was too impatient and eager on moving ahead to find it in the documentation)

## The code

As you will have noticed, this repository was started from the HelloWorld RoboMaker app. It still bears many, many references to that project. I will be removing them as I progress into the project.

The robot itself is compatible with the Turtlebot that is used in the simulation (it accepts /cmd_vel messages), but I've not yet figured out how to integrate the camera.

## Running the code

If you want to try out the code:

* You'll need a Raspberry Pi based robot with a motor controller connected to the GPIO pins and the standard Raspberry Pi camera
* ROS Melodic running on the Raspberry Pi

Follow these steps:

* Install dependencies:
  * `pip install pyyaml imutils boto3`
* Build the workspace:
  * `cd ~/ros-robot-control/HelloWorld/robot_ws`
  * `catkin_make` 
* Source the `setup.bash` script: 
  * `echo "source /home/pi/ros-robot-control/HelloWorld/robot_ws/devel/setup.bash" >> ~/.bashrc`
  * `source ~/.bashrc`
* Update [cmd_vel_listener.py](https://github.com/pbackx/ros-robot-control/blob/master/HelloWorld/robot_ws/src/ros_robot_control/scripts/cmd_vel_listener.py) to reflect your configuration (most importantly lines 57 and 58 that contain the GPIO pins used to control the motors)
* Launch the GluonCV model, pretty much as describe in the documentation and [update line 55 of the interface file to put in the correct ARN](https://github.com/pbackx/ros-robot-control/blob/master/HelloWorld/robot_ws/src/robot_interface/nodes/web#L55).
* Now launch the [deploy_rotate.launch](https://github.com/pbackx/ros-robot-control/blob/master/HelloWorld/robot_ws/src/robot_interface/launch/deploy_rotate.launch) file using `roslaunch`.
* In your browser (tested with the latest Chrome), surf to http://<ip-of-your-robot>:5000

That should be it. Feel free to open an issue if you need more support. I will clean things up as I move along.

