import jieba.analyse

file_name = '../data/笑傲江湖/40.txt'
topK = 10
content = open(file_name, 'rb').read()

jieba.analyse.set_stop_words('./dictionary/stop_words.txt')

print('tf-idf : ')
for x, w in jieba.analyse.extract_tags(content, withWeight=True, topK=topK):
    print('%s %s' % (x, w))

# print('TextRank : ')
# for x, w in jieba.analyse.textrank(content, withWeight=True, topK=topK):
#     print('%s %s' % (x, w))
