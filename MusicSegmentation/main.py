import os
import numpy as np
import matplotlib.pyplot as plt
import librosa
import subprocess
import json
import glob

# %% Video processing using FFmpeg
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

# %% Calculate the distribution of the duration
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

# %%
durations = []
for video_name in all_data:
    for elem in all_data[video_name]:
        durations.append(elem['duration'])
durations = np.array(durations, dtype=np.float32)

# %%
mp3_path = '../media/audio/akb.mp3'
y, sr = librosa.load(mp3_path)


# %% Spectral Flux
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

# %% Features for validation
frame_length = 2048
hop_length = 512
rms = librosa.feature.rms(y, frame_length=frame_length, hop_length=hop_length)
S = librosa.feature.melspectrogram(y, sr=sr, n_mels=128)
log_S = librosa.power_to_db(S, ref=np.max)
mfcc = librosa.feature.mfcc(S=log_S, n_mfcc=13)
delta_mfcc = librosa.feature.delta(mfcc)
delta2_mfcc = librosa.feature.delta(mfcc, order=2)
tempo = librosa.beat.tempo(y=y, aggregate=None)
delta_tempo = np.abs(librosa.feature.delta(tempo))
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

rms = rms[0]

# %% Detect the intervals (RMS)
division_time = []
for elem in all_data['akb']:
    division_time.append(elem['start_time'])

division_frames = librosa.time_to_frames(division_time)

std3 = np.where(rms < np.mean(rms) - 3 * np.std(rms))[0]  # get the indices values where rms < -3σ
division_candidate = list(std3)
frame30 = librosa.time_to_frames(30)

# delete candidates between 0 and 30 seconds
last_frame = division_candidate[-1]
division_candidate[:] = [x for x in division_candidate if not (x != 0 and x < frame30)]
division_candidate[:] = [x for x in division_candidate if not (x != last_frame and x > last_frame - frame30)]

# find consecutive frames
consecutive_frames = []
elem_prev = None
start_frame = None
end_frame = None
for elem in division_candidate:
    if elem != 0:
        if not elem == elem_prev + 1:
            end_frame = elem_prev
            consecutive_frames.append([start_frame, end_frame])
            start_frame = elem
    elem_prev = elem
del consecutive_frames[0]

# delete candidates in consecutive_frames
for start_frame, end_frame in consecutive_frames:
    if end_frame - start_frame > 1:
        division_candidate[:] = [x for x in division_candidate if not (start_frame <= x <= end_frame)]
        frame_idx = np.where(rms[start_frame:end_frame] == rms[start_frame:end_frame].min())[0]
        if len(frame_idx) == 1:
            division_candidate.append(np.int32(start_frame + frame_idx[0]))
        else:
            frame_median = np.median(frame_idx)
            division_candidate.append(np.int32(start_frame + frame_median))

        division_candidate.sort()

# %% Detect the interval (tempo)
# get the indices values where tempo > 3σ
std3_tempo = np.where(delta_tempo > np.mean(delta_tempo) + 3 * np.std(delta_tempo))[0]
