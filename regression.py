import csv
import os

from data.columns import COLUMNS


DATA_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
IGNORE = ['pk', 'total_tweets', 'state', 'candidate']


def monthly_filenames():
    monthly_path = os.path.join(DATA_PATH, 'monthly')
    return [os.path.join(monthly_path, filename)
            for filename in sorted(os.listdir(monthly_path))
            if not filename.endswith('_aligned.csv')]


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
    cleaned = [[v for i, v in enumerate(row) if i not in skip] for row in data][1:]
    cleaned_headers = [v for i, v in enumerate(headers) if i not in skip]
    cleaned_two_party = filter(lambda x: "clinton" in x[-1] or "trump" in x[-1],
                               cleaned)
    return cleaned, cleaned_two_party, cleaned_headers


def get_y_data():
    return read_data('data/results.csv')


def align_x_y(x, y, target="votes"):
    index = {"votes": -2, "electoral": -1}[target]
    aligned_x = []
    aligned_y = []
    for x_data in x:
        matched_x, matched_y = find_y_match(x_data, y)
        aligned_x.append(matched_x)
        aligned_y.append(float(matched_y[index]))
    aligned_x, columns = strip_unwanted_variables(aligned_x)
    return aligned_x, aligned_y, columns


def find_y_match(x_data, y):
    x_candidate, x_state = x_data[-1].lower(), x_data[-2].lower()
    for y_data in y:
        y_candidate, y_state = y_data[1].lower(), y_data[0].lower()
        if y_candidate in x_candidate and x_state == y_state:
            return x_data, y_data


def strip_unwanted_variables(data):
    return [map(float, item[2:-2]) for item in data], COLUMNS[2:-2]


def write_to_csv(filename, x, y, columns):
    new_name = 'aligned/{}'.format(filename.split('/')[-1].replace('.csv', '_aligned.csv'))
    filename = os.path.join(os.path.dirname(filename), new_name)
    with open(filename, 'w') as f:
        writer = csv.writer(f)
        for x_vals, y_vals in zip(x, y):
            row = x_vals + [y_vals]
            writer.writerow(row)


def regression_on_file(filename, target, ignore=[]):
    print(filename)
    data = read_data(filename)
    data, data_two_party, headers = clean_data(data, ignore=ignore)
    y = get_y_data()
    target = "votes"
    x, y, columns = align_x_y(data_two_party, y, target)
    write_to_csv(filename, x, y, columns + [target])



def regression_all_monthly():
    return {filename: regression_on_file(filename, 'votes')
            for filename in monthly_filenames()}


print(regression_all_monthly())
