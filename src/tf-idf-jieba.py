import jieba.analyse

file_name = '../data/笑傲江湖.txt'
topK = 50
content = open(file_name, 'rb').read()

tags = jieba.analyse.extract_tags(content, topK=topK)

print(", ".join(tags))
