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


def main():
    df = pd.DataFrame(
        columns=[
            'x', 'y', 'cover_class', 'src_file'
        ] + BAND_COLUMNS
    )
    for fpath in glob.glob(TRAIN_GLOB):
        points = get_points_from_shapefile(fpath)
        # src_file = '16FEB12162517-M1BS-057380245010_01_P001.NTF'
        src_file = '16FEB12162517-M1BS-_RB_Rrs.tif'
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
        df = df.append(class_df)

    # === subset the results
    # exclude glint-free water
    pre_len = len(df)
    df = df.query('band7 >= 0.11')
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

    # === restructure bands for violinplot
    # ref: https://stackoverflow.com/a/46134162/1483986
    df = df.melt(
        var_name='band_n', value_name='pixel_value',
        id_vars=[tgt_key],
        value_vars=BAND_COLUMNS
    )
    # import pdb; pdb.set_trace()

    # assert subset didn't cut out all tgt_class==yes or ==no
    assert len(pd.unique(df[tgt_key])) == 2

    ax = sns.violinplot(
        data=df, x='band_n', y='pixel_value',
        hue=tgt_key,
        split=True
    )
    plt.show()
    plt.savefig(fname="subset_{}_bands.png".format(tgt_class.lower()))

if __name__ == "__main__":
    main()
