from multiprocessing.pool import Pool
from unidecode import unidecode
import pycrfsuite
import json
from pymongo import MongoClient
import os
import random

client = MongoClient('mongodb://127.0.0.1:27017/', connect=False)
db_text = client['corpus']['all']

with open('./config_tone.json', 'r') as fs:
    config_labels = json.load(fs)


def type_of_word(word: str):
    if word.isdigit():
        return "N"
    if word.isupper():
        return "U"
    if word.istitle():
        return "T"
    if word.islower():
        return "L"
    return "0"


def word2features(sent, i, train_word):
    word = sent[i]
    features = [
        'word=' + word.lower(),
        'word.isdigit=%s' % word.isdigit(),
    ]
    if i - 1 >= 0:
        word1 = sent[i - 1]
        features.extend([
            '-1:word=' + word1.lower(),
            '-1.isdigit=%s' % word1.isdigit(),
        ])
    else:
        features.append('BOS')
    if i - 2 >= 0:
        word2 = sent[i - 2]
        features.extend([
            '-2:word=' + word2.lower(),
            '-2.isdigit=%s' % word2.isdigit(),
        ])
    else:
        features.append('BOS')
    # if i - 3 >= 0:
    #     word2 = sent[i - 3]
    #     features.extend([
    #         '-3:word=' + word2.lower(),
    #         '-2.isdigit=%s' % word2.isdigit(),
    #     ])
    # else:
    #     features.append('BOS')

    if i < len(sent) - 1:
        word1 = sent[i + 1]
        features.extend([
            '+1:word=' + word1.lower(),
            '+1.isdigit=%s' % word.isdigit(),
        ])
    else:
        features.append('EOS')
    if i < len(sent) - 2:
        word1 = sent[i + 2]
        features.extend([
            '+2:word=' + word1.lower(),
            '+2.isdigit=%s' % word.isdigit()
        ])
    else:
        features.append('EOS')
    # if i < len(sent) - 3:
    #     word1 = sent[i + 3]
    #     features.extend([
    #         '+3:word=' + word1.lower(),
    #         '+2.isdigit=%s' % word.isdigit()
    #     ])
    # else:
    #     features.append('EOS')
    return features


def sent2features(sent, train_word):
    return [word2features(sent, i, train_word) for i in range(len(sent))]


def sent2labels(sent, train_word):
    rs = [str(config_labels[train_word][token.lower()]) if unidecode(token).lower() == train_word else 'WORD' for
          token in sent]
    return rs


def run(train_word):
    total_item = db_text.find({"s": train_word}).count()
    print(train_word, total_item, config_labels[train_word])
    model_name = './models/%s.crfsuite' % train_word
    if os.path.isfile(model_name):
        return ''
    trainer = pycrfsuite.Trainer(verbose=False, algorithm='ap')
    test_x, test_y = [], []
    if total_item <= 0:
        return None
    item_full = db_text.find({"s": train_word.lower()}).limit(LIMIT)
    for item in item_full:
        if len(item['n']) != len(item['s']):
            continue
        try:
            rt_labels = sent2labels(item['n'], train_word)
            rt_feature = sent2features(item['s'], train_word)
            if DEBUG and random.randint(0, 100) < 30:
                test_x.append(rt_feature)
                test_y.append(rt_labels)
            else:
                trainer.append(rt_feature, rt_labels)
        except Exception as e:
            pass
    trainer.set_params({
        'max_iterations': 1000,
        'feature.possible_transitions': True,
        'feature.possible_states': True,
    })
    trainer.train(model_name)
    # tagger = pycrfsuite.Tagger()
    # tagger.open(model_name)
    #
    # y_pred = [tagger.tag(x) for x in test_x]
    # if y_pred and test_x:
    #     print(bio_classification_report(test_y, y_pred))


if __name__ == '__main__':
    number_process = 1
    LIMIT = 10000
    DEBUG = False
    pool = Pool(number_process)
    keys = list(config_labels.keys())
    pool.map(run, keys)
