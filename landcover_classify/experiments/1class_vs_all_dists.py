"""
compares training set band value distributions with test set

inputs
---------------
TRAIN_GLOB : glob str
    glob string selecting multiple .shp shapefiles
ntf_path : filepath
    
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
ntf_path = '16FEB12162517-M1BS-057380245010_01_P001.NTF'


def main():
    df = pd.DataFrame(
        columns=['band_n', 'pixel_value', 'x', 'y', 'cover_class', 'ntf']
    )
    for fpath in glob.glob(TRAIN_GLOB):
        points = get_points_from_shapefile(fpath)
        # ntf_path = '16FEB12162517-M1BS-_RB_Rrs.tif'
        class_df = read_bands_at(ntf_path, points, longformat=True)
        cover_class = fpath.split("use_points_")[1].split("_t")[0]
        class_df['cover_class'] = cover_class
        class_df['ntf'] = ntf_path
        df = df.append(class_df)

    # === restructure cover_class into is_tgt_class true/false
    # ['Water', 'Mangrove']
    tgt_class = 'Water'
    tgt_key = 'is_' + tgt_class.lower()
    df = df.rename(index=str, columns={'cover_class': tgt_key})
    df[tgt_key].loc[df[tgt_key] == tgt_class] = 'yes'
    df[tgt_key].loc[df[tgt_key] != 'yes'] = 'no'

    ax = sns.violinplot(
        data=df, x='band_n', y='pixel_value',
        hue=tgt_key,
        split=True
    )
    # plt.show()
    plt.savefig(fname="1vall_{}_bands.png".format(tgt_class.lower()))

if __name__ == "__main__":
    main()
