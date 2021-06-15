# Termex


---
FirstNode is termexLeptonCapture to run this node use (get image from camera and communication with them):
```
rosrun [pkg_name] termexLeptonCapture 

parameters:
  freq - frequency of getting image (default 8)
```
For example:
```
rosrun termex termexLeptonCapture _freq:=6
```

If u want use this node to send converted image u should modify termexLeptonCapture.cpp uncoment SCALED_IMAGE & RESIZE if u need.

To comunicate use topic `comand_console` type message std_msg/String. 
Example reset FFC: 
```
rostopic pub -1 comand_console std_msgs/String "FFC"
```
