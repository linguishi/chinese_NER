from collections import Counter
from pathlib import Path

MINCOUNT = 1

if __name__ == '__main__':
    # 1. Words
    print('Build vocab words')
    counter_words = Counter()
    for n in ['train', 'testright']:
        with Path('{}.words.txt'.format(n)).open() as f:
            for line in f:
                counter_words.update(line.strip().split())

    vocab_words = {w for w, c in counter_words.items() if c >= MINCOUNT}

    with Path('vocab.words.txt').open('w') as f:
        for w in sorted(list(vocab_words)):
            f.write('{}\n'.format(w))
    print('- done. Kept {} out of {}'.format(
        len(vocab_words), len(counter_words)))

    # 2. Tags
    print('Build vocab tags (may take a while)')
    vocab_tags = set()
    with Path('{}.tags.txt'.format('train')).open() as f:
        for line in f:
            vocab_tags.update(line.strip().split())

    with Path('vocab.tags.txt').open('w') as f:
        for t in sorted(list(vocab_tags)):
            f.write('{}\n'.format(t))
    print('- done. Found {} tags.'.format(len(vocab_tags)))
