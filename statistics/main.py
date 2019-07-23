import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import japanmap as jpm

data_folder = '../data'

akb = pd.read_csv(os.path.join(data_folder, 'akb.csv'))
ske = pd.read_csv(os.path.join(data_folder, 'ske.csv'))
nmb = pd.read_csv(os.path.join(data_folder, 'nmb.csv'))
hkt = pd.read_csv(os.path.join(data_folder, 'hkt.csv'))
ngt = pd.read_csv(os.path.join(data_folder, 'ngt.csv'))
stu = pd.read_csv(os.path.join(data_folder, 'stu.csv'))
akbg = pd.read_csv(os.path.join(data_folder, 'akbg.csv'))

all_data = {'AKB': akb, 'SKE': ske, 'NMB': nmb, 'HKT': hkt, 'NGT': ngt, 'STU': stu, 'AKBG': akbg}

# 年齢, 身長, 出身地, 血液型
# 身長
heights = {}
for key in all_data.keys():
    heights[key] = [all_data[key]['height'].mean(), all_data[key]['height'].std()]

print('# 身長===========================')
print('     | 平均         | 標準偏差')
print('---------------------------------')
for key in heights.keys():
    if key == 'AKBG':
        print('全体', '|', '{:.2f}cm'.format(np.round(heights[key][0], decimals=2)),
              '    | {:.2f}'.format(np.round(heights[key][1], decimals=2)))
    else:
        print(key, ' |', '{:.2f}cm'.format(np.round(heights[key][0], decimals=2)),
              '    | {:.2f}'.format(np.round(heights[key][1], decimals=2)))

print('---------------------------------')

# 血液型
blood_type = {}
for key in all_data.keys():
    blood_type[key] = {'A型': len(all_data[key][all_data[key]['blood_type'] == 'A型']),
                       'B型': len(all_data[key][all_data[key]['blood_type'] == 'B型']),
                       'O型': len(all_data[key][all_data[key]['blood_type'] == 'O型']),
                       'AB型': len(all_data[key][all_data[key]['blood_type'] == 'AB型']),
                       '不明': len(all_data[key][all_data[key]['blood_type'] == '不明'])}

print('')
print('# 血液型 ===================================================')
print('     | A型         | B型         | O型         | AB型        ')
print('------------------------------------------------------------')
for key in blood_type.keys():
    if key == 'AKBG':
        print('全体', '|',
              '{:.2f}%'.format(np.round(blood_type[key]['A型']
                                        / (len(all_data[key]) - blood_type[key]['不明']) * 100, decimals=2)),
              '     | {:.2f}%'.format(np.round(blood_type[key]['B型']
                                               / (len(all_data[key]) - blood_type[key]['不明']) * 100, decimals=2)),
              '     | {:.2f}%'.format(np.round(blood_type[key]['O型']
                                               / (len(all_data[key]) - blood_type[key]['不明']) * 100, decimals=2)),
              '     | {:.2f}%'.format(np.round(blood_type[key]['AB型']
                                               / (len(all_data[key]) - blood_type[key]['不明']) * 100, decimals=2)))
    else:
        print(key, ' |',
              '{:.2f}%'.format(np.round(blood_type[key]['A型']
                                        / (len(all_data[key]) - blood_type[key]['不明']) * 100, decimals=2)),
              '     | {:.2f}%'.format(np.round(blood_type[key]['B型']
                                               / (len(all_data[key]) - blood_type[key]['不明']) * 100, decimals=2)),
              '     | {:.2f}%'.format(np.round(blood_type[key]['O型']
                                               / (len(all_data[key]) - blood_type[key]['不明']) * 100, decimals=2)),
              '     | {:.2f}%'.format(np.round(blood_type[key]['AB型']
                                               / (len(all_data[key]) - blood_type[key]['不明']) * 100, decimals=2)))
print('------------------------------------------------------------')
print('')


# 年齢・誕生日
def calc_age(birthday):
    today = int(pd.to_datetime('today').strftime('%Y%m%d'))
    birthday = int(birthday)
    return int((today - birthday) / 10000)


for key in all_data.keys():
    all_data[key]['age'] = all_data[key]['birthday'].apply(lambda date: calc_age(date))

print('# 誕生日===========================================================================================')
print('     | 最年長                                     | 最年少')
print('---------------------------------------------------------------------------------------------------')
for key in all_data.keys():
    if key == 'AKBG':
        print_str = '全体' + ' | '
    else:
        print_str = key + '  | '

    print_str = print_str \
                + all_data[key][all_data[key]['birthday'] == all_data[key]['birthday'].min()]['full_name'].values[0]

    if len(all_data[key][all_data[key]['birthday'] == all_data[key]['birthday'].min()]['full_name'].values[0]) == 4:
        print_str = print_str + '  '
    elif len(all_data[key][all_data[key]['birthday'] == all_data[key]['birthday'].min()]['full_name'].values[0]) == 3:
        print_str = print_str + '    '

    print_str = print_str + 'さん (' \
                + str(all_data[key][all_data[key]['birthday'] == all_data[key]['birthday'].min()]['age'].values[0]) \
                + '歳' \
                + '| ' + str(all_data[key]['birthday'].min())[:4] + '年' \
                + str(all_data[key]['birthday'].min())[4:6] + '月' \
                + str(all_data[key]['birthday'].min())[6:] + '日生まれ' + ')'
    print_str = print_str + ' | ' \
                + all_data[key][all_data[key]['birthday'] == all_data[key]['birthday'].max()]['full_name'].values[0] \
                + 'さん '

    if len(all_data[key][all_data[key]['birthday'] == all_data[key]['birthday'].max()]['full_name'].values[0]) == 4:
        print_str = print_str + '  '
    elif len(all_data[key][all_data[key]['birthday'] == all_data[key]['birthday'].max()]['full_name'].values[0]) == 3:
        print_str = print_str + '    '

    print_str = print_str \
                + '(' \
                + str(all_data[key][all_data[key]['birthday'] == all_data[key]['birthday'].max()]['age'].values[0]) \
                + '歳' + '| ' + str(all_data[key]['birthday'].max())[:4] + '年' \
                + str(all_data[key]['birthday'].max())[4:6] + '月' \
                + str(all_data[key]['birthday'].max())[6:] + '日生まれ' + ')'

    print(print_str)

print('---------------------------------------------------------------------------------------------------')
print()

ages = {}
for key in all_data.keys():
    ages[key] = [all_data[key]['age'].mean(), all_data[key]['age'].std()]

print('# 年齢===========================')
print('     | 平均        | 標準偏差')
print('---------------------------------')
for key in ages.keys():
    if key == 'AKBG':
        print('全体', '|', '{:.2f}歳'.format(np.round(ages[key][0], decimals=2)),
              '    | {:.2f}'.format(np.round(ages[key][1], decimals=2)))
    else:
        print(key, ' |', '{:.2f}歳'.format(np.round(ages[key][0], decimals=2)),
              '    | {:.2f}'.format(np.round(ages[key][1], decimals=2)))

print('---------------------------------')
print()

# 出身地
prefectures = {}
for key in all_data:
    tmp_dict = {}
    for prefecture in jpm.pref_names:
        tmp_dict[prefecture] = len(all_data[key][all_data[key]['prefecture'] == prefecture])

    prefectures[key] = tmp_dict

color_list = ['red', 'deeppink', 'orangered', 'gold', 'yellow', 'greenyellow',
              'limegreen', 'darkcyan', 'blue', 'midnightblue']

prefecture_colors = {}
for key in prefectures.keys():
    prefecture_color = {}
    for prefecture in prefectures[key]:
        if prefecture is not '_':
            if prefectures[key][prefecture] > max(prefectures[key].values()) * 0.9:
                prefecture_color[prefecture] = color_list[0]
            elif prefectures[key][prefecture] > max(prefectures[key].values()) * 0.8:
                prefecture_color[prefecture] = color_list[1]
            elif prefectures[key][prefecture] > max(prefectures[key].values()) * 0.7:
                prefecture_color[prefecture] = color_list[2]
            elif prefectures[key][prefecture] > max(prefectures[key].values()) * 0.6:
                prefecture_color[prefecture] = color_list[3]
            elif prefectures[key][prefecture] > max(prefectures[key].values()) * 0.5:
                prefecture_color[prefecture] = color_list[4]
            elif prefectures[key][prefecture] > max(prefectures[key].values()) * 0.4:
                prefecture_color[prefecture] = color_list[5]
            elif prefectures[key][prefecture] > max(prefectures[key].values()) * 0.3:
                prefecture_color[prefecture] = color_list[6]
            elif prefectures[key][prefecture] > max(prefectures[key].values()) * 0.2:
                prefecture_color[prefecture] = color_list[7]
            elif prefectures[key][prefecture] > max(prefectures[key].values()) * 0.1:
                prefecture_color[prefecture] = color_list[8]
            elif prefectures[key][prefecture] >= 1:
                prefecture_color[prefecture] = color_list[9]

    prefecture_colors[key] = prefecture_color

# for key in prefecture_colors.keys():
#     plt.imshow(jpm.picture(prefecture_colors[key]))

plt.imshow(jpm.picture(prefecture_colors['AKB']))
# plt.imshow(jpm.picture(prefecture_colors['SKE']))
# plt.imshow(jpm.picture(prefecture_colors['NMB']))
# plt.imshow(jpm.picture(prefecture_colors['HKT']))
# plt.imshow(jpm.picture(prefecture_colors['NGT']))
# plt.imshow(jpm.picture(prefecture_colors['STU']))
