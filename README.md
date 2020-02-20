
Put shapefiles with Mike's transect ground truth data into `data`.
Run `python landcover_classify/shp_points_to_csv.py` to create `landclasses_master_pointlist.csv`.

`python -m landcover_classify.shapefile_points_to_master_rrs_csv images/tif_rrs_wv2/*` to add band values from image at all known points from shapefiles.
----------------------------------------------------------------------------

# Ground-truth Data Sources
## implemented:
* Mike's transects

## Not Yet Implemented:
* [FLUCCS data from SFWMD](https://geo-sfwmd.opendata.arcgis.com/datasets/d5d63afb753a4e0389f3a4641c8ae950_0)
* Mustang Island (& other?) LIDAR-based land classes

# TODO:
0. select area of tsne & plot onto spatial map

1. ~~add indicies (all possible indicies?)~~ (see note below)
   * normalized difference between band_n by band_n2
   * normalize band_n by average of all bands
   * band ratios
   * use all data to determine which indicies are most valuable & limit to those in the classifier
   * NOTE: Linear (and sometimes non-linear) relations between bands should be captured within a classifier, so these indicies would be redundant, *right*?


2. combine multiple binary classifications or one multiclass classifier?
    * possibly, but that requires another layer to summarize
    * multiple binary classifications with % chance of class are looking better and better

3. other classes out of .shp comments
    * which classes can we classify best?

4. wv2 decision tree for azure is ready soon from Matt

# Installing
```
# install pygdal
yum install -y gdal-devel
pip install pygdal=="`gdal-config --version`.*"'

# install other requirements
pip install -e .

# run tests to check installation
pytest --ignore images
```
