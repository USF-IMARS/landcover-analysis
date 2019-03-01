"""open all "train" .shp files and write x,y,z,class to csv file"""
import glob

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
        df = df.append({
            "lat": lat, "lon": lon, "alt": alt, "cover_class": cover_class
        }, ignore_index=True)
        n_pts += 1
    print("{} pts added.".format(n_pts))
df.to_csv("landclasses_master_pointlist.csv")
