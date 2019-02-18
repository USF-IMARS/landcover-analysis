
from datetime import datetime
import pprint

from osgeo import gdal
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
    # M1BS (multispectral)
    WV2_M_ID = 11
    # WV3_M_ID = "TODO"
    # # P1BS (panspectral)
    # WV2_P_ID = 24
    # WV3_P_ID = "TODO"
    # TODO: use datetime in this query
    fpath = "WV02_20141213163945_103001003B641400_14DEC13163945-M1BS-500534941090_01_P001.ntf"
    # fpath = imars_etl.extract(
    #     sql="product_id in ({})".format(WV2_M_ID) +
    #     "ORDER BY abs(TIMESTAMPDIFF("
    #     "   second, date_time, '2014-12-10 09:45:00'))"
    #     "LIMIT 1"
    # )
    # === open the file & get the pixel values at this pixel
    ds = gdal.Open(fpath)
    # get georeference info
    transform = ds.GetGeoTransform()
    xOrigin = transform[0]
    yOrigin = transform[3]
    pixelWidth = transform[1]
    pixelHeight = transform[5]
    print("file @ {},{} px={}x{}".format(
        xOrigin, yOrigin, pixelWidth, pixelHeight
    ))
    band_values = [[0]*ds.RasterCount]*len(points)
    for band_n in range(ds.RasterCount):
        band = ds.GetRasterBand(band_n+1)  # 1-based index
        data = band.ReadAsArray()
        # loop through the coordinates
        for point_n, point in enumerate(points):
            x = point[0]
            y = point[1]

            xOffset = int((x - xOrigin) / pixelWidth)
            yOffset = int((y - yOrigin) / pixelHeight)

            # get individual pixel values
            value = data[yOffset][xOffset]
            print("band {} {},{} = {}".format(band_n, xOffset, yOffset, value))
            band_values[point_n][band_n] = value
    return band_values


bandvals = get_pixel_bands(
    datetime(2017, 1, 1),
    [(26, -81.7), (26, -81.6)]
)
pp.pprint(bandvals)
