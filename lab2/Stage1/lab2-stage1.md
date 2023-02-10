# # stage1

##### ；记录电影对应实例
防止过滤时将实例删除:
```
entity_info_fpath = "douban2fb.txt"
mvi_entities = []
with open(entity_info_fpath, 'r') as f:
    for line in f:
        entity = line.strip().split('\t')[-1]
        mvi_entities.append(entity)
```
##### ；记录freebase中各实体、关系出现次数
```
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
```
##### ；一跳图
只保留至少出现在 20 个、最多出现在2w个三元组中的实体，以及超过 50 次的关系：
```
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
## EX：
# > 可乐 品牌 可口
#  {可乐：{品牌:{可口:{}}}}
#  {可口：{品牌:{可乐:{}}}}
# > 可乐 品牌 百事
#  {可乐：{品牌:{可口:{},百事:{}}}}
#  {可口：{品牌:{可乐:{}}}}
#  {百事：{品牌:{可乐:{}}}}
# > 可口 adj 食物
#  {可乐：{品牌:{可口:{},百事:{}}}}
#  {可口：{品牌:{可乐:{}}, adj:{食物:{}}}}
#  {百事：{品牌:{可乐:{}}}}
#  {食物：{品牌:{可口:{}}}}
# 结构：<key>: <value>
#                |
#                ->dict
#                ->{r1:<value>,r2:<value>,...}
#                         |
#                         ->dict
#                         ->{e1:<value>,e2:<value>,...}
```
##### ；二跳图
1. 删除出现次数少于70次的关系
2. 删除出现次数少于15多于150的实例
3. 重复1直至实例数降到2000以下
4. 产生二跳图
```
for head in triples_2.keys():
    rel_dict = triples_2[head]
    for rel in rel_dict.keys():
        tail_dict = rel_dict[rel]
        for tail in tail_dict:
            triples_2[head][rel][tail] = triples_1[tail]
```
最终规模为：
1. 实体数量（包含578个电影实体）为1887
2. 关系数量为 35 个
3. 三元组数量为31894个






