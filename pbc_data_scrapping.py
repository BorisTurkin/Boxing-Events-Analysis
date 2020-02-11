import pandas as pd
import requests
import json
from bs4 import BeautifulSoup
from dateutil.relativedelta import *
from pathlib import Path


# Setup path and links
PATH = str(Path(__file__).parent.absolute()) + '/'
pbc_fights_link = 'https://www.premierboxingchampions.com'
master_page = pbc_fights_link + '/past-boxing-fights'


# Find all links with fights and check if they are indeed active
pbc_links = []
for i in range(1, 100):
    new_link = master_page + '?page=' + str(i)
    response = requests.get(new_link)
    if response.status_code == 200:
        pbc_links.append(new_link)
    else:
        break
pbc_links.append(master_page)


def get_fights(links):
    # Pass a list of links to to pick events.
    empty_list = []
    for link in links:
        soup = BeautifulSoup(requests.get(link).content, 'html.parser')
        events = soup.find_all('script', type='application/ld+json')
        for i in events:
            j = json.loads(i.text)
            for k in range(0, 10):
                try:
                    empty_list.append(
                        [j[k]['name'].replace('&nbsp;', ' '),
                         j[k]['startDate'], j[k]['location']['name'],
                         (j[k]['performer'][0]['givenName'] + ' ' +
                            j[k]['performer'][0]['familyName']),
                         j[k]['performer'][0]['nationality'],
                         j[k]['performer'][0]['workLocation']['addressRegion'],
                         int(j[k]['performer'][0]['weight']['value']),
                         int(j[k]['performer'][0]['height']['value']),
                         j[k]['performer'][0]['birthDate'],
                         (j[k]['performer'][1]['givenName'] + ' ' +
                            j[k]['performer'][1]['familyName']),
                         j[k]['performer'][1]['nationality'],
                         j[k]['performer'][1]['workLocation']['addressRegion'],
                         int(j[k]['performer'][1]['weight']['value']),
                         int(j[k]['performer'][1]['height']['value']),
                         j[k]['performer'][1]['birthDate']])
                except Exception:
                    pass
    return empty_list


# Generate raw dataframe.
df = pd.DataFrame(get_fights(pbc_links), columns=[
    'event', 'date', 'location',
    'name_1', 'nationality_1', 'work_location_1',
    'weight_1', 'height_1', 'dob_1',
    'name_2', 'nationality_2', 'work_location_2',
    'weight_2', 'height_2', 'dob_2'
])
# Clean the dataframe.
df = df.replace({'dob_2': {'2018-08-03': '1989-11-18'}}, regex=True)
for i in ['date', 'dob_1', 'dob_2']:
    df[i] = pd.to_datetime(df[i]).dt.date
df = df.sort_values(by='date', ascending=False).reset_index(drop=True)
df = df.drop_duplicates()
# Add age parameters.
df['age_1'] = [relativedelta(a, b).years for a, b in zip(df.date, df.dob_1)]
df['age_2'] = [relativedelta(a, b).years for a, b in zip(df.date, df.dob_2)]
df['age_d'] = [relativedelta(a, b).years for a, b in zip(df.dob_1, df.dob_2)]


# Predtermined weight classes
weight_classes = pd.read_csv(PATH + 'data/weight_classes.csv')


def pick_weight_class(value):
    # Function to pick a weight class
    df_w = weight_classes[weight_classes['max_value'] >= value]
    return df_w['name'].iloc[-1]


df['weight_class'] = df['weight_1'].apply(pick_weight_class)
df.to_csv(PATH + 'data/pbc_events.csv', index=False)
