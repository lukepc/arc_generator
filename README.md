# Arc Generator
### ArcMap toolbox and the python code within that builds arcs centered on points in a feature layer, oriented away from another feature layer.

This repository includes the ArcMap Toolbox ("Arcs from points.tbx") and the python code for the two tools contained within. 
The tools both generate arcs centered on point feature layers chosen by the user. The arcs open away from either a user-defined origin
point (arcs_from_points_origins.py) or from the nearest feature in the a user-defined layer (arcs_from_points_nearest.py). Curvature 
of the arcs is based on the user-input "radius," that defines the circle used to generate the arcs. Length of the arc is chosen by the user.


Notes: 

All code is rough and uncommented.

Arcs don't behave properly if the desired arc length conflicts with the circle size (eg if length > ( 4 * pi * radius ) )


