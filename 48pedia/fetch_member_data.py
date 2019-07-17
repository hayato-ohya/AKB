import requests
from bs4 import BeautifulSoup


def fetch_member_list(members):
    member_list = []
    og_list = []
    active_flg = True
    for i in range(len(members)):
        if len(members[i].contents) == 18 and ('元\n' in str(members[i].contents[1].contents[0])):
            active_flg = False
        elif len(members[i].contents) == 18 and ('最終在籍日' in str(members[i].contents[15].contents[0])):
            active_flg = False

        if len(members[i].contents) == 18 and hasattr(members[i].contents[5].contents[0], 'contents'):
            member_dict = {}
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
            enrollment = members[i].contents[13].contents[0].text.strip(' ')

            # birthday
            if hasattr(members[i].contents[9].contents[0], 'attrs'):
                birthday = members[i].contents[9].contents[0].attrs['data-sort-value']
            else:
                birthday = None

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
            elif hasattr(members[i].contents[15].contents[0], 'attrs') is False:
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
                        if '研究生' in str(note_list[j]):
                            sister = note_list[j].split('研究生')[-1].strip('\n')
                        elif '8' in str(note_list[j]):
                            sister = note_list[j].split('8')[-1].strip('\n')
                        elif 'N' in str(note_list[j]):
                            sister = note_list[j].split('N')[-1].strip('\n')

                    else:
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
            member_dict['promotion'] = promotion  # OGは最終在籍日
            member_dict['sister'] = sister
            member_dict['team1'] = team1
            member_dict['team2'] = team2
            member_dict['note'] = note

            if active_flg:
                member_dict['active'] = 1
                member_list.append(member_dict)
            else:
                member_dict['active'] = 0
                og_list.append(member_dict)

    return member_list, og_list


def fetch_all_member_data():
    # AKB
    r_akb = requests.get("https://48pedia.org/AKB48%E3%83%A1%E3%83%B3%E3%83%90%E3%83%BC%E4%B8%80%E8%A6%A7")
    soup_akb = BeautifulSoup(r_akb.content, 'html.parser')
    members_akb = soup_akb.find_all("tr")
    member_list_akb = fetch_member_list(members_akb)[0]

    # AKB (OG)
    r_akb_og = requests.get('https://48pedia.org/AKB48%E5%85%83%E3%83%A1%E3%83%B3%E3%83%90%E3%83%BC%E4%B8%80%E8%A6%A7')
    soup_akb_og = BeautifulSoup(r_akb_og.content, 'html.parser')
    members_akb_og = soup_akb_og.find_all("tr")
    member_list_akb_og = fetch_member_list(members_akb_og)[1]

    # NMB
    r_nmb = requests.get('https://48pedia.org/NMB48%E3%83%A1%E3%83%B3%E3%83%90%E3%83%BC%E4%B8%80%E8%A6%A7')
    soup_nmb = BeautifulSoup(r_nmb.content, 'html.parser')
    members_nmb = soup_nmb.find_all("tr")
    member_list_nmb, member_list_nmb_og = fetch_member_list(members_nmb)

    # SKE
    r_ske = requests.get('https://48pedia.org/SKE48%E3%83%A1%E3%83%B3%E3%83%90%E3%83%BC%E4%B8%80%E8%A6%A7')
    soup_ske = BeautifulSoup(r_ske.content, 'html.parser')
    members_ske = soup_ske.find_all("tr")
    member_list_ske, member_list_ske_og = fetch_member_list(members_ske)

    # HKT
    r_hkt = requests.get('https://48pedia.org/HKT48%E3%83%A1%E3%83%B3%E3%83%90%E3%83%BC%E4%B8%80%E8%A6%A7')
    soup_hkt = BeautifulSoup(r_hkt.content, 'html.parser')
    members_hkt = soup_hkt.find_all("tr")
    member_list_hkt, member_list_hkt_og = fetch_member_list(members_hkt)

    # NGT
    r_ngt = requests.get('https://48pedia.org/NGT48%E3%83%A1%E3%83%B3%E3%83%90%E3%83%BC%E4%B8%80%E8%A6%A7')
    soup_ngt = BeautifulSoup(r_ngt.content, 'html.parser')
    members_ngt = soup_ngt.find_all("tr")
    member_list_ngt, member_list_ngt_og = fetch_member_list(members_ngt)

    # STU
    r_stu = requests.get('https://48pedia.org/STU48%E3%83%A1%E3%83%B3%E3%83%90%E3%83%BC%E4%B8%80%E8%A6%A7')
    soup_stu = BeautifulSoup(r_stu.content, 'html.parser')
    members_stu = soup_stu.find_all("tr")
    member_list_stu, member_list_stu_og = fetch_member_list(members_stu)

    all_member = {'AKB': member_list_akb,
                  'AKB_OG': member_list_akb_og,
                  'SKE': member_list_ske,
                  'SKE_OG': member_list_ske_og,
                  'NMB': member_list_nmb,
                  'NMB_OG': member_list_nmb_og,
                  'HKT': member_list_hkt,
                  'HKT_OG': member_list_hkt_og,
                  'NGT': member_list_ngt,
                  'NGT_OG': member_list_ngt_og,
                  'STU': member_list_stu,
                  'STU_OG': member_list_stu_og}

    return all_member
