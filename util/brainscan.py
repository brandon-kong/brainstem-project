# PY_MLBrainScan
# Colin Buenvenida


# Importing global packages
import pandas as pd
import matplotlib.pyplot as plt
import statistics
from sklearn.cluster import KMeans
import numpy as np

# # Matplotlib backend update to create interactive plot
# import matplotlib
# matplotlib.use('TkAgg')


def brainScan():
    """
    Of 4 possible ML_Brainstem data frames (created by PY_MLBrainSurgeon's brainOp() function),
    loads a user-specified frame and performs a categorical/binning analysis.

    :return: Binning results of user-specified data frame, either in the form of a table or a chart, depending on the
    given data frame's type (DEN vs INT)
    """

    # User greeting:
    print("Hi Colin! This is brainScan(). \nWhat data frame are we working on today?", "\n")
    print("1: DEN_Coronal")
    print("2: INT_Coronal")
    print("3: DEN_Sagittal")
    print("4: INT_Sagittal")
    print("5: OTHER", "\n")

    # Data frame selection
    try:
        user_select = int(input("What dataframe?: "))
    except ValueError:
        print("Invalid input. Please enter a number, 1 through 4.")

    # Assigning data frame and file path
    if user_select == 1:
        filePath = "nu_brain_NewDenC.csv"
    elif user_select == 2:
        filePath = "nu_brain_NewIntC.csv"
    elif user_select == 3:
        filePath = "nu_brain_NewDenS.csv"
    elif user_select == 4:
        filePath = "nu_brain_NewIntS.csv"
    elif user_select == 5:
        filePath = input("What data set would you like to analyze?: ")
    else:
        print("Invalid option. Please select a number between 1 and 5.")

    # Reading CSV file
    df = pd.read_csv(filePath, header=1, float_precision='high')

    # Protocol 1: DENSITY ANALYSIS
    if user_select in [1, 3, 5]:
        # Initializing accumulators
        counterList1 = 0  # 0 to 0.000001
        counterList2 = 0  # 0.000001 to 0.00001
        counterList3 = 0  # 0.00001 to 0.0001
        counterList4 = 0  # 0.0001 to 0.001
        counterList5 = 0  # 0.001 to 0.01
        counterList6 = 0  # 0.01 to 0.1
        counterList7 = 0  # 0.1 and greater
        counterList8 = 0  # -1
        counterList9 = 0  # gene labels?

        # Kaiwen add-in --> Will keep track of the actual values that range between 0.001 and 0.002
        counterList10 = []

        # Checking if values are within specified ranges
        for row in df.values:
            for value in row:
                try:
                    num_value = float(value)
                    if 0 <= num_value < 0.000001:
                        counterList1 += 1
                    elif 0.000001 <= num_value < 0.00001:
                        counterList2 += 1
                    elif 0.00001 <= num_value < 0.0001:
                        counterList3 += 1
                    elif 0.0001 <= num_value < 0.001:
                        counterList4 += 1
                    elif 0.001 <= num_value < 0.01:
                        counterList5 += 1
                        # Kaiwen add-in
                        if num_value <= 0.002:
                            counterList10.append(num_value)
                    elif 0.01 <= num_value < 0.1:
                        counterList6 += 1
                    elif num_value >= 0.1:
                        counterList7 += 1
                    elif 0 > num_value >= -1:
                        counterList8 += 1
                except ValueError:  # Handling cases where the value cannot be converted to a number (i.e. gene names)
                    print(f"Error converting value to number: {value}")
                    counterList9 += 1
                    pass

        print("\n\n\n-- Binning Analysis --")
        print("\n0 to 0.000001: ", counterList1)
        print("0.000001 to 0.00001: ", counterList2)
        print("0.00001 to 0.0001: ", counterList3)
        print("0.0001 to 0.001: ", counterList4)
        print("0.001 to 0.01: ", counterList5)
        print("0.01 to 0.1: ", counterList6)
        print("0.1 and greater: ", counterList7)

        print("\nKaiwen's Add-In:")
        print("0.001 to 0.002: ", len(counterList10))
        print(f"Average Expression Value: {statistics.mean(counterList10)}")

        print("\n")

        print("-1 (fully inactive): ", counterList8)
        print("Error cases / gene names: ", counterList9)
        print(f"Total entries in DataFrame: {df.size}")

        print("\n")

        print("Minimum value: ", df.values.min())
        print("Maximum values: ", df.values.max())

        # Generating a bar chart for the bin counts
        bins = ['0 to 0.000001', '0.000001 to 0.00001', '0.00001 to 0.0001', '0.0001 to 0.001', '0.001 to 0.01',
                '0.01 to 0.1', '0.1 and greater']
        bin_counts = [counterList1, counterList2, counterList3, counterList4, counterList5, counterList6, counterList7]

        plt.bar(bins, bin_counts)
        plt.xlabel(bins)
        plt.ylabel('Count')
        plt.title('Distribution of Gene Expression Bins')
        plt.show()  # Showcasing the generated chart

    # Protocol 2: INTENSITY ANALYSIS
    elif user_select in [2, 4]:
        # Generating a histogram
        plt.hist(df.values.flatten(), bins=30, edgecolor='black')
        plt.xlabel('Values')
        plt.ylabel('Frequency')
        plt.title('Histogram of Gene Expression Values')
        plt.show()

    ############################################################
    """
    THE JACOB SPECIAL:
    Running k-means clustering on the selected dataset in 4, 6, 8, and 13 initial clusters,
    then displaying centroids as vertical lines across a general histogram
    """

    print("\n\nTHE JACOB SPECIAL: Running k-means clustering on the selected dataset in 4, 6, 8, and 13 initial"
          "clusters, then displaying centroids as vertical lines across a general histogram")
    jacobProtocol = input("\nWould you like to initiate protocol? y/n?: ")
    if jacobProtocol.lower() == "y":

        # Extracting expression values from the DataFrame
        expression_values = df.values

        # Implementing iteration of 4, 6, 8, 13 clusters
        for k_value in [4, 6, 8, 13]:

            # Running k-means clustering
            kmeans = KMeans(n_clusters=k_value, random_state=42)
            kmeans.fit(expression_values)

            # Printing title for terminal print-out
            print("#################################################################")
            print(f"--   CLUSTER: {k_value}   --")

            # Displaying centroids for 4, 6, 8, and 13 initial clusters
            centroids = kmeans.cluster_centers_
            print(f"\nK-means centroids of {k_value} clusters:")
            for i, centroid in enumerate(centroids):
                print(f"Cluster {i + 1}: {centroid}")

            # Displaying the distribution of each cluster
            labels = kmeans.labels_
            for cluster_label in range(k_value):
                cluster_indices = np.where(labels == cluster_label)[0]
                cluster_distribution = expression_values[cluster_indices].flatten()
                print(f"\nDistribution of values in Cluster {cluster_label + 1}:")
                print(f"Minimum value: {cluster_distribution.min()}")
                print(f"Maximum value: {cluster_distribution.max()}")
                print(f"Mean value: {cluster_distribution.mean()}")
                print(f"Standard deviation: {cluster_distribution.std()}")

    else:
        "Terminating program. Sayonara."
    ###############################################################


if __name__ == "__main__":
    brainScan()
