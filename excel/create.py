# -*- coding: utf-8 -*-  
#!/usr/bin/python

import xlrd
import xlwt
import openpyxl
import random

def get_file_names(files, num):
    file_names = []
    file_total_num = len(files)

    index_all = random.sample(range(0, file_total_num), num)
    for index in index_all:
        file_names.append(files[index])

    return file_names

def run(path):
    num_view1 = [
        [3, 4],
        [5, 2],
        [6, 4],
        [5, 4],
        [4, 3],
        [4, 1],
        [3, 4],
        [4, 4],
        [1, 2],
        [4, 1],
        [7, 4],
        [6, 3],
        [7, 4],
        [6, 2],
        [4, 3],
        [1, 2],
        [5, 3],
        [7, 1],
        [1, 2],
        [7, 2],
        [4, 1],
        [6, 4],
        [4, 4],
        [6, 1],
        [6, 3],
        [5, 4],
        [2, 1],
        [5, 1],
        [1, 1],
        [2, 3],
        [6, 2],
        [4, 4],
        [5, 4],
        [1, 2],
        [4, 1],
        [3, 3],
        [4, 4],
        [1, 4],
        [4, 4],
        [3, 2],
        [4, 4],
        [6, 1],
        [4, 1],
        [4, 3],
        [5, 3],
        [4, 3],
        [5, 2],
        [5, 3],
        [2, 2],
        [5, 4],
        [2, 4],
        [3, 3],
        [3, 3],
        [4, 4],
        [5, 3],
        [2, 3],
        [5, 4],
        [5, 1],
        [6, 3],
        [4, 2],
        [3, 3],
        [5, 4],
        [5, 3],
        [4, 3],
        [8, 2],
        [2, 2],
        [3, 4],
        [3, 1],
        [5, 4],
        [1, 3],
        [4, 1],
        [4, 3],
        [4, 1],
        [5, 1],
        [1, 2],
        [5, 4],
        [1, 2],
        [5, 1],
        [8, 1],
        [2, 4],
        [3, 1],
        [6, 4],
        [6, 4],
        [1, 2],
        [7, 3],
        [3, 4],
        [6, 4],
        [1, 4],
        [8, 1],
        [3, 2],
        [1, 3],
        [4, 1],
        [7, 1],
        [6, 3],
        [6, 3],
        [5, 1],
        [2, 3],
        [6, 1],
        [5, 2],
        [7, 4],
        [8, 2],
        [6, 2],
        [7, 2],
        [6, 1],
        [4, 2],
        [1, 3],
        [2, 4],
        [5, 3],
        [8, 3],
        [5, 2],
        [4, 3],
        [4, 3],
        [5, 3],
        [4, 3],
        [7, 3],
        [5, 2],
        [5, 1],
        [4, 1],
        [4, 3],
        [4, 2],
        [7, 4],
        [1, 4],
        [5, 4],
        [4, 1],
        [1, 1],
        [5, 2],
        [4, 2],
        [7, 1],
        [7, 4]]

    num_view2 = [
        [3, 4],
        [1, 4],
        [5, 4],
        [6, 3],
        [1, 4],
        [7, 1],
        [2, 2],
        [6, 2],
        [3, 4],
        [4, 3],
        [5, 3],
        [3, 2],
        [5, 4],
        [4, 1],
        [5, 3],
        [5, 1],
        [4, 2],
        [5, 2],
        [1, 1],
        [5, 1],
        [4, 1],
        [5, 3],
        [2, 1],
        [7, 1],
        [4, 2],
        [6, 2],
        [3, 4],
        [3, 2],
        [3, 1],
        [5, 2],
        [5, 3],
        [3, 4],
        [5, 1],
        [1, 4],
        [7, 2],
        [4, 4],
        [7, 3],
        [5, 1],
        [3, 2],
        [5, 3],
        [5, 3],
        [3, 2],
        [3, 4],
        [3, 2],
        [2, 2],
        [5, 3],
        [6, 1],
        [5, 1],
        [1, 3],
        [3, 1],
        [2, 2],
        [5, 4],
        [5, 4],
        [2, 4],
        [6, 3],
        [4, 2],
        [4, 4],
        [3, 3],
        [3, 4],
        [4, 3],
        [3, 4],
        [2, 3],
        [6, 3],
        [1, 1],
        [5, 1],
        [5, 2],
        [4, 3],
        [5, 4],
        [1, 4],
        [3, 4],
        [4, 1],
        [1, 4],
        [3, 4],
        [2, 1],
        [4, 4],
        [1, 4],
        [3, 4],
        [6, 3],
        [7, 3],
        [5, 4],
        [4, 4],
        [1, 4],
        [5, 4],
        [5, 1],
        [4, 1],
        [5, 3],
        [6, 4],
        [5, 3],
        [7, 2],
        [2, 4],
        [3, 3],
        [5, 2],
        [5, 3],
        [5, 2],
        [3, 2],
        [6, 3],
        [5, 1],
        [5, 3],
        [1, 1],
        [6, 2],
        [6, 3],
        [2, 2],
        [4, 3],
        [7, 2],
        [7, 1],
        [1, 2],
        [2, 3],
        [3, 1],
        [6, 3],
        [1, 2],
        [5, 1],
        [5, 3],
        [6, 1],
        [2, 3],
        [6, 3],
        [4, 4],
        [6, 3],
        [4, 2],
        [6, 3],
        [3, 3],
        [6, 2],
        [3, 4],
        [6, 4],
        [5, 1],
        [4, 1],
        [4, 2],
        [4, 1],
        [3, 3],
        [3, 2]]

    view1_ok_files = {
        '混合需求驱动的文内视觉资源移动视觉搜索框架',
        '本体构建中的协同问题研究——以中华人民共和国史本体为例',
        '基于语义分析的产品分类本体查询研究',
        '领域本体术语的抽取方法研究',
        '基于SNOMED',
        'CT和FCA的医学领域本体构建研究',
        '面向学科领域的学术文献语义标注框架研究',
        '基于本体的人物关系一致性检测方法研究',
        '基于主题词表与百科知识相融合的领域本体自动构建研究',
        '基于语义一致性的多层本体元模型构建方法研究',
        '基于本体和NoSQL的机械产品方案设计的知识表示与存储研究',
        '基于哈斯图的本体偏序关系消冗方法研究',
        '基于本体概念相似度的网页排序算法研究'
    }

    view1_fail_files = {
        '利用领域本体提高信息对称性的研究',
        '文摘创新点的语义本体模型研究',
        '本体映射系统的评价体系研究',
        '基于领域本体的数字文献资源聚合及服务推荐方法研究',
        '本体评估研究进展',
        '面向本体学习的中文专利术语抽取研究',
        '本体进化驱动的个性化语义搜索研究',
        '基于领域本体的网络口碑传播动机识别',
        '基于VSM和偏好本体的个性化信息检索技术的研究',
        '专利领域本体概念语义层次获取',
        '领域本体与社群分类法结构中心性的比较研究',
        '基于数据科学的知识创新服务应用模式构建研究',
        '数据驱动的企业多层竞争网络构建与态势分析',
        '基于共期刊学科类间关系构建全学科科学骨架图',
        '基于网络叙词表的图情学科SKOS构建与可视化研究',
        '基于概念匹配的数字图书馆关联数据的关联构建',
        '突发事件驱动的应急情报分析框架构建',
        '基于生命周期的应急情报体系理论模型构建',
        '多维视角下应急情报管理体系的知识库构建研究',
        '论基于“三大研究范式”之上的当代中国情报学学科体系与学科群体系构建',
        '基于共现潜在语义向量空间模型的语义核构建',
        '应急参考咨询团队构建模式研究',
        '基于专利特征抽取的技术树构建方法研究',
        '基于形式概念分析的学科术语层次关系构建研究',
        '科技报告集成管理系统构建',
        '基于向量空间模型的标签树构建方法研究',
        '当代情报学哲学的主要观点及其理论体系构建',
        '面向知识服务的知识组织框架体系构建',
        '突发公共卫生事件网络语料库系统构建',
        '基于海量数字资源的科研关系网络构建探究',
        '基于社会资本的异构社会网络构建研究',
        '对等网环境下基于树模型的对等节点的知识地图构建研究',
        '简论国家信息政策体系构建',
        '基于校园网的文献服务模型及信息网络构建技术',
        '基于DRM技术的电子书服务模式的构建',
        '构建基于数字化图书馆的智能化数据库系统',
        '动态网站管理信息系统的构建',
        '信息服务的社会监督(Ⅰ)——信息服务监督的社会化发展与社会监督体系的构建',
        '信息检索类别分析与构建',
        '数字图书馆资源知识聚合可视化模型构建研究',
        '科学数据共享行为的理论模型构建及测度实证研究',
        '线上商品评论有效性分类专业领域知识模型的构建研究',
        '国家科技管理信息系统构建及其对科技情报工作的影响',
        '科技项目查重系统构建研究',
        '技术创新过程的基因图谱构建及其实证',
        '基于关联规则挖掘和极性分析的商品评论情感词典构建',
        '面向情报流程的情报方法体系构建',
        '情报分析:定义、意义构建与流程',
        '立足情报服务',
        '借力工程思维:大数据时代情报工程学的理论构建',
        '融合结构与内容特征的微博沉默用户兴趣模型构建研究',
        '科技文献检索中基于主题词表分面化改造的分面构建',
        '基于信息生态学的微博舆论生态系统构建与机理研究'
    }

    view2_ok_files = {
    '面向阅读推广的微博用户转发行为预测',
    '基于微博用户创作内容的新闻线索自动发现研究',
    '探究微博用户原创信息分享行为——基于冲动行为视角',
    '微博社会网络及传播研究评述',
    '微博用户在突发事件中转发行为研究:基于信息源的视角',
    '结合用户关系网和标签共现网的微博用户标签推荐研究',
    '基于用户感知、偏好和涉入的微博舆情传播意愿影响因素研究',
    '微博机制和转发预测研究',
    '融合结构与内容特征的微博沉默用户兴趣模型构建研究',
    '基于社会网络关系的微博个性化推荐模型'
    }

    view2_fail_files = {
        '基于LDA和随机森林的微博谣言识别研究——以2016年雾霾谣言为例',
        '基于贝叶斯模型的移动环境下网络舆情用户情感演化研究——以新浪微博“里约奥运会中国女排夺冠”话题为例',
        '基于种群密度的微政务信息公开共生演化研究',
        '基于卷积神经网络的微博舆情情感分类研究',
        '突发公共卫生事件利益相关者在社交媒体中的关注点及演化模式',
        '科学推文作者行为模式与地理分布研究',
        '新媒体环境下的网络舆情特征量及行为规律研究——基于信息生态理论',
        '基于深度学习和OCC情感规则的网络舆情情感识别研究',
        '基于微博公众情感状态的新产品市场预测研究',
        '基于情境推演的微博突发事件预测模型研究',
        '中文微博作者身份识别研究',
        '基于SVM的中文微博观点倾向性识别',
        '考虑互惠边的微博网络信息传播模型及最有影响力节点排序算法',
        '新媒体环境下网络舆情演化模型及仿真研究——基于信息生态视角',
        '基于微博用户创作内容的新闻线索自动发现研究',
        '基于修正G~2特征筛选的中文微博情感组合分类',
        '基于社会网络分析的微博社区网络结构及传播特性研究',
        '探究微博用户原创信息分享行为——基于冲动行为视角',
        '基于迁移学习微博情绪分类研究——以H7N9微博为例',
        '基于链路结构的微博领域专家识别研究',
        '基于新浪热门平台的微博热度评价指标体系实证研究',
        '微博社会网络及传播研究评述',
        '融合结构与内容特征的微博沉默用户兴趣模型构建研究',
        '基于迭代策略的微博事件查询扩展方法',
        '微博用户在突发事件中转发行为研究:基于信息源的视角',
        '基于信息生态学的微博舆论生态系统构建与机理研究',
        '结合用户关系网和标签共现网的微博用户标签推荐研究',
        '基于扫描统计量的微博中突发事件舆情动态监测方法',
        '一种基于新闻学的微博事件特征选择方法',
        '危机事件中的微博意见领袖影响因素实证研究',
        '基于单句粒度的微博主题挖掘研究',
        '基于社会网络关系的微博个性化推荐模型',
        '基于用户感知、偏好和涉入的微博舆情传播意愿影响因素研究',
        '基于ELM模型的微博舆情传播影响因素研究——以新浪微博为例',
        '面向中文微博的观点句识别研究',
        '基于新词扩充和特征选择的微博观点句识别方法',
        '微博机制和转发预测研究',
        '基于潜在狄利克雷分配模型的微博主题演化分析',
        '突发事件新闻报道与微博信息的爆发性模式比较',
        '基于学术论文全文内容的算法使用行为及其影响力研究',
        '基于认知风格的数字图书馆用户信息检索行为研究',
        '微信群内部信息交流的网络结构、行为及其演化分析——基于会话分析视角',
        '基于扎根理论的社会化问答社区用户知识贡献行为意向影响因素研究',
        '移动经验取样法:促进真实情境下的用户信息行为研究',
        '社交网络群组用户知识共享行为动机研究:以Facebook Group和微信群为例',
        '高校学生网络行为时序特征的可视化分析',
        '基于情景化用户偏好的学术信息行为研究述评',
        '基于结构方程的知识型微信社群用户参与动机和参与行为关联性分析',
        '移动环境下融合情境信息的群组推荐模型研究——基于用户APP行为数据的实证分析',
        '科学推文作者行为模式与地理分布研究',
        '新媒体环境下的网络舆情特征量及行为规律研究——基于信息生态理论',
        '面向阅读推广的微博用户转发行为预测',
        '微信学术检索用户行为分析与实证研究',
        '学术专著引用行为研究——基于引文内容特征分析的视角',
        '生物信息学文献中的科学软件利用行为研究',
        '任务复杂性与用户认知和Web导航行为关系探究',
        '科学数据的引用行为及其影响力研究',
        '学术博客用户的博文分类行为研究——以科学网博客为例',
        '科学数据共享行为的理论模型构建及测度实证研究',
        '不同任务类型下查询重构行为分析',
        '移动社交网络用户内容创造与分享行为研究——社会网络与自恋的交互效应',
        '探究微博用户原创信息分享行为——基于冲动行为视角',
        '基于知识超网络的科研合作行为实证研究和建模',
        '社交媒体后续采纳阶段用户转移行为研究——以微信为例',
        '时间限制对用户搜索交互行为的影响及其预测',
        '信息浏览行为是理论导向抑或生物驱动?——基于眼动仪实验的实证分析',
        '大数据环境下科技文献用户阅读行为知识组织模型研究',
        '基于技术接受模型的微信用户信息发布行为研究',
        '微博用户在突发事件中转发行为研究:基于信息源的视角',
        '基于个体行为的科研合作网络知识扩散建模研究',
        '青少年用户移动阅读采纳行为实证研究',
        '学术团队合作信息查寻与检索行为的影响因素实证研究',
        '基于国外图书情报领域六种主流期刊的网络信息行为研究综述',
        '基于多智能体的网络百科用户贡献行为的动态特性',
        '基于CART分类方法的期刊操纵引用行为识别建模研究',
        '网络视频服务用户内容生成上传行为意愿实证研究',
        '信息技术条件下的消费者行为特征',
        '竞争情报行为的正当性与灰色信息收集方式的研究',
        '一种应用言语行为理论的新闻篇章理解与摘要生成方法',
        '市民信息需求与利用行为的调查分析',
        '论情报需要与情报行为的互逆过程',
        '一类用户情报行为的统计拟合',
        '试探行为科学与情报学的相关性',
        '多特征融合的中文命名实体链接方法研究',
        '世界一流大学竞争力与科研产出计量学特征的相关性研究',
        '不同特征下的学术文本结构功能自动识别研究',
        '高校学生网络行为时序特征的可视化分析',
        '基于文献共被引特征的文献相似度计算优化研究',
        '引文生态视角下标准必要专利的引文特征研究',
        '五种关联强度指标对研究前沿时间特征的识别',
        '基于表示学习的跨模态检索模型与特征抽取研究综述',
        '社交媒体健康信息质量研究:基于真伪健康信息特征的分析',
        '生命周期阶段中的科学合作网络演化及高影响力学者成长特征研究',
        'C9联盟与世界一流大学联盟信息计量学特征研究',
        '新媒体环境下的网络舆情特征量及行为规律研究——基于信息生态理论',
        '3S引文现象的特征测度及学术意义——“睡美人”、“时髦女”与“天鹅”综论',
        '基于LDA模型特征选择的在线医疗社区文本分类及用户聚类研究',
        '论文标题特征与被引的关联性研究',
        '追根溯源:优秀科学计量学家引用的重要文献识别及引用内容特征研究',
        '基于多特征时间抽取模型的食品安全事件演化序列生成研究',
        '电子商务领域的科学特征与技术特征比较——文献计量视角',
        '基于联合聚类与用户特征提取的协同过滤推荐算法',
        '基于条件随机场模型的“评价特征-评价词”对抽取研究',
        '基于混合内容线索特征的语义组块标注研究',
        '基于二进制烟花算法的特征选择方法',
        '学术专著引用行为研究——基于引文内容特征分析的视角',
        '基于案例-规则检索的特征阈值选择模型',
        '医学图像模态特征表达及其比较研究',
        '届满专利与无效专利的施引特征对比及其情报学意义',
        '一种基于网络评论的商品特征挖掘方法'
    }

    wb = xlwt.Workbook()
    sheet = wb.add_sheet("view1")
    sheet.write(0, 0, "所有文章")

    index = 1
    for item in num_view1:
        file_view1_ok = get_file_names(view1_ok_files, item[0])
        file_view1_fail = get_file_names(view1_fail_files, item[1])
        file_view1_ok.append(file_view1_fail)
        sheet.write(index, 0, file_view1_ok)
        index = index + 1

    index = 1
    for item in num_view2:
        file_view2_ok = get_file_names(view2_ok_files, item[0])
        file_view2_fail = get_file_names(view2_fail_files, item[1])
        file_view2_ok.append(file_view2_fail)
        sheet.write(index, 0, file_view2_ok)
        index = index + 1

    wb.save(path)


if __name__ == "__main__":
    run('./file_names.xls')