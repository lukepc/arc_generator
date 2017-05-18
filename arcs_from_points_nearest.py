import arcpy
import math
import os
import numpy as np
from arcpy import env


arcpy.env.overwriteOutput = True

pts = arcpy.GetParameterAsText(0)
near_features = arcpy.GetParameterAsText(1)
full = arcpy.GetParameterAsText(2)
crad = float(arcpy.GetParameterAsText(3))
arc_length = float(arcpy.GetParameterAsText(4))

spatial_ref = arcpy.Describe(pts).spatialReference

fields = ["OBJECTID", "SHAPE", "SHAPE@X", "SHAPE@Y", "NEAR_X", "NEAR_Y"]
outpath = "C:/Users/lukepc/on_board_bear_files/arc_files/build_fence_lines/Whistler_main.gdb"
outname = "test"
outlines = outpath + "/testlines"
temp_pts = "temp_pts_file"
temp_line = "temp_line_file"

if(arc_length > ( 2 * math.pi * crad )):
   print("Error: Desired arc length is longer than circumference of circle defined by radius.")

arcpy.CopyFeatures_management(pts, "temp_pts_file")
arcpy.Near_analysis(temp_pts, near_features,"", "LOCATION")

    
try:
    arcpy.CreateFeatureclass_management(outpath, outname, "POINT", spatial_reference = spatial_ref)
    arcpy.AddField_management(outname, "ID", "TEXT", field_length = 50)
    arcpy.AddField_management(outname, "orderfield", "SHORT", field_length = 10)


    with arcpy.da.SearchCursor(temp_pts, fields) as cursor:
                for row in cursor:
                    x0 = row[4]
                    y0 = row[5]
                    objid = row[0]
                    x1 = row[2]
                    y1 = row[3]

                    theta = math.atan2((y1 - y0), (x1 - x0)) 
                    x3 = crad*math.cos(theta) + x1
                    y3 = crad*math.sin(theta) + y1
                    theta2 = theta + math.pi


                    for i in range(1, 11):
                      
                         al = arc_length / ( crad * i )

                         thetaip = theta2 + ( al / 2)
                         thetaim = theta2 - ( al  / 2)

                         xi4 = crad * math.cos(thetaip) + x3
                         yi4 = crad * math.sin(thetaip) + y3
                         xi5 = crad * math.cos(thetaim) + x3 
                         yi5 = crad * math.sin(thetaim) + y3

                         cursin = arcpy.da.InsertCursor(outname, ("SHAPE@X", "SHAPE@Y", "ID", "orderfield"))
                         n_order = 10 + i - 10
                         xy = (xi4, yi4, objid, n_order)
                         cursin.insertRow(xy)
                         n_order = 10 + 10 - i
                         xy = (xi5, yi5, objid, n_order)
                         cursin.insertRow(xy)    
            
             
    inpoints = "test"
    
    arcpy.PointsToLine_management(inpoints, temp_line, "ID", "orderfield", "NO_CLOSE")
    arcpy.cartography.SmoothLine(temp_line, full, "BEZIER_INTERPOLATION", 0)
    
    arcpy.Delete_management(inpoints)
    arcpy.Delete_management(temp_line)
    arcpy.Delete_management(temp_pts)

    

    
except Exception as e:
    print(e)
    
arcpy.GetMessages()






































