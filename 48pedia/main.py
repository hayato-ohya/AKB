import requests
import bs4
from bs4 import BeautifulSoup
import time
import pandas as pd
import fetch_member_data


def detect_sentence_type(input_sentence):
    positive_words = ['得意', '特技', '好き', '長所', '趣味', '苦手ではない', 'すき']
    negative_words = ['苦手', '嫌い', '短所', '得意ではない', 'きらい']

    positive_flg = False
    negative_flg = False
    for word in positive_words:
        if word in input_sentence:
            positive_flg = True

    for word in negative_words:
        if word in input_sentence:
            negative_flg = True

    if '負けず嫌い' in input_sentence:
        positive_flg = False
        negative_flg = False

    if '好き嫌い' in input_sentence:
        if input_sentence.count('好き') > input_sentence.count('嫌い'):
            positive_flg = True
            negative_flg = False
        elif input_sentence.count('好き') < input_sentence.count('嫌い'):
            positive_flg = False
            negative_flg = True
        else:
            positive_flg = False
            negative_flg = False

    if positive_flg and negative_flg:
        positive_flg = False
        negative_flg = False

    if positive_flg:
        ret = 'positive'
    elif negative_flg:
        ret = 'negative'
    else:
        ret = 'other'

    return ret


def fetch_member_info(address):
    r = requests.get(address)
    soup = BeautifulSoup(r.content, 'html.parser')
    tr = soup.find_all("tr")

    blood_type = None
    height = None

    for elem in tr:
        if hasattr(elem.contents[0], 'contents'):
            if '血液型' == str(elem.contents[0].contents[0]):
                blood_type = elem.contents[1].text.strip('\n').split('[')[0]
            if '身長' in str(elem.contents[0].contents[0]):
                height = elem.contents[1].text.strip('\n').split('[')[0].split(' ')[0]
            if blood_type is not None and height is not None:
                break
        else:
            break

    description = soup.find_all(["h2", "h3", "li"])
    friend_flg = False
    attribute_flg = False
    related_member = []
    attributes = {}
    positive_sentences = []
    negative_sentences = []
    other_sentences = []

    for sentence in description:
        if friend_flg:
            for elem in sentence.contents:
                if hasattr(elem, 'attrs'):
                    if "title" in elem.attrs.keys():
                        related_member.append(elem.attrs["title"])
        if attribute_flg:
            tmp_sentence = ''
            for elem in sentence.contents:
                if type(elem) == bs4.element.NavigableString:
                    tmp_sentence += elem

            if detect_sentence_type(tmp_sentence) == 'positive':
                positive_sentences.append(tmp_sentence)
            elif detect_sentence_type(tmp_sentence) == 'negative':
                negative_sentences.append(tmp_sentence)
            else:
                if not ('ギャラリー' in str(tmp_sentence)):
                    other_sentences.append(tmp_sentence)

        if hasattr(sentence.contents[0], 'attrs'):
            if 'id' in sentence.contents[0].attrs.keys():
                if sentence.contents[0].attrs["id"] == '交友関係':
                    friend_flg = True
                    attribute_flg = False
                elif sentence.contents[0].attrs["id"] == '性格・趣味':
                    attribute_flg = True
                    friend_flg = False
                elif sentence.contents[0].attrs["id"] == 'ギャラリー':
                    break

    attributes['positive_description'] = positive_sentences
    attributes['negative_description'] = negative_sentences
    attributes['other_description'] = other_sentences

    # reshape data
    if height is not None:
        height = float(height.strip('cm'))

    return blood_type, height, attributes


all_data = fetch_member_data.fetch_all_member_data()
homepage = 'https://48pedia.org/'
for group in all_data.keys():
    for i, member in enumerate(all_data[group]):
        web_page = homepage + member['full_name']
        blood_type_, height_, attributes_ = fetch_member_info(web_page)
        all_data[group][i]['blood_type'] = blood_type_
        all_data[group][i]['height'] = height_
        all_data[group][i]['attributes'] = attributes_

        print(all_data[group][i])
        time.sleep(3)  # サーバの負荷軽減

akb_df = pd.DataFrame(all_data['AKB'])
akb_og_df = pd.DataFrame(all_data['AKB_OG'])
ske_df = pd.DataFrame(all_data['SKE'])
ske_og_df = pd.DataFrame(all_data['SKE_OG'])
nmb_df = pd.DataFrame(all_data['NMB'])
nmb_og_df = pd.DataFrame(all_data['NMB_OG'])
hkt_df = pd.DataFrame(all_data['HKT'])
hkt_og_df = pd.DataFrame(all_data['HKT_OG'])
ngt_df = pd.DataFrame(all_data['NGT'])
ngt_og_df = pd.DataFrame(all_data['NGT_OG'])
stu_df = pd.DataFrame(all_data['STU'])
stu_og_df = pd.DataFrame(all_data['STU_OG'])

akb_all_df = pd.concat([akb_df, akb_og_df])
ske_all_df = pd.concat([ske_df, ske_og_df])
nmb_all_df = pd.concat([nmb_df, nmb_og_df])
hkt_all_df = pd.concat([hkt_df, hkt_og_df])
ngt_all_df = pd.concat([ngt_df, ngt_og_df])
stu_all_df = pd.concat([stu_df, stu_og_df])

akbg_df = pd.concat([akb_df, ske_df, nmb_df, hkt_df, ngt_df, stu_df])
akbg_og_df = pd.concat([akb_og_df, ske_og_df, nmb_og_df, hkt_og_df, ngt_og_df, stu_og_df])
akbg_all_df = pd.concat([akbg_df, akbg_og_df])

# save data
akb_df.to_csv('data/akb.csv', index=False)
akb_og_df.to_csv('data/akb_og.csv', index=False)
ske_df.to_csv('data/ske.csv', index=False)
ske_og_df.to_csv('data/ske_og.csv', index=False)
nmb_df.to_csv('data/nmb.csv', index=False)
nmb_og_df.to_csv('data/nmb_og.csv', index=False)
hkt_df.to_csv('data/hkt.csv', index=False)
hkt_og_df.to_csv('data/hkt_og.csv', index=False)
ngt_df.to_csv('data/ngt.csv', index=False)
ngt_og_df.to_csv('data/ngt_og.csv', index=False)
stu_df.to_csv('data/stu.csv', index=False)
stu_og_df.to_csv('data/stu_og.csv', index=False)

akb_all_df.to_csv('data/akb_all.csv', index=False)
ske_all_df.to_csv('data/ske_all.csv', index=False)
nmb_all_df.to_csv('data/nmb_all.csv', index=False)
hkt_all_df.to_csv('data/hkt_all.csv', index=False)
ngt_all_df.to_csv('data/ngt_all.csv', index=False)
stu_all_df.to_csv('data/stu_all.csv', index=False)

akbg_df.to_csv('data/akbg.csv', index=False)
akbg_og_df.to_csv('data/akbg_og.csv', index=False)
akbg_all_df.to_csv('data/akbg_all.csv', index=False)
