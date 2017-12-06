import jieba.analyse

file_name = '../data/創世記/创世记01.txt'
topK = 10
content = open(file_name, 'rb').read()

print('tf-idf : ')
for x, w in jieba.analyse.extract_tags(content, withWeight=True, topK=topK):
    print('%s %s' % (x, w))

# print('TextRank : ')
# for x, w in jieba.analyse.textrank(content, withWeight=True, topK=topK):
#     print('%s %s' % (x, w))
