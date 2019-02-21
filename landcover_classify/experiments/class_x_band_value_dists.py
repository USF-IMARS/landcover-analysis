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
TEST_GLOB = 'data/GTPs_touse_points_*_test.shp'


def main():
    train_df = pd.DataFrame(
        columns=['band_n', 'pixel_value', 'x', 'y', 'cover_class', 'ntf']
    )
    for fpath in glob.glob(TRAIN_GLOB):
        points = get_points_from_shapefile(fpath)
        # ntf_path = '16FEB12162517-M1BS-057380245010_01_P001.NTF'
        ntf_path = '16FEB12162517-M1BS-_RB_Rrs.tif'
        df = read_bands_at(ntf_path, points, longformat=True)
        cover_class = fpath.split("use_points_")[1].split("_t")[0]
        df['cover_class'] = cover_class
        df['ntf'] = ntf_path
        train_df = train_df.append(df)

    ax = sns.violinplot(
        data=train_df, x='cover_class', y='pixel_value', hue='band_n',
        split=False
    )
    plt.show()

if __name__ == "__main__":
    main()
