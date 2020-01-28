"""
compares training set band value distributions with test set
"""

import glob

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from landcover_classify.get_points_from_shapefile \
    import get_points_from_shapefile
from landcover_classify.read_bands_at \
    import read_bands_at

TRAIN_GLOB = 'data/GTPs_touse_points_*_train.shp'
BAND_COLUMNS = ['band'+str(n) for n in range(8)]  # band0, band1, etc


def get_image_band_columns_at_point(src_file, points, fpath):
    band_arry = read_bands_at(src_file, points, longformat=False)
    class_df = pd.DataFrame(
        band_arry,
        columns=BAND_COLUMNS
    )
    class_df['x'] = [p[0] for p in points]
    class_df['y'] = [p[1] for p in points]
    cover_class = fpath.split("use_points_")[1].split("_t")[0]
    class_df['cover_class'] = cover_class
    class_df['src_file'] = src_file
    return class_df


def main(tif_files):
    df = pd.DataFrame(
        columns=[
            'x', 'y', 'cover_class', 'src_file'
        ] + BAND_COLUMNS
    )
    shp_files = glob.glob(TRAIN_GLOB)
    print('inspecting {} .shp and {} .tif files'.format(
        len(shp_files), len(tif_files)
    ))
    for fpath in shp_files:
        points = get_points_from_shapefile(fpath)
        for src_file in tif_files:
            class_df = get_image_band_columns_at_point(src_file, points, fpath)
            df = df.append(class_df)

    df.to_csv("master_dataframe_rrs.csv")

    # === subset the results
    # exclude glint-free water
    pre_len = len(df)
    df = df.query('band7 >= 0.11')
    if pre_len > 0:
        print("{}/{} rows match subset ({:2.1f}%)".format(
            len(df),
            pre_len,
            100*len(df)/pre_len
        ))

    # === restructure cover_class into is_tgt_class true/false
    # ['Water', 'Mangrove']
    tgt_class = 'Mangrove'
    tgt_key = 'is_' + tgt_class.lower()
    df = df.rename(index=str, columns={'cover_class': tgt_key})
    df[tgt_key].loc[df[tgt_key] == tgt_class] = 'yes'
    df[tgt_key].loc[df[tgt_key] != 'yes'] = 'no'

    df.to_csv("{}_rrs.csv".format(tgt_key))

    # === restructure bands for violinplot
    # ref: https://stackoverflow.com/a/46134162/1483986
    df = df.melt(
        var_name='band_n', value_name='pixel_value',
        id_vars=[tgt_key],
        value_vars=BAND_COLUMNS
    )
    # assert subset didn't cut out all tgt_class==yes or ==no
    assert len(pd.unique(df[tgt_key])) == 2

    sns.violinplot(
        data=df, x='band_n', y='pixel_value',
        hue=tgt_key,
        split=True
    )
    plt.show()
    plt.savefig(fname="subset_{}_bands_rrs.png".format(
        tgt_class.lower()
    ))


if __name__ == "__main__":
    image_files = glob.glob(
        '16FEB12162517-M1BS-_RB_Rrs.tiff'
        # 'images/tif_rrs_wv2/wv2_rrs_201803*.tif'
        # 'wv2_Rrs_20161026T150644.tif'
        # '16FEB12162517-M1BS-057380245010_01_P001.NTF'
    )
    main(image_files)
