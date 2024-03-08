# asCAD
Application for automatical generation of industrial robot's trajectory (Kawasaki) based on the 2D CAD drawing.
Supported CAD drawing format is dxf file (Drawing Interchange Format - developed by Autodesk to enable data interoperability between AutoCAD and other programs).
Possible use cases: welding, gripping or laser cutting using Kawasaki industrial robot.
GUI created in wxPython, the cross-platform GUI toolkit for the Python language.

Possible improvements:
- supporting 3D trajectories
- direct communication with Kawasaki controller (currently the AS code is generated within application and can be saved to a file which needs to be copied to a controller)

![image](https://user-images.githubusercontent.com/36520228/201860348-fa47011f-f9da-43ab-bd65-597b128cc66b.png)

