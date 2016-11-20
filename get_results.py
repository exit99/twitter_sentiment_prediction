import csv
import re
import requests

from bs4 import BeautifulSoup


def valid_name(name):
    for candidate in ['trump', 'clinton', 'johnson', 'stein']:
        if candidate in name.lower():
            return True


def get_data():
    link = "http://www.politico.com/2016-election/results/map/president"
    html = requests.get(link).text
    soup = BeautifulSoup(html, 'html.parser')
    states = soup.find_all("div", {"class": "results-data"})
    data = {}
    for state_table in states:
        abbrev = state_table['data-stateabb']
        results = {}
        for row in state_table.find_all('tr'):
            name_combo = row.find("span", {"class": "name-combo"})
            for string in name_combo.stripped_strings:
                name = string.split('. ')[-1]
            if not valid_name(name):
                continue
            votes = re.sub(',', '', row.find("td", {"class": "results-popular"}).text)
            votes = int(votes)
            delegates = row.find("td", {"class": "delegates-cell"}) or 0
            if delegates:
                if delegates.text:
                    delegates = int(delegates.text)
                else:
                    delegates = 0
            results[name] = {
                "votes": votes,
                "delegates": delegates,
            }
        data[abbrev] = results
    return data


data = get_data()
with open("data/results.csv", "w") as f:
    writer = csv.writer(f)
    writer.writerow(["state", "candidate", "votes", "delegates"])
    for state, items in data.items():
        for name, stats in items.items():
            writer.writerow([state, name, stats['votes'], stats['delegates']])
