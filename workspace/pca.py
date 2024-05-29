import pandas as pd
import numpy as np

from sklearn.decomposition import PCA

dataset = "../data/parent/wakeup_NewDenC.csv"
data = pd.read_csv(dataset)

"""
def main():
    num_components = min(data.shape[0], data.shape[1])

    # perform PCA
    pca = PCA(n_components=num_components)
    pca.fit(data)

    loadings = pca.components_.T * np.sqrt(pca.explained_variance_)

    df_loadings = pd.DataFrame(loadings, columns=[f'PC{i}' for i in range(1, num_components + 1)], index=data.columns)

    new_df = pd.DataFrame()

    for i in range(1, 21):
        print(f"PC{i}")

        loading = df_loadings[f'PC{i}'].sort_values(ascending=False).to_frame()
        print(loading)

        # get the first 10 rows and the last 10 rows
        top_10 = loading.head(10)
        bottom_10 = loading.tail(10)

        new_df = pd.concat([new_df, top_10, bottom_10])

        # add it to the new DataFrame
        print(new_df)

    new_df.to_csv("../data/parent/PCA.csv")
"""

def main():
    master_ds = pd.read_csv("../data/parent/wakeup_NewDenC.csv")
    genes_to_keep = pd.read_csv("../data/generated/Top10Genes.csv")

    genes_to_keep = genes_to_keep["Gene"].tolist()


if __name__ == "__main__":
    main()
