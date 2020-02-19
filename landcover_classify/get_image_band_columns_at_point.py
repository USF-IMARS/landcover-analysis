import pandas as pd

from landcover_classify.read_bands_at import read_bands_at

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
