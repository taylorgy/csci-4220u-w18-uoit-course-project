# csci-4220u-w18-uoit-course-project
This is the course project of csci-4220u-w18-uoit: Computer Vision.

## [Optical Flow] Gesture recognition using python + opencv.  
Use laptop camera to capture images while moving finger to one direction (up, down, left, right, up-left, etc.) in the air. The gesture recognition program identifies the motion of the finger between every two frames to calculate the motion direction and velocity, then shows the motion simultaneously by moving a ball on the canvas. As shown in the following figure.  

![image](https://github.com/TaylorGy/csci-4220u-w18-uoit-course-project/blob/master/schematic_diagram.png)  

*Key words:* Optical Flow, Hand and Gesture Detection, YCrCb and HSV Color Space

## Environment  
- Hardware: laptop with camera  
- Software:  
  - OS: Windows 7+  
  - Language: Python 2.7  
  - Libraries: Opencv 2.4, numpy. (You coulde use pip to install required libs)

## Usage
- project.py
- In cmd:
```
$ python project.py [<video_source>]
# default video_source is laptop camera
```
- key operations of program:
  1 - toggle optical flow visualization
  2 - toggle hand contours visualization
  3 - toggle HSV flow visualization

- press 'ESC' to quit

## Result demo

![image](https://github.com/TaylorGy/csci-4220u-w18-uoit-course-project/blob/master/demo.png)  

## Reference
[1] R. M. Baby and R. R. Ahamed, "Optical Flow Motion Detection on Raspberry Pi," 2014 Fourth International Conference on Advances in Computing and Communications, Cochin, 2014, pp. 151-152.  
URL: http://ieeexplore.ieee.org.uproxy.library.dc-uoit.ca/stamp/stamp.jsp?tp=&arnumber=6906011&isnumber=6905967
[2] URL:https://sandipanweb.wordpress.com/2018/02/25/implementing-lucas-kanade-optical-flow-algorithm-in-python/
[3] URL:https://www.intorobotics.com/9-opencv-tutorials-hand-gesture-detection-recognition/
[4] URL:http://creat-tabu.blogspot.ca/2013/08/opencv-python-hand-gesture-recognition.html
