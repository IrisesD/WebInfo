import json
import jieba
import jieba.posseg
import jieba.analyse
import re
from Pretreatment import Sparse

PostingList = [0]
WordMap = {}
PL_word_num = 0

filename='data/data.json'
create_PL_file_path='data/PostingList.json'
create_WordMap_file_path='data/WordMap.json'

with open(filename,encoding='utf-8') as f:
    json_data=json.load(f)
for box in json_data:
    #-----<预处理>-----
    #获取基本信息：片面和简介
    movie_info=box["name"]
    movie_info+=box["intro"]
    #获取类型信息
    sentences = box['info'].split('\n')
    for i in range(len(sentences)-1,-1,-1):
        if "类型" in sentences[i]:
            movie_info+=sentences[i]
            break
    #删除所有英文
    pattern = re.compile("[\u4e00-\u9fa5]")
    movie_info="".join(pattern.findall(movie_info))
    #开始分词
    _sparse=Sparse(movie_info)
    box_words = _sparse.sparse()
    #支持搜索作品豆瓣id和rating
    box_words.append(box['id'])
    sentences = box['rating'].split('\n')
    for i in range(len(sentences)):
        if "." in sentences[i]:
            box_words.append(sentences[i])
            break
    #将完整片名加上
    box_words.append(box['name'].split(' ')[0])
    #-------<Posting List>---------
    for word in box_words:
        if word in WordMap:
            word_id = WordMap[word]
            first_id=str(''.join(PostingList[word_id][0]))
            id_gap=int(box['id'])-int(first_id)
            PostingList[word_id].append(str(id_gap))
        else:
            PL_word_num += 1
            WordMap[word] = PL_word_num
            PostingList.append([])
            PostingList[PL_word_num].append(box["id"])

PostingList[0] = PL_word_num
jsonPostingList = json.dumps(PostingList)
file1 = open(create_PL_file_path, 'w')
file1.write(jsonPostingList)
file1.close()

jsonWordMap = json.dumps(WordMap)
file2 = open(create_WordMap_file_path, 'w')
file2.write(jsonWordMap)
file2.close()
print(PostingList)
print(WordMap)
f.close()
