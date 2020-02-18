"""2d histogram plot """
import numpy  # segfault unless this is here? WEIRD.
from osgeo import gdal
from osgeo import ogr
from osgeo import osr
# import geotiler  # requires py 3.6+
import rasterio
from rasterio.plot import show  # attributeError without this?
import matplotlib.pyplot as plt
from matplotlib.ticker import NullFormatter
import glob
import pprint
pp = pprint.PrettyPrinter(indent=4)
# assert plotly.__version__ > '2.0.2'
img_path = '16FEB12162517-M1BS-_RB_Rrs.tiff'

nullfmt = NullFormatter()         # no labels

# start with a rectangular Figure
plt.figure(1, figsize=(8, 8))


# === plot points
print("reading data")
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
    x = []
    y = []
    z = []
    for feature in layer:
        pt = feature.GetGeometryRef()
        pt.Transform(transform)
        lat, lon, alt = pt.GetPoint()
        x.append(lat)
        y.append(lon)
        z.append(alt)
    axis = plt.scatter(
        x, y,
        marker='+', linewidth=1,
        label="{:03}:{}".format(len(x), cover_class), zorder=1
    )


# === plot image raster
print('reading image...')
# img = gdal.Open(img_path).ReadAsArray()
# axis = plt.gca()
with rasterio.open(img_path) as img:
    with rasterio.vrt.WarpedVRT(
        img, crs='epsg:4326', resampling=rasterio.enums.Resampling.bilinear
    ) as vrt:
        print('drawing image...')
        axis = show(
            img, title='???', ax=axis, zorder=2
        )
        # plt.imshow(vrt)
# plt.imshow(img[0, :, :])  # shows just first of the 8 bands

print("showing plot...")
plt.show()
