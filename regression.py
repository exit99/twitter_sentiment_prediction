import csv
import os

from sklearn.linear_model import LinearRegression


DATA_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
IGNORE = ['pk', 'total_tweets', 'state', 'candidate']


def monthly_filenames():
    monthly_path = os.path.join(DATA_PATH, 'monthly')
    return [os.path.join(monthly_path, filename)
            for filename in sorted(os.listdir(monthly_path))]


def read_data(filename):
    with open(filename, 'r') as f:
        return [v for v in csv.reader(f)]


def add_voting_data(data):
    with open(os.path.join(DATA_PATH, 'results.csv'), 'r') as f:
        results = [v for v in csv.reader(f)]
    new_data = [data[0] + [results[0][2], results[0][3]]]  # Combined headers
    for row in data[1:]:
        for v in results[1:]:
            state, name, votes, delegates = v[0], v[1], v[2], v[3]
            if state == row[-2] and name.lower() in row[-1].lower():
                row += [votes, delegates]
                new_data.append(row)
                break
    return new_data


def clean_data(data, ignore=[]):
    headers = data[0]
    skip = [i for i, v in enumerate(headers) if v in ignore]
    cleaned = [[v for i, v in enumerate(row) if i not in skip] for row in data]
    cleaned_headers = [v for i, v in enumerate(headers) if i not in skip]
    return cleaned, cleaned_headers


def seperate_x_y(data, target):
    pass


def regression_on_file(filename, target, ignore=[]):
    lr = LinearRegression()
    data = read_data(filename)
    data = clean_data(data, target, ignore=ignore)
    import pdb; pdb.set_trace();


def regression_all_monthly():
    return {filename: regression_on_file(filename, 'votes')
            for filename in monthly_filenames()}
