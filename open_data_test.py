"""test that we can open the .shp files"""

from osgeo import ogr

from landcover_classify.get_points_from_shapefile \
    import get_points_from_shapefile

import glob
import pprint
pp = pprint.PrettyPrinter(indent=4)


def open_test(fpath):
    # === projected points
    points = get_points_from_shapefile(fpath)
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
