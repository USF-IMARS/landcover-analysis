
from datetime import datetime

from osgeo import gdal
import imars_etl


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
    fpath = imars_etl.extract(
        sql="product_id in ({})".format(WV2_M_ID),
        post_where="ORDER BY abs(TIMESTAMPDIFF("
        "   second, datetimefield, '2014-12-10 09:45:00'))"
        "LIMIT 1"
    )
    # === open the file & get the pixel values at this pixel
    ds = gdal.Open(fpath)
    # get georeference info
    transform = ds.GetGeoTransform()
    xOrigin = transform[0]
    yOrigin = transform[3]
    pixelWidth = transform[1]
    pixelHeight = transform[5]
    band = ds.GetRasterBand(1)  # 1-based index
    data = band.ReadAsArray()
    # loop through the coordinates
    band_values = []
    for point in points:
        x = point[0]
        y = point[1]

        xOffset = int((x - xOrigin) / pixelWidth)
        yOffset = int((y - yOrigin) / pixelHeight)
        print(xOffset)
        print(yOffset)
        # get individual pixel values
        value = data[yOffset][xOffset]
        print(value)
        band_values.append(value)

    return band_values


bandvals = get_pixel_bands(datetime(2017, 1, 1), [(26, -81.7)])
print(bandvals)
