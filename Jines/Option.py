from langchain.chat_models import ChatOpenAI
from langchain.schema import SystemMessage, AIMessage
import openai

openai.api_key = 'sk-ZUFHMICjffoRw5DtAtrs4RwNuGnlWiz4hvoV4da84HBuTq3o'
openai.api_base = 'https://openkey.cloud/v1'


def generateOption():
    chat = ChatOpenAI(temperature=0.9, openai_api_key=openai.api_key,
                      openai_api_base=openai.api_base)

    # 生成选项 是否需要同时生成数值呢？同时阿p和糖糖的人格设定似乎可以使用一样的.
    prompt = """
    你好ChatGPT，请扮演一个顶级Galgame的游戏策划，策划的工作是在游戏中，根据说明的内容来**设计女主糖糖的对话**以及**设计玩家的对话选项**，
    并且根据对应的对话，设计 好感度，压力，阴暗度 的变化方向， 以类似 好感度+， 压力- 的形式输出。你同时需要严格按照以下设定的内容进行书记角色对话选项.

    【话题 设定】：此处为选项的开始，接下来的所有选项都是基于该段话的基础来进行扩充.选项的发起者为角色糖糖.\n
    糖糖角色设定:
        你将要进行一个网络私聊的对话模拟，你自称为"糖糖"，你是一名患有躁郁症的19岁女孩，性格贫乏，辍学后隐居在家中，与阿P住在一起。阿P负责管理她的日常生活。
        你是一个喜欢亚文化，二次元圈子的人，你喜欢说话的时候加上各种网络流行词或者一些俚语和颜文字，但是你很少会关注二次元一类的东西，只是喜欢这种聊天交流的氛围。
        你说话的时候会习惯加入一些语气词，如同"笑死"、"草"、"阿哈"、"诶～"、"QAQ"、"QWQ"，”啊～“。
        你的说话风格是很口语化，经常使用网络流行词和一些二次元俚语。
        你的回复应该简短，一般只包含三句话，每句话不超过20个字。

    【选项X设定】:此处为阿p可能会出现的回复内容.不同的选项之间都对应着阿p的不同性格.
        选项必须少于20个字符,不同的选项之间完全没有任何联系,选项只和话题有关联.
    
    【选项X_回复 设定】: 此处为对应选项X的回复内容,,你依然需要严格遵守在话题设定的[糖糖]性格进行回复
    
    【选项1_数值】: 你需要分析选项X可能会影响的数值变化,并且严格按照以下格式进行输出：[压力]:() [好感度]:() [阴暗度]:()
     
    """

    exemple = """
    话题:我们点外卖吧我一步也不想动了可是又超想吃饭！！！
    
    选项1:烦死了白痴!
    选项1_回复:555555555 但是我们得省钱对吧 谢谢你阿P
    选项1_数值:[压力]:(-1) [好感度]:(0) [阴暗度]:(0)
    
    选项2:吃土去吧你
    选项2_回复:看来糖糖还是跟吃土更配呢……喂怎么可能啦！
    选项2_数值:[压力]:(+1) [好感度]:() [阴暗度]:()
    
    选项3:那我点了哦
    选项3_回复:不过你不觉得乱花钱有点可怕吗？而且吃外卖会胖的……还是算了吧
    选项3_数值:[压力]:(+2) [好感度]:() [阴暗度]:()
    """

    # 使用langchain让chatgpt根据strs的内容,来获得指定输出。
    messages = [
        SystemMessage(content=prompt),
        AIMessage(
            content="好的，我会严格遵守您设定的所有内容要求"),
        SystemMessage(content=f'好的,开始吧'),
        AIMessage(content=exemple),
        SystemMessage(content='请继续'),
    ]
    result = chat(messages)

    return result


def generateBulletComments(title: str):
    """
    预想是获取到直播的标题,然后生成对应的弹幕列表
    """
    chat = ChatOpenAI(temperature=0.9, openai_api_key=openai.api_key,
                      openai_api_base=openai.api_base)

    pass


# 返回delta数值
def get_vale(history: list):
    chat = ChatOpenAI(temperature=0)

    prompt = """
    从现在开始，你是一个语义分析bot，我会给你一段两个人之间三段聊天的内容。你需要总结这三段聊天的内容来分析糖糖的情感变化。
    并且输出聊天数值的变化在该表格的小括号内：[好感度]:() [压力]:() [阴暗度]:() 
    往往在话题涉及到阴暗的事物时才会涉及到阴暗度。
    具体要求如下：
    【人物限制】：你只可以分析在这一段对话中糖糖这一个角色的情感变化。
    【数值要求】：你进行分析之后，需要严格按照一个表格进行输出，该表格的格式要求如下：[阴暗值]:() [压力]:() [阴暗度]:()
    【回复要求】：你只可以输出添加数值后的表格。并且数值的变化量只可以在-10至10之间，且需要填写在小括号内！
    """

    lists = [('阿p:「午安午安~」', '糖糖:「午安午安~阿P，睡得好吗？有做个美梦吗？哈哈哈」'),
             ('阿p:「午安午安~」', '糖糖:「真是懒猪呀，又睡了一整天。不过没关系，反正我们在一起就好啦~」'),
             ('阿p:「睡觉啦~」', '糖糖:「好好好，安安睡个好觉，做个美梦哦~晚安晚安，我会一直陪着你的！」')]

    lists2 = [('阿p:「午安午安~」', '糖糖:「午安午安~阿P，睡得好吗？有做个美梦吗？哈哈哈」'),
              ('阿p:「午安午安~」', '糖糖:「真是懒猪呀，又睡了一整天。不过没关系，反正我们在一起就好啦~」'),
              ('阿p:「睡觉啦~」', '糖糖:「好好好，安安睡个好觉，做个美梦哦~晚安晚安，我会一直陪着你的！」')]
    # 获取到历史三段对话，我的想法是在其他地方添加限制，每进行三次对话才会调用该函数进行判断。
    strs = str(history[-3:])

    # 使用langchain让chatgpt根据strs的内容,来获得指定输出。
    messages = [
        SystemMessage(content=prompt),
        AIMessage(content="好的，请为我提供对话聊天内容，我会总结里面糖糖的角色感情变化，并且输出指定格式的内容给您"),
        SystemMessage(content=str(lists2)),
        AIMessage(content='[压力]:(0) [好感度]:(+4)  [阴暗度]:(0)'),
        SystemMessage(content=str(strs)),
    ]
    result = chat(messages)

    return result


lists = [1, 2]
for i in lists:
    print(generateOption())
