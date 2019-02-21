"""test that we can open the .shp files"""

from osgeo import ogr, osr

import glob
import pprint
pp = pprint.PrettyPrinter(indent=4)


def doProjection(feature, transform):
    pt = feature.GetGeometryRef()
    pt.Transform(transform)
    print("({}, {}),".format(pt.GetPoint()[0], pt.GetPoint()[1]))
    return pt.GetPoint()[0:2]


def returnCoordSet(inputlayer):
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
        transformed_coords.append(doProjection(feature, transform))
    return transformed_coords


def open_test(fpath):
    # === projected points
    points = returnCoordSet(fpath)
    # pp.pprint(points)

    # === print layer fields
    source = ogr.Open(fpath)
    layer = source.GetLayer()
    field_names = [field.name for field in layer.schema]
    # pp.pprint(field_names)

    assert layer.GetLayerDefn().GetFieldCount() == len(layer.schema)
    assert layer.GetLayerDefn().GetFieldDefn(0).name == layer.schema[0].name

    # import fiona
    # shapes = fiona.open(fpath)
    # shapes.schema
    # shapes.schema['properties'].keys()
    # # first feature
    # shapes.next()

    # import geopandas as gpd
    # shapes = gpd.read_file(fpath)
    # list(shapes.columns.values)
    # # first features
    # shapes.head(3)

    n_features = layer.GetFeatureCount()
    assert len(points) == n_features
    n_fields = len(field_names)
    print("{} features x {} fields".format(
        n_features, n_fields
    ))
    return n_features, n_fields


def test_open_all_train_files():
    for fpath in glob.glob('data/GTPs_touse_points_*_train.shp'):
        fname = fpath.split('/')[-1]
        print(" === ", fname)
        cover_class = fname.split("points_")[1].split("_train")[0]
        print(cover_class)
        open_test(fpath)
