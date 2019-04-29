"""Reload and serve a saved model"""

from pathlib import Path
from tensorflow.contrib import predictor
import numpy as np

LINE = '''
一九四九年十月一日，这是一个永远为中国人民所纪念的日子。这一天，北京30万军民聚集在天安门广场上举行了开国大典。人群和旗帜、彩绸、鲜花、灯饰，汇成了喜庆的锦秀海洋。下午3时，大地欢声雷动。毛泽东和朱德两位伟人一前一后，沿着城楼西侧的古砖梯道，最先登上了天安门城楼。当林伯渠宣布开会后，在国歌《义勇军进行曲》的乐曲声中，中央人民政府主席、副主席和委员就位。人民领袖毛泽东庄严宣布：“中华人民共和国中央人民政府成立了!”这个洪亮的声音震撼了北京城，震撼了全国，震撼了全世界，开创了中国各民族人民的新世纪。
'''


def extract_entities(tags_array, text_line):
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


if __name__ == '__main__':
    export_dir = 'saved_model'
    subdirs = [x for x in Path(export_dir).iterdir()
               if x.is_dir() and 'temp' not in str(x)]
    latest = str(sorted(subdirs)[-1])
    predict_fn = predictor.from_saved_model(latest)
    words = [w.encode() for w in LINE.strip()]
    nwords = len(words)
    predictions = predict_fn({'words': [words], 'nwords': [nwords]})
    print(predictions)
    print(extract_entities(predictions['tags'], LINE.strip()))
