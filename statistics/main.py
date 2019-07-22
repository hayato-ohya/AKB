import os
import numpy as np
import pandas as pd

data_folder = '../data'

akb = pd.read_csv(os.path.join(data_folder, 'akb.csv'))
ske = pd.read_csv(os.path.join(data_folder, 'ske.csv'))
nmb = pd.read_csv(os.path.join(data_folder, 'nmb.csv'))
hkt = pd.read_csv(os.path.join(data_folder, 'hkt.csv'))
ngt = pd.read_csv(os.path.join(data_folder, 'ngt.csv'))
stu = pd.read_csv(os.path.join(data_folder, 'stu.csv'))
akbg = pd.read_csv(os.path.join(data_folder, 'akbg.csv'))

# 年齢, 身長, 出身地, 血液型
# 身長
height_akb_mean = akb['height'].mean()
height_akb_var = akb['height'].var()
height_ske_mean = ske['height'].mean()
height_ske_var = ske['height'].var()
height_nmb_mean = nmb['height'].mean()
height_nmb_var = nmb['height'].var()
height_hkt_mean = hkt['height'].mean()
height_hkt_var = hkt['height'].var()
height_ngt_mean = ngt['height'].mean()
height_ngt_var = ngt['height'].var()
height_stu_mean = stu['height'].mean()
height_stu_var = stu['height'].var()
height_akbg_mean = akbg['height'].mean()
height_akbg_var = akbg['height'].var()

print('# 身長=====================')
print('    | 平均         | 分散')
print('---------------------------')
print('AKB |', '{:.2f}cm'.format(np.round(height_akb_mean, decimals=2)),
      '    | {:.2f}'.format(np.round(height_akb_var, decimals=2)))
print('SKE |', '{:.2f}cm'.format(np.round(height_ske_mean, decimals=2)),
      '    | {:.2f}'.format(np.round(height_ske_var, decimals=2)))
print('NMB |', '{:.2f}cm'.format(np.round(height_nmb_mean, decimals=2)),
      '    | {:.2f}'.format(np.round(height_nmb_var, decimals=2)))
print('HKT |', '{:.2f}cm'.format(np.round(height_hkt_mean, decimals=2)),
      '    | {:.2f}'.format(np.round(height_hkt_var, decimals=2)))
print('NGT |', '{:.2f}cm'.format(np.round(height_ngt_mean, decimals=2)),
      '    | {:.2f}'.format(np.round(height_ngt_var, decimals=2)))
print('STU |', '{:.2f}cm'.format(np.round(height_stu_mean, decimals=2)),
      '    | {:.2f}'.format(np.round(height_stu_var, decimals=2)))
print('全体|', '{:.2f}cm'.format(np.round(height_akbg_mean, decimals=2)),
      '    | {:.2f}'.format(np.round(height_akbg_var, decimals=2)))

# height_df = pd.DataFrame({'AKB': {'mean': height_akb_mean, 'variance': height_akb_var},
# #                           'SKE': {'mean': height_ske_mean, 'variance': height_ske_var},
# #                           'NMB': {'mean': height_nmb_mean, 'variance': height_nmb_var},
# #                           'HKT': {'mean': height_hkt_mean, 'variance': height_hkt_var},
# #                           'NGT': {'mean': height_ngt_mean, 'variance': height_ngt_var},
# #                           'STU': {'mean': height_stu_mean, 'variance': height_stu_var},
# #                           'ALL': {'mean': height_akbg_mean, 'variance': height_akbg_var}})
# # print(height_df.T)

# 血液型
blood_type_akb = {'A型': len(akb[akb['blood_type'] == 'A型']),
                  'B型': len(akb[akb['blood_type'] == 'B型']),
                  'O型': len(akb[akb['blood_type'] == 'O型']),
                  'AB型': len(akb[akb['blood_type'] == 'AB型']),
                  '不明': len(akb[akb['blood_type'] == '不明'])}
blood_type_ske = {'A型': len(ske[ske['blood_type'] == 'A型']),
                  'B型': len(ske[ske['blood_type'] == 'B型']),
                  'O型': len(ske[ske['blood_type'] == 'O型']),
                  'AB型': len(ske[ske['blood_type'] == 'AB型']),
                  '不明': len(ske[ske['blood_type'] == '不明'])}
blood_type_nmb = {'A型': len(nmb[nmb['blood_type'] == 'A型']),
                  'B型': len(nmb[nmb['blood_type'] == 'B型']),
                  'O型': len(nmb[nmb['blood_type'] == 'O型']),
                  'AB型': len(nmb[nmb['blood_type'] == 'AB型']),
                  '不明': len(nmb[nmb['blood_type'] == '不明'])}
blood_type_hkt = {'A型': len(hkt[hkt['blood_type'] == 'A型']),
                  'B型': len(hkt[hkt['blood_type'] == 'B型']),
                  'O型': len(hkt[hkt['blood_type'] == 'O型']),
                  'AB型': len(hkt[hkt['blood_type'] == 'AB型']),
                  '不明': len(hkt[hkt['blood_type'] == '不明'])}
blood_type_ngt = {'A型': len(ngt[ngt['blood_type'] == 'A型']),
                  'B型': len(ngt[ngt['blood_type'] == 'B型']),
                  'O型': len(ngt[ngt['blood_type'] == 'O型']),
                  'AB型': len(ngt[ngt['blood_type'] == 'AB型']),
                  '不明': len(ngt[ngt['blood_type'] == '不明'])}
blood_type_stu = {'A型': len(stu[stu['blood_type'] == 'A型']),
                  'B型': len(stu[stu['blood_type'] == 'B型']),
                  'O型': len(stu[stu['blood_type'] == 'O型']),
                  'AB型': len(stu[stu['blood_type'] == 'AB型']),
                  '不明': len(stu[stu['blood_type'] == '不明'])}
blood_type_akbg = {'A型': len(akbg[akbg['blood_type'] == 'A型']),
                   'B型': len(akbg[akbg['blood_type'] == 'B型']),
                   'O型': len(akbg[akbg['blood_type'] == 'O型']),
                   'AB型': len(akbg[akbg['blood_type'] == 'AB型']),
                   '不明': len(akbg[akbg['blood_type'] == '不明'])}

print('')
print('# 血液型 ===================================================')
print('    | A型         | B型         | O型         | AB型        ')
print('------------------------------------------------------------')
print('AKB |',
      '{:.2f}%'.format(np.round(blood_type_akb['A型'] / (len(akb) - blood_type_akb['不明']) * 100, decimals=2)),
      '     | {:.2f}%'.format(np.round(blood_type_akb['B型'] / (len(akb) - blood_type_akb['不明']) * 100, decimals=2)),
      '     | {:.2f}%'.format(np.round(blood_type_akb['O型'] / (len(akb) - blood_type_akb['不明']) * 100, decimals=2)),
      '     | {:.2f}%'.format(np.round(blood_type_akb['AB型'] / (len(akb) - blood_type_akb['不明']) * 100, decimals=2)))
print('SKE |',
      '{:.2f}%'.format(np.round(blood_type_ske['A型'] / (len(ske) - blood_type_ske['不明']) * 100, decimals=2)),
      '     | {:.2f}%'.format(np.round(blood_type_ske['B型'] / (len(ske) - blood_type_ske['不明']) * 100, decimals=2)),
      '     | {:.2f}%'.format(np.round(blood_type_ske['O型'] / (len(ske) - blood_type_ske['不明']) * 100, decimals=2)),
      '     | {:.2f}%'.format(np.round(blood_type_ske['AB型'] / (len(ske) - blood_type_ske['不明']) * 100, decimals=2)))
print('NMB |',
      '{:.2f}%'.format(np.round(blood_type_nmb['A型'] / (len(nmb) - blood_type_nmb['不明']) * 100, decimals=2)),
      '     | {:.2f}%'.format(np.round(blood_type_nmb['B型'] / (len(nmb) - blood_type_nmb['不明']) * 100, decimals=2)),
      '     | {:.2f}%'.format(np.round(blood_type_nmb['O型'] / (len(nmb) - blood_type_nmb['不明']) * 100, decimals=2)),
      '     | {:.2f}%'.format(np.round(blood_type_nmb['AB型'] / (len(nmb) - blood_type_nmb['不明']) * 100, decimals=2)))
print('HKT |',
      '{:.2f}%'.format(np.round(blood_type_hkt['A型'] / (len(hkt) - blood_type_hkt['不明']) * 100, decimals=2)),
      '     | {:.2f}%'.format(np.round(blood_type_hkt['B型'] / (len(hkt) - blood_type_hkt['不明']) * 100, decimals=2)),
      '     | {:.2f}%'.format(np.round(blood_type_hkt['O型'] / (len(hkt) - blood_type_hkt['不明']) * 100, decimals=2)),
      '     | {:.2f}%'.format(np.round(blood_type_hkt['AB型'] / (len(hkt) - blood_type_hkt['不明']) * 100, decimals=2)))
print('NGT |',
      '{:.2f}%'.format(np.round(blood_type_ngt['A型'] / (len(ngt) - blood_type_ngt['不明']) * 100, decimals=2)),
      '     | {:.2f}%'.format(np.round(blood_type_ngt['B型'] / (len(ngt) - blood_type_ngt['不明']) * 100, decimals=2)),
      '     | {:.2f}%'.format(np.round(blood_type_ngt['O型'] / (len(ngt) - blood_type_ngt['不明']) * 100, decimals=2)),
      '     | {:.2f}%'.format(np.round(blood_type_ngt['AB型'] / (len(ngt) - blood_type_ngt['不明']) * 100, decimals=2)))
print('STU |',
      '{:.2f}%'.format(np.round(blood_type_stu['A型'] / (len(stu) - blood_type_stu['不明']) * 100, decimals=2)),
      '     | {:.2f}%'.format(np.round(blood_type_stu['B型'] / (len(stu) - blood_type_stu['不明']) * 100, decimals=2)),
      '     | {:.2f}%'.format(np.round(blood_type_stu['O型'] / (len(stu) - blood_type_stu['不明']) * 100, decimals=2)),
      '     | {:.2f}%'.format(np.round(blood_type_stu['AB型'] / (len(stu) - blood_type_stu['不明']) * 100, decimals=2)))
print('全体|',
      '{:.2f}%'.format(np.round(blood_type_akbg['A型'] / (len(akbg) - blood_type_akbg['不明']) * 100, decimals=2)),
      '     | {:.2f}%'.format(np.round(blood_type_akbg['B型'] / (len(akbg) - blood_type_akbg['不明']) * 100, decimals=2)),
      '     | {:.2f}%'.format(np.round(blood_type_akbg['O型'] / (len(akbg) - blood_type_akbg['不明']) * 100, decimals=2)),
      '     | {:.2f}%'.format(np.round(blood_type_akbg['AB型'] / (len(akbg) - blood_type_akbg['不明']) * 100, decimals=2)))
