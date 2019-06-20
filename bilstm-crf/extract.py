import pandas
from sklearn.model_selection import train_test_split
import re

from util import find_locations

with open('data/stopwords2.txt', 'r') as file:
    stop_words = file.read().split('\n')
stop_words.sort(key=lambda x: len(x), reverse=True)

LABEL_BEGIN = 'B-LBL'
LABEL_MIDDLE = 'I-LBL'
LABEL_END = 'E-LBL'

data = pandas.read_csv("data/tiny_label.csv", delimiter="	")
data = data[['desc_clean', 'labels']]


def valid_label(l):
    if len(l) <= 1:
        # print('invalid label removed:' + l)
        return False
    return True


data['labels'] = [list(filter(valid_label, eval(l))) for l in data['labels']]

# limit dataset
data = data.head(256)

for sw in stop_words:
    for i, str in enumerate(data['desc_clean']):
        data['desc_clean'][i] = re.sub(r'[-]{3,}|[*]{3,}', '', str.replace(sw, ''))

full_marks = []

for x, y in zip(data['desc_clean'], data['labels']):
    full_marks.append(['O'] * len(x))
    y.sort(key=lambda x: len(x), reverse=True)
    for label in y:
        found_locs = list(find_locations(x, label))
        if len(found_locs) == 0:
            print(label + ' not found in ' + x)
        for found_location in found_locs:
            if full_marks[-1][found_location] == 'O':
                full_marks[-1][found_location] = LABEL_BEGIN
            else:
                # pass
                print('-----------------------Intersecting labels @ b-----------------------')
                print(x)
                print(y)
                print(label)
                print(x[found_location])
                print(full_marks[-1][found_location])
            for i in range(found_location + 1, found_location + len(label)):
                if i < len(x):
                    if full_marks[-1][i] == 'O':
                        full_marks[-1][i] = LABEL_MIDDLE
                    else:
                        pass
                        # print('-----------------------Intersecting labels @ i-----------------------')
                        # print(x)
                        # print(y)
                        # print(label)
                        # print(x[i])
                        # print(full_marks[-1][i])

X_train, X_test, y_train, y_test = train_test_split(data['desc_clean'], full_marks, test_size=0.1)
