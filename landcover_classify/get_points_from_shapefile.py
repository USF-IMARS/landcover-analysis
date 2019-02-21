from osgeo import osr
from osgeo import ogr


def get_points_from_shapefile(fpath):
    """
    Reads all points from shapefile and
    returns array of (lat,lon) pairs (EPSG 4326)
    """
    fname = fpath.split('/')[-1]
    print(" === ", fname)
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

    return points


def _get_points_from_shapefile_2(inputlayer):
    """
    alternate implementation
    """
    driver = ogr.GetDriverByName('ESRI Shapefile')
    # 0 means read-only, 1 means writeable
    dataSource = driver.Open(inputlayer, 0)
    layer = dataSource.GetLayer()
    sourceprj = layer.GetSpatialRef()
    targetprj = osr.SpatialReference()
    targetprj.ImportFromEPSG(4326)
    transform = osr.CoordinateTransformation(sourceprj, targetprj)
    transformed_coords = []
    # feature = layer.GetFeature(i)
    for feature in layer:
        # exported = json.loads(feature.ExportToJson())
        # print(exported['properties'].keys())
        transformed_coords.append(_doProjection(feature, transform))
    return transformed_coords


def _doProjection(feature, transform):
    pt = feature.GetGeometryRef()
    pt.Transform(transform)
    print("({}, {}),".format(pt.GetPoint()[0], pt.GetPoint()[1]))
    return pt.GetPoint()[0:2]
