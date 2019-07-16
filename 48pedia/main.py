import requests
from bs4 import BeautifulSoup


def fetch_member_list(members):
    member_list = []
    for i in range(len(members)):
        if len(members[i].contents) == 18 and hasattr(members[i].contents[5].contents[0], 'contents'):
            member_dict = {}
            print(i)
            if '・' in members[i].contents[1].text.strip('\n'):
                team1 = members[i].contents[1].text.strip('\n').split('・')[0]
                team2 = members[i].contents[1].text.strip('\n').split('・')[1]
            else:
                team1 = members[i].contents[1].text.strip('\n')
                team2 = None

            if '研' in team1:
                team1 = team1.strip('研')
                team2 = '研'

            full_name = members[i].contents[5].contents[0].contents[0].text
            kana = members[i].contents[5].contents[0].contents[3].text
            # nickname = members[i].contents[7].text.strip('\n')
            birthday = members[i].contents[9].contents[0].attrs['data-sort-value']
            enrollment = members[i].contents[13].contents[0].text.strip(' ')

            # nickname
            if len(members[i].contents[7].contents) == 1:
                nickname = members[i].contents[7].contents[0].strip('\n')
            else:
                nickname = []
                for j in range(len(members[i].contents[7].contents)):
                    if not ('br' in str(members[i].contents[7].contents[j])):
                        nickname.append(members[i].contents[7].contents[j].strip('\n'))

            # prefecture
            if hasattr(members[i].contents[11].contents[0], 'text'):
                prefecture = members[i].contents[11].contents[0].text
            else:
                prefecture = members[i].contents[11].contents[0].strip('\n')

            if team2 == '研':
                promotion = None
            else:
                promotion = members[i].contents[15].contents[0].attrs['data-sort-value']

            # note / sister
            sister = None
            note = []
            note_list = members[i].contents[17].contents
            for j in range(len(note_list)):
                if '姉' in note_list[j] or '妹' in note_list[j]:
                    if j+1 == len(note_list):
                        # print(j, note_list[j])
                        if '研究生' in str(note_list[j]):
                            sister = note_list[j].split('研究生')[-1].strip('\n')
                        elif '8' in str(note_list[j]):
                            sister = note_list[j].split('8')[-1].strip('\n')
                        elif 'N' in str(note_list[j]):
                            print('N')
                            sister = note_list[j].split('N')[-1].strip('\n')

                    else:
                        # print("sister", j, note_list[j+1])
                        sister = note_list[j+1].contents[0]

                elif not note_list[j] == '\n':
                    if not ('br' in str(note_list[j])):
                        if hasattr(note_list[j], 'text'):
                            note.append(note_list[j].text.strip('\n'))
                        else:
                            note.append(note_list[j].strip('\n'))

            member_dict['birthday'] = birthday
            member_dict['enrollment'] = enrollment
            member_dict['full_name'] = full_name
            member_dict['kana'] = kana
            member_dict['nickname'] = nickname
            member_dict['prefecture'] = prefecture
            member_dict['promotion'] = promotion
            member_dict['sister'] = sister
            member_dict['team1'] = team1
            member_dict['team2'] = team2
            member_dict['note'] = note

            member_list.append(member_dict)

    return member_list


# AKB
r_AKB = requests.get("https://48pedia.org/AKB48%E3%83%A1%E3%83%B3%E3%83%90%E3%83%BC%E4%B8%80%E8%A6%A7")
soup_AKB = BeautifulSoup(r_AKB.content, 'html.parser')
members_AKB = soup_AKB.find_all("tr")
member_list_AKB = fetch_member_list(members_AKB)

# AKB (OG)

# NMB
r_NMB = requests.get('https://48pedia.org/NMB48%E3%83%A1%E3%83%B3%E3%83%90%E3%83%BC%E4%B8%80%E8%A6%A7')
soup_NMB = BeautifulSoup(r_NMB.content, 'html.parser')
members_NMB = soup_NMB.find_all("tr")
member_list_NMB = fetch_member_list(members_NMB)

# SKE

# HKT

# NGT

# STU
