import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans


def cluster_main(time_series, task='get_label', n_clusters=3):
    time_series_arr = np.array(time_series)
    if task == 'get_best_k':
        get_best_k(time_series_arr.T)
    else:
        return get_k_means_label(time_series_arr.T, k=n_clusters, max_iter=100)


def get_k_means_label(input_x, k, max_iter=100):
    km = KMeans(n_clusters=k, max_iter=max_iter).fit(input_x)
    return km.labels_


def get_best_k(input_x):

    distortions = []
    K = input_x.shape[0] + 1
    for k in range(1, K):
        km = KMeans(n_clusters=k, max_iter=100).fit(input_x)

        # Sum of squared distances of samples to their closest cluster center
        err = km.inertia_
        distortions.append(err)

    # Plot the elbow
    plt.figure(figsize=(10, 8))
    plt.plot(range(1, K), distortions, 'bx-')
    plt.xlabel('k', fontsize=15)
    plt.ylabel('Distortion', fontsize=15)
    plt.xticks(fontsize=15)
    plt.yticks(fontsize=15)
    plt.title(' The Elbow Method showing the optimal k')
    plt.show()


# def get_best_k_cv(air_quality_model):
#     """
#     Specifically for leave one out CV algorithm
#
#     """
#
#     locations = air_quality_model.air_quality_locations
#     time_series = air_quality_model.air_quality_time_series
#
#     for each_location in locations:
#
#         other_locations = [i for i in locations if i != each_location]
#         train_time_series = time_series[other_locations]
#         scaled_train_time_series = air_quality_model.scaler.transform(train_time_series)
#         train_time_series_dropna = scaled_train_time_series.dropna().T
#
#         # k means determine k
#         distortions = []
#         K = range(1, len(other_locations) + 1, 1)
#         for k in K:
#             kmeans = KMeans(n_clusters=k, max_iter=300).fit(train_time_series_dropna)
#             # err = sum(np.min(cdist(train_time_series_dropna, kmeans.cluster_centers_, 'euclidean'), axis=1)) \
#             #       / train_time_series_dropna.shape[0]
#
#             # Sum of squared distances of samples to their closest cluster center
#             err = kmeans.inertia_
#             distortions.append(err)
#             print(k, dict(zip(other_locations, kmeans.labels_)))
#             print(each_location, k, 'err=', err)
#
#         # Plot the elbow
#         plt.figure(figsize=(15, 20))
#         plt.plot(K, distortions, 'bx-')
#         plt.xlabel('k')
#         plt.ylabel('Distortion')
#         plt.title(str(each_location) + ' The Elbow Method showing the optimal k')
#         plt.show()
#
