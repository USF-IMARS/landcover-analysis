"""open all "train" .shp files and write x,y,z,class to csv file"""
import glob
from datetime import datetime

import pandas as pd
from osgeo import osr
from osgeo import ogr


print("reading data")
df = pd.DataFrame(columns=['lat', 'lon', 'alt', 'cover_class'])
for fpath in glob.glob('data/GTPs_touse_points_*_train.shp'):
    fname = fpath.split('/')[-1]
    print(" === ", fname)
    cover_class = fname.split("points_")[1].split("_train")[0]

    source = ogr.Open(fpath)
    layer = source.GetLayer()
    sourceprj = layer.GetSpatialRef()
    targetprj = osr.SpatialReference()
    targetprj.ImportFromEPSG(4326)
    transform = osr.CoordinateTransformation(sourceprj, targetprj)
    n_pts = 0
    for feature in layer:
        pt = feature.GetGeometryRef()
        pt.Transform(transform)
        lat, lon, alt = pt.GetPoint()
        date_field = feature.GetFieldAsDateTime('DATE_')
        month = date_field[1]
        if month > 12 or month < 1:
            month = 'NA'
        # Others that might be intersting:
        # feature.GetFeature('CERP_Class')
        # feature.GetFeature('SC_Class')
        # also the species-specific counts (but all I see is 0 and null)
        df = df.append({
            "lat": lat, "lon": lon, "alt": alt, "cover_class": cover_class,
            "month": month
        }, ignore_index=True)
        n_pts += 1
    print("{} pts added.".format(n_pts))
df.to_csv("landclasses_master_pointlist.csv")
