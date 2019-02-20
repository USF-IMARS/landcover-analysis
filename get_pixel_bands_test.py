"""
Tries to open up a .ntf file and fetch some pixel values.
"""

from datetime import datetime
import pprint
import glob
import matplotlib.pyplot as plt

import seaborn as sns
import numpy as np
from osgeo import osr
from osgeo import ogr
# import imars_etl

from landcover_classify.read_bands_at import read_bands_at

pp = pprint.PrettyPrinter(indent=4)

dt = datetime(2014, 12, 10, 9, 45)
# === extract the nearest ntf
# TODO: add area_id to limit # images
# M1BS (multispectral)
WV2_M_ID = 11
# WV3_M_ID = "TODO"
# # P1BS (panspectral)
# WV2_P_ID = 24
# WV3_P_ID = "TODO"
# TODO: use datetime in this query
# MySQL get nearest date; ref: https://stackoverflow.com/a/27401431/1483986
# fpath = imars_etl.extract(
#     sql="product_id in ({})".format(WV2_M_ID) +
#     "ORDER BY abs(TIMESTAMPDIFF("
#     "   second, date_time, '2014-12-10 09:45:00'))"
#     "LIMIT 1"
# )
# manually set filepath for now:
fpath = "16FEB12162517-M1BS-057380245010_01_P001.NTF"

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

    points = []
    for feature in layer:
        pt = feature.GetGeometryRef()
        pt.Transform(transform)
        lat, lon, alt = pt.GetPoint()
        points.append((lat, lon))

bandvals = read_bands_at(
    fpath,
    points
)
# pp.pprint(bandvals)
# === remove nan rows
pre_len = len(bandvals)
bandvals = bandvals[~np.isnan(bandvals).any(axis=1)]
print("{} valid values found (was {:2.2f}% NaNs)".format(
    len(bandvals),
    100 - 100*len(bandvals)/pre_len
))

# === save output
np.savetxt("filepath_dt_all_matrix.csv", bandvals, delimiter=",")

ax = sns.violinplot(data=bandvals, split=True)
plt.show()
