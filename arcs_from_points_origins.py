import arcpy
import math
import os
import numpy as np
from arcpy import env


arcpy.env.overwriteOutput = True

pts = arcpy.GetParameterAsText(0)
fence_id = arcpy.GetParameterAsText(1)
origin_pts = arcpy.GetParameterAsText(2)
orig_id = arcpy.GetParameterAsText(3)
full = arcpy.GetParameterAsText(4)
crad = float(arcpy.GetParameterAsText(5))
arc_length = float(arcpy.GetParameterAsText(6))

spatial_ref = arcpy.Describe(pts).spatialReference

fields = ["OBJECTID", "SHAPE", "SHAPE@X", "SHAPE@Y", fence_id]
o_fields = ["OBJECTID", "SHAPE@X", "SHAPE@Y", orig_id]
outpath = "C:/Users/lukepc/on_board_bear_files/arc_files/build_fence_lines/Whistler_main.gdb"
outname = "test"
outlines = outpath + "/testlines"
temp_line = "temp_line_file"

if(arc_length > ( 2 * math.pi * crad )):
   print("Error: Desired arc length is longer than circumference of circle defined by radius.")
    

try: 
    arcpy.CreateFeatureclass_management(outpath, outname, "POINT", spatial_reference = spatial_ref)
    arcpy.AddField_management(outname, "ID", "TEXT", field_length = 50)
    arcpy.AddField_management(outname, "orderfield", "SHORT", field_length = 10)
    

    with arcpy.da.SearchCursor(origin_pts, o_fields) as o_cursor:
        for orow in o_cursor:
            print("Row: " + str(orow))
            x0 = orow[1]
            y0 = orow[2]
            o_id = orow[3]
            print(x0)
            print(y0)
            print(o_id)
            with arcpy.da.SearchCursor(pts, fields) as cursor:
                for row in cursor:
                    print(row[0])
                    f_id = row[4]
                    objid = row[0]
                    x1 = row[2]
                    y1 = row[3]

                    if o_id == f_id:
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

    arcpy.Delete_management("test")
    arcpy.Delete_management(temp_line)   

    
except Exception as e:
    print(e)
    
arcpy.GetMessages()
























