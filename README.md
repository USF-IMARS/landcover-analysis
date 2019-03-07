# Ground-truth Data Sources
## implemented:
* Mike's transects

## Not Yet Implemented:
* [FLUCCS data from SFWMD](https://geo-sfwmd.opendata.arcgis.com/datasets/d5d63afb753a4e0389f3a4641c8ae950_0)
* Mustang Island (& other?) LIDAR-based land classes

# TODO:
0. select area of tsne & plot onto spatial map

1. add indicies (all possible indicies?)
   * normalized difference between band_n by band_n2
   * normalize band_n by average of all bands
   * band ratios
   * use all data to determine which indicies are most valuable & limit to those in the classifier

2. combine multiple binary classifications or one multiclass classifier?
    * possibly, but that requires another layer to summarize

3. other classes out of comments

4. wv2 decision tree for azure is ready soon from Matt
