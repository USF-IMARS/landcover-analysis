"""2d histogram plot """
import numpy as np
from osgeo import ogr
from osgeo import osr
# import geotiler  # requires py 3.6+

import matplotlib.pyplot as plt
from matplotlib.ticker import NullFormatter
import glob
import pprint
pp = pprint.PrettyPrinter(indent=4)
# assert plotly.__version__ > '2.0.2'

nullfmt = NullFormatter()         # no labels

# definitions for the axes
left, width = 0.1, 0.65
bottom, height = 0.1, 0.65
bottom_h = left_h = left + width + 0.02

rect_scatter = [left, bottom, width, height]
rect_histx = [left, bottom_h, width, 0.2]
rect_histy = [left_h, bottom, 0.2, height]

# start with a rectangular Figure
plt.figure(1, figsize=(8, 8))

axScatter = plt.axes(rect_scatter)
axHistx = plt.axes(rect_histx)
axHisty = plt.axes(rect_histy)

# no labels
axHistx.xaxis.set_major_formatter(nullfmt)
axHisty.yaxis.set_major_formatter(nullfmt)


print("reading data")
all_x = []
all_y = []
all_z = []
for fpath in glob.glob('data/GTPs_touse_points_*_test.shp'):
    fname = fpath.split('/')[-1]
    print(" === ", fname)
    cover_class = fname.split("points_")[1].split("_test")[0]

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
    all_x.append(x)
    all_y.append(y)
    all_z.append(z)
    axScatter.scatter(
        x, y,
        marker='+', linewidth=1,
        label="{:03}:{}".format(len(x), cover_class)
    )

print("squashing ")
X = np.array([inner for outer in all_x for inner in outer])
Y = np.array([inner for outer in all_y for inner in outer])

print("determining nice limits by hand...")
binwidth = 0.25
xymax = np.max([np.max(np.fabs(X)), np.max(np.fabs(Y))])
lim = (int(xymax/binwidth) + 1) * binwidth
bins = np.arange(-lim, lim + binwidth, binwidth)
xbins = bins
ybins = bins

print("determining nice limits w/ numpy...")
H, xedges, yedges = np.histogram2d(
    X, Y,
    # weights=???,
    # bins=(10, 10)
)

# print("{} \n\tvs \n{}".format(xbins, xedges))
print(H)

for i in range(len(all_x)):
    x = all_x[i]
    y = all_y[i]
    axHistx.hist(
        x, bins=xedges, histtype='bar', stacked=True
    )
    axHisty.hist(
        y, bins=yedges, histtype='bar', stacked=True,
        orientation='horizontal',
    )

axScatter.legend(fontsize='small')

axHistx.set_xlim(axScatter.get_xlim())
axHisty.set_ylim(axScatter.get_ylim())

# print("adding histogram heatmap")
# # axScatter.imshow(
# #     H, interpolation='nearest', origin='low',
# #     extent=[xedges[0], xedges[-1], yedges[0], yedges[-1]]
# # )
#
# im = mpl.image.NonUniformImage(axScatter, interpolation='bilinear')
# xcenters = (xedges[:-1] + xedges[1:]) / 2
# ycenters = (yedges[:-1] + yedges[1:]) / 2
# im.set_data(xcenters, ycenters, H)
# axScatter.images.append(im)

# download background map using OpenStreetMap
# https://wrobell.dcmod.org/geotiler/usage.html#matplotlib-example
# x_left, x_right = axScatter.get_xlim()
# y_top, y_bottom = axScatter.get_ylim()
# mm = geotiler.Map(
#     extent=(x_left, y_bottom, x_right, y_top),
#     # zoom=18
# )
# img = geotiler.render_map(mm)
# axScatter.imshow(img)
#
#
print("showing plot...")
plt.show()
