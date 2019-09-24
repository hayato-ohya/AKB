import os
import numpy as np
import glob
import pandas as pd


def aggregate_data():
    folder_list = os.listdir('latent_representations')
    print(folder_list)

    for folder_name in folder_list:
        npy_list = glob.glob('latent_representations/' + folder_name + '/*.npy')
        all_data = np.zeros([len(npy_list), 18, 512], dtype=np.float32)

        for i, elem in enumerate(npy_list):
            npy = np.load(npy_list[i])
            npy_reshaped = npy.reshape([1, 18, 512])
            all_data[i, :, :] = npy_reshaped

        np.save('aggregated_data/' + folder_name + '.npy', all_data)
        np.save('stats_data/' + folder_name + '_mean.npy', np.mean(all_data, axis=0))
        np.save('stats_data/' + folder_name + '_variance.npy', np.var(all_data, axis=0))


# folder_list = os.listdir('latent_representations')
mean_data_dict = {}
mean_list = glob.glob('stats_data/*_mean.npy')
for npy_mean_path in mean_list:
    member_name = npy_mean_path.split('stats_data/')[-1].split('_mean.npy')[0]
    npy_mean = np.load(npy_mean_path)
    mean_data_dict[member_name] = npy_mean.flatten()

similarity = {}
for key in mean_data_dict:
    tmp_dict = {}
    for key2 in mean_data_dict:
        tmp_dict[key2] = np.sqrt(((mean_data_dict[key] - mean_data_dict[key2]) ** 2).sum())

    similarity[key] = tmp_dict

similarity_pd = pd.DataFrame(similarity)
