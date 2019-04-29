from pathlib import Path

import numpy as np


if __name__ == '__main__':
    with Path('vocab.words.txt').open() as f:
        word_to_idx = {line.strip(): idx for idx, line in enumerate(f)}
    with Path('vocab.words.txt').open() as f:
        word_to_found = {line.strip(): False for line in f}

    size_vocab = len(word_to_idx)

    # 0矩阵
    embeddings = np.zeros((size_vocab, 300))

    # 获取相关的character vectors
    found = 0
    print('Reading W2V file (may take a while)')
    with Path('sgns.target.word-character.char1-1.dynwin5.thr10.neg5.dim300.iter5').open() as f:
        for line_idx, line in enumerate(f):
            if line_idx % 100000 == 0:
                print('- At line {}'.format(line_idx))
            line = line.strip().split()
            if len(line) != 300 + 1:
                continue
            word = line[0]
            embedding = line[1:]
            if (word in word_to_idx) and (not word_to_found[word]):
                word_to_found[word] = True
                found += 1
                word_idx = word_to_idx[word]
                embeddings[word_idx] = embedding
    print('- done. Found {} vectors for {} words'.format(found, size_vocab))

    # 保存 np.array
    np.savez_compressed('ch2vec.npz', embeddings=embeddings)
