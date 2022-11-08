# 环境
#### & jieba
[fxsjy/jieba: 结巴中文分词 (github.com)](https://github.com/fxsjy/jieba)
```
conda/pip install jieba
```
#### & Synonyms
[chatopera/Synonyms: 中文近义词：聊天机器人，智能问答工具包 (github.com)](https://github.com/chatopera/Synonyms)
```
pip install -U synonyms
python -c "import synonyms" # download word vectors file
```

---
# 运行
```{shell}
#先在build_PL.py中将小说或电影的文件设置

python build_PL.py 
#里面import了Pretreatment.py文件，最终生成
#PostingList.json, WordMap.json文件

python bool_search.py
#进行查询
```

----
# 方法

## # 1.预处理
##### ；打标信息来源
1. ['name']
2. ['info']从中获取书籍、电影类型
3. ['intro']
4. ['id']可搜豆瓣id
5. ['rating']可搜评分
介于文本特征、时间成本和最终效果，本次任务不考虑任何英语搜索，于是去掉所有英文。

##### ；自定义词典
手动定义一些不用分割的词（比如”摩根·弗里曼“的“弗里曼”，是否添加随缘）到`add_word_list.txt`中，调用`jieba.load_userdict(add_word_file)`。

##### ；去除停用词
停用词词典用的是[goto456/stopwords: 中文常用停用词表（哈工大停用词表、百度停用词表等） (github.com)](https://github.com/goto456/stopwords)里的中文停用词词典，在jieba全模式分割后，参考停用词文件进行剔除。

以下为实际效果。
去除前：
![[jieba-full-mode.png]](./img/jieba-full-mode.png)
去除后：
![[rm-stop-words.png]](./img/rm-stop-words.png)
可以看到，如“了”、“下”等停用词被剔除。

##### ；去除重复、同义词
方法：采用`import synonyms`，通过compare两个词的相似度而决定是否合并
下图为实际效果：
![[merge-synonyms.png]]
可以看到，许多重复的词（比如“救赎”等）被删掉。

## # 2.倒排链表的建立和压缩

1. 建立：先对得到的词进行map映射，每个词有自己的`word_id`，将相关文档的id附在`PostingList[word_id]`上。
2. 压缩：采用了间距代替。
效果如下：
![[postingList.png]](./img/postingList.png)

## # 3.bool查询
1. 载入文件
	1. 倒排.json
	2. WordMap.json
	3. book/movie.json
2. 查询语句处理
	1. 递归分解
	2. 优先级：NOT AND OR
3. 输出相关信息

----
# 结果分析与展示

本组组员学号后两位：12、15、61
TOP250电影相关的有12、15、61、112、115、161、212、215

12 -《楚门的世界》：”初恋“，”剧情“

15 - 《机器人总动员》：”飞船“

61 - 《搏击俱乐部》：”俱乐部“，”剧情“

112 -《幽灵公主》：”奇幻“，”森林“

115 -《小森林》：”森林“、”剧情“

161 - 《三块广告牌》：”剧情“，”广告“，”翻天覆地“

212 - 《心灵奇旅》：”奇幻“，”二十二“，”俱乐部“

215 - 《青蛇》：”奇幻“，”剧情“，”南宋“

搜索”飞船 OR ( 剧情 AND 广告 ）“
![[search-1.png]](./img/search-1.png)
得到《机器人总动员》和《三块广告牌》

搜索”森林 AND 奇幻 OR 女朋友“
![[search-2.png]](./img/search-2.png)
得到《幽灵公主》

搜索”剧情 AND NOT (翻天覆地 OR 初恋 OR 俱乐部)“
![[search-3.png]](./img/search-3.png)
得到《小森林》和《青蛇》
