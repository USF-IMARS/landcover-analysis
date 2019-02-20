
from datetime import datetime
import pprint
import glob
from math import sqrt

import numpy as np
from osgeo import gdal
from osgeo import osr
from osgeo import ogr
import imars_etl

pp = pprint.PrettyPrinter(indent=4)


def get_pixel_bands(datetime, points):
    """
    fetch image and return bands.

    parameters
    ----------
    points: list of tuples
        [(lat, lon), (lat, lon)] points to extract band values

    returns
    -------
    band_values : list of lists
        [[band1, band2], [band1, band2]] band values for each point requested
        list returned is in same order as points.

    TODO: this could be optimized by passing in all dates, lats, lons
          at same time so we avoid possible re-extracting of images.
    """
    # === extract the nearest ntf
    # TODO: add area_id to limit # images
    # M1BS (multispectral)
    WV2_M_ID = 11
    # WV3_M_ID = "TODO"
    # # P1BS (panspectral)
    # WV2_P_ID = 24
    # WV3_P_ID = "TODO"
    # TODO: use datetime in this query
    fpath = "16FEB12162517-M1BS-057380245010_01_P001.NTF"
    # MySQL get nearest date; ref: https://stackoverflow.com/a/27401431/1483986
    # fpath = imars_etl.extract(
    #     sql="product_id in ({})".format(WV2_M_ID) +
    #     "ORDER BY abs(TIMESTAMPDIFF("
    #     "   second, date_time, '2014-12-10 09:45:00'))"
    #     "LIMIT 1"
    # )
    # === open the file & get the pixel values at this pixel
    ds = gdal.Open(fpath)
    # get georeference info
    # === assert transform is null?
    print("pre-calc-geo:")
    print(ds.GetGeoTransform())
    # assert ds.GetGeoTransform() == [0.0, 1.0, 0.0, 0.0, 0.0, 1.0]
    src_s_ref = osr.SpatialReference(wkt=ds.GetProjection())
    assert src_s_ref.IsProjected() == 0
    assert src_s_ref.GetAttrValue('geogcs') is None
    assert src_s_ref.ExportToWkt() == ''
    gcps = ds.GetGCPs()
    # assert that this:
    # gcp_transform = osr.CoordinateTransformation(gcp_s_ref, src_s_ref)
    # throws :
    # ERROR 6: No translation for an empty SRS to PROJ.4 format is known.
    # === set up the transform manually using ground control points
    gcp_s_ref = osr.SpatialReference(wkt=ds.GetGCPProjection())

    # assume control points are corners
    assert len(gcps) == 4
    assert gcps[0].Id == 'UpperLeft'
    p1 = gcps[0]
    assert gcps[2].Id == 'LowerRight'
    p2 = gcps[2]
    # x_0 = y_0 = z_0 = 0
    # x_f = y_f = z_f = 0
    # for gcp in control_points:
    #     print("{}=({},{},{})".format(gcp.Id, gcp.GCPX, gcp.GCPY, gcp.GCPZ))
    #     x_0 = min(gcp.GCPX, x_0)
    #     y_0 = min(gcp.GCPY, y_0)
    #     z_0 = min(gcp.GCPZ, z_0)
    #     x_f = max(gcp.GCPX, x_f)
    #     y_f = max(gcp.GCPY, y_f)
    #     z_f = max(gcp.GCPZ, z_f)
    #     px_x = gcp.GCPPixel
    #     px_y = gcp.GCPLine
    # x_range = x_f - x_0
    # y_range = y_f - y_0
    # x_res = x_range / ds.RasterXSize
    # y_res = y_range / ds.RasterYSize
    # x_skew = sqrt(x_range**2 + y_range**2) / y_res  # geo_distance / ypixel
    # y_skew = sqrt(x_range**2 + y_range**2) / x_res  # geo_distance / xpixel
    # https://stackoverflow.com/questions/27166739/description-of-parameters-of-gdal-setgeotransform
    x_skew = (
        sqrt((p1.GCPX-p2.GCPX)**2 + (p1.GCPY-p2.GCPY)**2) /
        (p1.GCPLine - p2.GCPLine)
    )
    y_skew = (
        sqrt((p1.GCPX-p2.GCPX)**2 + (p1.GCPY-p2.GCPY)**2) /
        (p1.GCPPixel - p2.GCPPixel)
    )
    x_res = (p2.GCPX - p1.GCPX) / ds.RasterXSize
    y_res = (p2.GCPY - p1.GCPY) / ds.RasterYSize
    ds.SetGeoTransform([
        p1.GCPX,
        x_res,
        x_skew,
        p1.GCPY,
        y_skew,
        y_res,
    ])
    print("post-calc-geo:")
    print(ds.GetGeoTransform())
    # assert ds.GetGeoTransform() == [
    #     p1.GCPX,
    #     x_res,
    #     x_skew,
    #     p1.GCPY,
    #     y_skew,
    #     y_res,
    # ]
    (
        xOrigin, pixelWidth, xskew, yOrigin, yskew, pixelHeight
    ) = ds.GetGeoTransform()
    print("{} @ {},{} px={}x{}".format(
        fpath, xOrigin, yOrigin, pixelWidth, pixelHeight
    ))
    band_values = np.array([[float('nan')]*ds.RasterCount]*len(points))
    for band_n in range(ds.RasterCount):
        band = ds.GetRasterBand(band_n+1)  # 1-based index
        data = band.ReadAsArray()
        # loop through the coordinates
        for point_n, point in enumerate(points):
            x = point[0]
            y = point[1]
            # print("reading @ {},{}".format(x, y))
            xOffset = int((x - xOrigin) / pixelWidth)
            yOffset = int((y - yOrigin) / pixelHeight)

            # get individual pixel values
            try:
                value = data[yOffset][xOffset]
                print("band {} {},{} (point#{})= {}".format(
                    band_n, xOffset, yOffset, point_n, value
                ))
                band_values[point_n, band_n] = value
            except IndexError:
                print("point {},{} is out-of-image".format(yOffset, xOffset))

    return band_values

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

bandvals = get_pixel_bands(
    datetime(2017, 1, 1),
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
np.savetxt("filepath_dt_all.csv", bandvals, delimiter=",")
# import pdb; pdb.set_trace()
