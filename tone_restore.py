import pycrfsuite
from addtone_crf import sent2features
from tokens import split_sent_postag
import time
import os
import json

tic = time.time()

with open('./config_tone.json', 'r') as fs:
    blabels = json.load(fs)
config_labels = {}

for k, v in blabels.items():
    rev = {}
    for _k, _v in v.items():
        rev[str(_v)] = _k
    config_labels[k] = rev

tests = [
    'coi niet ban',
    'dai ca',
    'anh ay that la vi dai'
]
tic = time.time()

for test in tests:
    test = split_sent_postag(test)
    test_clone = test[:]
    for index, token in enumerate(test):
        token_lower = token.lower()
        model_name = './models/%s.crfsuite' % token_lower
        if not os.path.isfile(model_name):
            continue
        tagger = pycrfsuite.Tagger()
        tagger.open(model_name)
        x_test = sent2features(test, train_word=token_lower)
        print(x_test)
        rs = tagger.tag(x_test)
        # result = numpy.zeros(len(tagger.labels()))
        # for idx, label in enumerate(tagger.labels()):
        #     pro = ['WORD' for token in test]
        #     pro[index] = label
        #     result[idx] = tagger.probability(pro)
        #     print(result)
        if rs[index] != 'WORD':
            test_clone[index] = "[%s]" % config_labels[token_lower][rs[index]]
    print(" ".join(test_clone))
print(time.time() - tic)
