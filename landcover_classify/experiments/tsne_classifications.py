"""
t-distributed Stochastic Neighbor Embedding (t-SNE) visualization of classes
in hyperplane.

Based on: https://blog.applied.ai/visualising-high-dimensional-data/
"""
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE
import seaborn as sns
from sklearn.preprocessing import StandardScaler


print(__doc__)

BAND_COLUMNS = ['band'+str(n) for n in range(8)]  # band0, band1, etc
h = .02  # step size in the mesh
NTF_OR_RRS = "ntf"


def main():
    # master_dataframe_ is exported by class_subset_vs_all_dists
    df = pd.read_csv('master_dataframe_{}.csv'.format(NTF_OR_RRS))
    df = df.dropna()

    tsne = TSNE(
        n_components=2, random_state=0,
        perplexity=30  # should be ~ size of smallest expected cluster
    )
    dfsvd = df[BAND_COLUMNS]
    print(dfsvd.shape)
    print("building tsne using :")
    print(dfsvd.head())

    # TODO: should we scale here or use raw values?
    X = StandardScaler().fit_transform(dfsvd.values)
    # X = dfsvd.values
    Z = tsne.fit_transform(X)
    dftsne = pd.DataFrame(Z, columns=['x', 'y'], index=dfsvd.index)
    dftsne['class'] = df['cover_class']
    g = sns.lmplot(
        'x', 'y', dftsne, hue='class', fit_reg=False, size=8,
        scatter_kws={'alpha': 0.7, 's': 60}
    )
    g.axes.flat[0].set_title(
        'Scatterplot of dataset reduced to 2D using t-SNE'
    )

    plt.show()


if __name__ == "__main__":
    main()
