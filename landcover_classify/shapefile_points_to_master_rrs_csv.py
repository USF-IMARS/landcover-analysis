"""
Reads points from all shapefiles and given image to create csv dataframe.
"""
import sys
import glob
import pandas as pd

from landcover_classify.get_points_from_shapefile \
    import get_points_from_shapefile
from landcover_classify.get_image_band_columns_at_point \
    import get_image_band_columns_at_point

SHAPEFILE_GLOB = 'data/GTPs_touse_points_*.shp'
BAND_COLUMNS = ['band'+str(n) for n in range(8)]  # band0, band1, etc
DATAFRAME_FILE = "master_dataframe_rrs.csv"


def main(tif_files):
    # open df to append to or create new
    try:
        df = pd.read_csv(DATAFRAME_FILE)
    except FileNotFoundError:  # TODO catch file read error, not AssertionError
        df = pd.DataFrame(
            columns=[
                'x', 'y', 'cover_class', 'src_file'
            ] + BAND_COLUMNS
        )
    shp_files = glob.glob(SHAPEFILE_GLOB)
    print('inspecting {} .shp and {} .tif files'.format(
        len(shp_files), len(tif_files)
    ))
    for fpath in shp_files:
        points = get_points_from_shapefile(fpath)
        for src_file in tif_files:
            class_df = get_image_band_columns_at_point(src_file, points, fpath)
            if class_df is not None:
                print('points being added to dataFrame')
                df = df.append(class_df)
            # else point is outside of image

    df.drop_duplicates().reset_index(drop=True)
    df.to_csv(DATAFRAME_FILE)


if __name__ == "__main__":
    # === images passed in from CLI
    for fileglob in sys.argv[1:]:
        image_files = glob.glob(
            fileglob
        )
        main(image_files)

    # === images read from hardcoded list
    # from landcover_classify.image_list import IMAGE_LIST
    # for imagepath in IMAGE_LIST:
    #     try:
    #         fullpath = "images/tif_r_rs_wv2/" + imagepath
    #         print(" === === " + fullpath)
    #         main(fullpath)
    #     except AssertionError as err:
    #         print(err)
