import os
import numpy as np
import matplotlib.pyplot as plt
import librosa
import subprocess
import json
import glob

#%% Video processing using FFmpeg
file_dir = '../media/video'
filename = 'nmb3_2.mp4'
file_path = os.path.join(file_dir, filename)
cmd = 'ffprobe -v error -show_chapters -of json -i ' + file_path
out = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
media_info = json.loads(out.stdout)

out_file_dir = '../media/video/nmb3_2'
output_name = 'nmb'

for i, elem in enumerate(media_info['chapters']):
    output_file_path = os.path.join(out_file_dir, output_name)
    output_file_path = output_file_path + '_' + str(i).zfill(2) + '.mp4'
    start_time = np.float(elem['start_time'])
    duration = np.float(elem['end_time']) - start_time
    duration = np.round(duration, decimals=6)
    # print(output_file_path)
    print('start:', float(elem['start_time']), 'end:', np.float(elem['end_time']), 'duration:', duration)
    out_cmd = 'ffmpeg -ss ' + str(start_time) + ' -i ' + file_path + ' -t ' + str(duration) + ' ' + output_file_path
    subprocess.run(out_cmd, shell=True)

#%% Calculate the distribution of the duration
json_list = glob.glob('../data/json/*.json')

all_data = {}
for json_path in json_list:
    with open(json_path) as f:
        data = json.load(f)

    video_name = json_path.split('/')[-1].split('.')[0]
    tmp_list = []
    for elem in data['chapters']:
        elem['start'] = np.int(elem['start'])
        elem['start_time'] = np.float(elem['start_time'])
        elem['end'] = np.int(elem['end'])
        elem['end_time'] = np.float(elem['end_time'])
        duration = elem['end_time'] - elem['start_time']
        duration = np.round(duration, decimals=6)
        elem['duration'] = duration
        tmp_list.append(elem)

    all_data[video_name] = tmp_list

#%%
durations = []
for video_name in all_data:
    for elem in all_data[video_name]:
        durations.append(elem['duration'])
durations = np.array(durations, dtype=np.float32)

#%%
mp3_path = '../media/audio/akb.mp3'
y, sr = librosa.load(mp3_path)


#%% Spectral Flux
def calc_spectral_flux(src):
    spec, phase = librosa.magphase(librosa.stft(src), 2)
    power_spec = spec
    # power_spec = np.abs(spec) ** 2
    power_spec = np.divide(power_spec, power_spec.max(axis=0),
                           out=np.zeros_like(power_spec), where=power_spec.max(axis=0) != 0)  # normalization
    spec_diff = power_spec[:, 1:] - power_spec[:, :-1]
    ret = (spec_diff ** 2).sum(axis=0)
    return ret


# flux = calc_spectral_flux(y)

#%% Features for validation
frame_length = 2048
hop_length = 512
rms = librosa.feature.rms(y, frame_length=frame_length, hop_length=hop_length)
S = librosa.feature.melspectrogram(y, sr=sr, n_mels=128)
log_S = librosa.power_to_db(S, ref=np.max)
mfcc = librosa.feature.mfcc(S=log_S, n_mfcc=13)
delta_mfcc = librosa.feature.delta(mfcc)
delta2_mfcc = librosa.feature.delta(mfcc, order=2)
# spec_bw = librosa.feature.spectral_bandwidth(y=y, sr=sr)
# cent = librosa.feature.spectral_centroid(y=y, sr=sr)
# contrast = librosa.feature.spectral_contrast(S=np.abs(librosa.stft(y)), sr=sr)
# flatness = librosa.feature.spectral_flatness(y=y)
# rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr, roll_percent=0.5)
# zero_crossings = librosa.feature.zero_crossing_rate(y=y)
#
# S = np.abs(librosa.stft(y))
# contrast = librosa.feature.spectral_contrast(S=S, sr=sr)
# tonnetz = librosa.feature.tonnetz(y=librosa.effects.harmonic(y), sr=sr)

#%% Detect the intervals
division_time = []
for elem in all_data['akb']:
    division_time.append(elem['start_time'])

rms_normalized = (rms[0] - np.mean(rms[0])) / np.std(rms[0])
std3 = np.where(rms_normalized < -3)[0]  # get the indices values where rms < -3σ
