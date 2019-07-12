import requests
from bs4 import BeautifulSoup

r = requests.get("https://48pedia.org/AKB48%E3%83%A1%E3%83%B3%E3%83%90%E3%83%BC%E4%B8%80%E8%A6%A7")
soup = BeautifulSoup(r.content, 'html.parser')
# print(soup)

members = soup.find_all("tr")

i = 1
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
nickname = members[i].contents[7].text.strip('\n')
birthday = members[i].contents[9].contents[0].attrs['data-sort-value']
prefecture = members[i].contents[11].contents[0].text
enrollment = members[i].contents[13].contents[0].text.strip(' ')

if team2 == '研':
    promotion = None
else:
    promotion = members[i].contents[15].contents[0].attrs['data-sort-value']
