import requests
import bs4
from bs4 import BeautifulSoup
import time
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
        if '血液型' == str(elem.contents[0].contents[0]):
            blood_type = elem.contents[1].text.strip('\n').split('[')[0]
        if '身長' == str(elem.contents[0].contents[0]):
            height = elem.contents[1].text.strip('\n').split('[')[0]
        if blood_type is not None and height is not None:
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
        time.sleep(5)  # サーバの負荷軽減
