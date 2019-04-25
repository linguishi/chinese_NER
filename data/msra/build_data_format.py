from pathlib import Path

if __name__ == '__main__':
    file_names = ['train', 'testright']
    tag_dict = {'nt': 'ORG', 'ns': 'LOC', 'nr': 'PER', 'o': 'O'}

    for file_name in file_names:
        with Path('raw_data/{}.txt'.format(file_name)).open() as f:
            word_lines = []
            tag_lines = []
            for line in f:
                words = []
                tags = []
                strip_line = line.strip()
                word_tag_pairs = [tuple(item.split('/')) for item in strip_line.split(' ')]
                for word, tag in word_tag_pairs:
                    words.extend(list(word))
                    if tag == 'o':
                        tags.extend(tag_dict[tag] * len(word))
                    else:
                        tags.append('B-{}'.format(tag_dict[tag]))
                        tags.extend(['I-{}'.format(tag_dict[tag])] * (len(word) - 1))
                assert len(tags) == len(words)
                word_lines.append(' '.join(words))
                tag_lines.append(' '.join(tags))

            with Path('{}.words.txt'.format(file_name)).open('w') as g:
                for word_line in word_lines:
                    g.write(word_line + '\n')

            with Path('{}.tags.txt'.format(file_name)).open('w') as d:
                for tag_line in tag_lines:
                    d.write(tag_line + '\n')
