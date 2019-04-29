"""Reload and serve a saved model"""

from pathlib import Path
from tensorflow.contrib import predictor
from functools import partial
import numpy as np

LINE = '''中央纪委国家监委网站4月29日消息，日前，经中共中央批准，中央纪委国家监委对陕西省委原常委、秘书长钱引安严重违纪违法问题进行了立案审查调查。'''


def extract_entities(tags_array, text_line):
    text_line = text_line.strip()
    results = {'PER': [], 'LOC': [], 'ORG': []}
    begin = len(text_line)
    meet_b = False
    entity = 'O'
    for idx, tag in enumerate(np.squeeze(tags_array)):
        tag = tag.decode()
        if tag[0] == 'B' and not meet_b:
            meet_b = True
            begin = idx
            entity = tag[2:]
        elif tag[0] == 'B' and meet_b:
            results[entity].append(text_line[begin:idx])
            meet_b = False
        elif tag[0] == 'O' and meet_b:
            results[entity].append(text_line[begin:idx])
            meet_b = False
    if meet_b:
        results[entity].append(text_line[begin:])
    return results


def predict(pred_fn, line):
    words = [w.encode() for w in line.strip()]
    nwords = len(words)
    predictions = pred_fn({'words': [words], 'nwords': [nwords]})
    return predictions


if __name__ == '__main__':
    export_dir = 'saved_model'
    subdirs = [x for x in Path(export_dir).iterdir()
               if x.is_dir() and 'temp' not in str(x)]
    latest = str(sorted(subdirs)[-1])
    predict_fn = partial(predict, predictor.from_saved_model(latest))
    print(LINE)
    print(extract_entities(predict_fn(LINE)['tags'], LINE))
    line = input('\n\n输入一句中文： ')
    while line.strip().lower() != 'q':
        print('\n\n', extract_entities(predict_fn(line)['tags'], line))
        line = input('\n\n输入一句中文： ')
