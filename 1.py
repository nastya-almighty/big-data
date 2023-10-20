import opendatasets as od
import pandas as pd
import time
from pathlib import Path

dataset_path = Path('imdb-user-reviews', 'song_lyrics.csv')
if not dataset_path.is_file():
    od.download('https://www.kaggle.com/datasets/sadmadlad/imdb-user-reviews')


import json


n, mean, M2 = 0, 0.0, 0
for path in Path('imdb-user-reviews').glob('**/*'):
    if path.is_file() and path.suffix == '.json':
        with open(path, 'r') as f:
            info = json.load(f)
        score = float(info['movieIMDbRating'])
        n += 1
        delta = score - mean
        mean += delta / n
        M2 += delta * (score - mean)

print(mean, (M2 / n) ** (1/2))


from functools import reduce

def mapper(path):
    with open(path, 'r') as f:
        info = json.load(f)
    score = float(info['movieIMDbRating'])
    print(f"Processed {path}: rating = {score}")
    return (score, 1)

def reducer(score_data1, score_data2):
    score1, n1, M2_1 = score_data1
    if len(score_data2) == 2:
        score2, n2 = score_data2
        M2_2 = 0
    else:
        score2, n2, M2_2 = score_data2
    n = n1 + n2
    mean1 = score1 * n1
    mean2 = score2 * n2
    mean = (mean1 + mean2) / n
    delta = score2 - score1
    M2 = M2_1 + M2_2 + delta * delta * n1 * n2 / n
    return (mean, n, M2)

json_files = [path for path in Path('imdb-user-reviews').glob('**/*.json') if path.is_file()]

# среднее и М2
initial_value = (0, 0, 0)
result = reduce(reducer, map(mapper, json_files), initial_value)

mean, n, M2 = result
std_deviation = (M2 / n) ** 0.5

print(mean, std_deviation)