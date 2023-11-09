from konlpy.tag import Okt
from collections import Counter
import re


def get_keyword(texts, max_length):
    words = ' '.join(texts)
    words = re.sub(r'\([^)]*\)', "", words)
    words = re.sub("[^\uAC00-\uD7A30-9a-zA-Z\s]", "", words)

    okt = Okt()
    words = okt.nouns(words)
    frequency = Counter(words)

    return frequency.most_common(1)

