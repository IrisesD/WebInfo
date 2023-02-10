import gzip
import copy
import json
#======================================================================================
def filter(triples_2,min_rel: int,max_show: int,min_show: int):
    entities_2 = {} #记录实体出现次数
    relations_2 = {} #记录关系出现次数
    for head in triples_2.keys():
        rel_dict = triples_2[head]
        cnt = 0
        for rel in rel_dict.keys():
            if rel not in relations_2.keys():
                relations_2[rel] = 0
            else:
                relations_2[rel] += 1
            tail_dict = rel_dict[rel]
            cnt += len(tail_dict)
        entities_2[head] = cnt
    print("删除出现少于 ",min_rel," 次的关系")
    i = 0
    j = 0
    for key in relations_2.keys():
        if relations_2[key] < min_rel:
            i += 1
            for head in triples_2.keys():
                rel_dict = triples_2[head]
                if key in rel_dict.keys():
                    del triples_2[head][key]
                    j += 1
    print("删除关系数:",i,j)
    i=0
    j =0
    for key in entities_2.keys():
        if entities_2[key] not in mvi_entities:
            if entities_2[key] <min_show:
                i+=1
            elif entities_2[key] >max_show:
                j+=1
    print("小于min_show: ",i,"大于max_show: ",j)
    print("删除一跳图出现超过",max_show,"次的实体,并且只采样",min_show,"核")
    j = 0 
    triples_2_temp = copy.deepcopy(triples_2)
    for key in entities_2.keys():
        if key not in mvi_entities:
            if (entities_2[key] > max_show or entities_2[key] < min_show):
                j += 1
                rel_dict = triples_2[key]
                for rel in rel_dict.keys():
                    tail_dict = rel_dict[rel]
                    for tail in tail_dict.keys():
                        if tail in triples_2_temp.keys():
                            if rel in triples_2_temp[tail].keys():
                                del triples_2_temp[tail][rel][key]
                del triples_2_temp[key]
    del triples_2
    print("删除实例数:",j)
    del_entities_num = j
    return triples_2_temp, del_entities_num
#======================================================================================
tag_info_fpath = "Movie_tag.csv"
entity_info_fpath = "douban2fb.txt"
freebase_info_fpath = "freebase_douban.gz"
outfile = "graph_2step.json"

mvi_entities = []
with open(entity_info_fpath, 'r') as f:
    for line in f:
        entity = line.strip().split('\t')[-1]
        mvi_entities.append(entity)
        
entities = {} #记录实体出现次数
relations = {} #记录关系出现次数

template_str = "http://rdf.freebase.com/ns/"
with gzip.open(freebase_info_fpath,'rb') as f:
    for line in f:
        line_info = line.decode().split('\t')
        # 过滤不含有template前缀的实体
        if template_str not in line_info[2]:
            continue
        # 提取"http://rdf.freebase.com/ns/"之后的内容:
        # 头实体
        head = line_info[0][len(template_str)+1:].strip('>')
        if head not in entities.keys():
            entities[head] = 0
        else:
            entities[head] += 1
        # 关系
        rel = line_info[1][len(template_str)+1:].strip('>')
        if rel not in relations.keys():
            relations[rel] = 0
        else:
            relations[rel] += 1
        # 尾实体 
        tail = line_info[2][len(template_str)+1:].strip('>')
        if tail not in entities.keys():
            entities[tail] = 0
        else:
            entities[tail] += 1

triples_1 = {} #记录第一跳初始图

template_str = "http://rdf.freebase.com/ns/"
with gzip.open(freebase_info_fpath,'rb') as f:
    for line in f:
        line_info = line.decode().split('\t')
        # 过滤不含有template前缀的实体
        if template_str not in line_info[2]:
            continue
        # 提取"http://rdf.freebase.com/ns/"之后的内容:
        # 关系
        rel = line_info[1][len(template_str)+1:].strip('>')
        if relations[rel] < 50:
            continue
        # 头实体与尾实体 
        head = line_info[0][len(template_str)+1:].strip('>')
        tail = line_info[2][len(template_str)+1:].strip('>')
        if head not in mvi_entities and (entities[head] < 20 or entities[head] > 20000):
            continue
        if tail not in mvi_entities and (entities[tail] < 20 or entities[tail] > 20000):
            continue
        
        if head not in triples_1.keys():
            triples_1[head] = {}
        if tail not in triples_1.keys():
            triples_1[tail] = {}
        if rel not in triples_1[head].keys():
            triples_1[head][rel] = {}
        if rel not in triples_1[tail].keys():
            triples_1[tail][rel] = {}
        triples_1[head][rel][tail] = {}
        triples_1[tail][rel][head] = {}

triples_2 = copy.deepcopy(triples_1)
while(len(triples_2.keys())>2000):
    triples_2, del_entities_num = filter(triples_2,min_rel = 70,max_show = 150,min_show = 15)
    print(len(triples_2.keys()))
    for item in mvi_entities:
        if item not in triples_2.keys():
            print(item)
    if del_entities_num == 0:
        break

for head in triples_2.keys():
    rel_dict = triples_2[head]
    for rel in rel_dict.keys():
        tail_dict = rel_dict[rel]
        for tail in tail_dict:
            triples_2[head][rel][tail] = triples_1[tail]
            
with open(outfile, 'w') as f:
    json.dump(triples_2, f)
print("done")