import json
from langchain.chat_models import ChatOpenAI
from langchain.schema import SystemMessage, AIMessage
import openai


def to_jsonl(text, filename, id):
    # 分割文本为列表
    lines = text.split("\n")
    dialogs = []
    dialog = {}
    option = {}
    for line in lines:
        line = line.strip()
        if line.startswith("prefix"):
            dialog = {"prefix": line[7:].strip(), "options": [], "id": '', "category": ''}
            dialog["options"].append(option)
            dialogs.append(dialog)

        elif line.startswith("options"):
            dialog["options"].append(option)
            option = {"user": "", "reply": "", "attribute_change": ""}
        elif line.startswith("user"):
            option["user"] = line[5:].strip()
        elif line.startswith("reply"):
            option["reply"] = line[6:].strip()
        elif line.startswith("attribute_change"):
            option["attribute_change"] = line[17:].strip()

    if option:
        dialog["options"].append(option)
    if dialog:
        dialogs.append(dialog)

    with open(filename, 'a+', encoding='utf-8') as f:
        for entry in dialogs:
            json.dump(entry, f, ensure_ascii=False)
            f.write('\n')


# sk-xU8l4dplX16E3CUE3AM1`UWjBYcNZA0WMNznEbvpEwIitc09G
openai.api_key = 'sk-xA6WEmmj03pvw95jDf2a912eF27c4f87Bd379359B299AaDe'
openai.api_base = 'https://api.sirly.cc/v1'

'''
1. 生成多选项
2. 单行，多行无选项内容
3. 合并为单个option，自动生成options和reply，生成emoji
'''


def emoji_jsonl(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    option_time = 0

    decoder = json.JSONDecoder()
    chat = ChatOpenAI(temperature=0, openai_api_key=openai.api_key, openai_api_base=openai.api_base)
    for i in range(len(lines)):
        objs = []
        s = lines[i]
        while s:
            obj, pos = decoder.raw_decode(s)
            objs.append(obj)
            s = s[pos:].lstrip()

        for obj in objs:
            prefix = obj['prefix']
            # print('\nprefix: ', prefix)
            messages2 = [
                # 相当于我们提问前让chatgpt进行角色扮演
                SystemMessage(
                    content="从现在开始，你是一个情感分析bot，我会给你一段角色糖糖的对话，你需要将该段对话转换为emoji,"
                            "注意：emoji的范围包括情感和代表事物的emoji。"),
                AIMessage(content="好的，我会严格遵守你的要求,把用户的对话转换为emoji。"),
                SystemMessage(content='''
                糖糖:阿P，看！我买了小发发'
                '''),
                AIMessage(content="😊"),
                SystemMessage(content='''
                糖糖:糖糖好像累了……让糖糖休息一下好不好'
                '''),
                AIMessage(content="😣😢"),
                AIMessage(content="😊"),
                SystemMessage(content='''
                糖糖:房间太乱了 想买个扫地机器人 可是房间这么乱 买来也动不了'
                '''),
                AIMessage(content="🏘😓"),
                SystemMessage(content=f'''
                A:{prefix}'
                ''')
            ]
            obj['source'] = 'Original_Generation'
            if 'prefix_emoji' not in obj or obj['prefix_emoji'] == '':
                obj['prefix_emoji'] = chat(messages2).content
                print('\nprefix_emoji: ', obj['prefix_emoji'])
            else:
                pass
            if len(obj['options']) <= 1:
                print('prefix: ', prefix)

            for option in obj['options']:
                option_time += 1
                # 这里是生成emoji的部分，你可能需要根据你自己的需求来修改这部分的代码
                user = option['user']
                reply = option['reply']
                attribute_change = option['attribute_change']

                messages = [
                    # 相当于我们提问前让chatgpt进行角色扮演
                    SystemMessage(
                        content="从现在开始，你是一个情感分析bot，我会给你一段糖糖和阿P的对话记录和糖糖的情感变化数值，你需要仔细分析对话记录和情感变化数值,"
                                "然后输出一个emoji来表示糖糖当前的情感状态。"
                                "注意：你需要尽可能的扩大emoji的范围，既包括情感emoji，也包括代表事物的emoji"),
                    AIMessage(content="好的，我会严格遵守你的要求。"),
                    SystemMessage(content='''
                    糖糖:阿P，看！我买了小发发'
                    "阿P:真好看，跟糖糖好像"
                    "糖糖:对吧！我不在的时候，你就把小花花当成糖糖，好好疼爱它吧！"
                    "糖糖的感情数值变化：Stress: -1
                    '''),
                    AIMessage(content="😊💖"),
                    SystemMessage(content='''
                    糖糖:今天有点想试试平时不会做的事'
                    "阿P:相爱"
                    "糖糖:……我们不是一直相爱的吗～？"
                    "糖糖的感情数值变化：Stress: -1
                    '''),
                    AIMessage(content="😓💦"),
                    SystemMessage(content='''
                    糖糖:睡太久了浑身无力～～……我可以就酱紫睡一辈子吗？'
                    "阿P:可以啊！"
                    "糖糖:好耶～～！！！"
                    "糖糖的感情数值变化：Stress: -1
                    '''),
                    AIMessage(content="😋🎉"),

                    SystemMessage(content=f'''
                    糖糖:{prefix}'
                    "阿p:{user}"
                    "糖糖:{reply}"
                    "糖糖的感情数值变化：{attribute_change}
                    '''
                                  )
                ]
                if 'option_emoji' not in option or option['option_emoji'] == '':
                    option['option_emoji'] = chat(messages).content
                    print('option_emoji: ', option['option_emoji'])
                elif attribute_change == '':
                    option["attribute_change"] = 'Stress: -1'

            lines[i] = '\n'.join(json.dumps(obj, ensure_ascii=False) for obj in objs)

            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(''.join(lines))


# {text:''{"user": "", "reply": "", "attribute_change": "", "option_emoji": ""},"condition": "", "source":
# "Original_Generation"}
#

def generatePrefix():
    chat = ChatOpenAI(temperature=1.0, openai_api_key=openai.api_key,
                      openai_api_base=openai.api_base)

    # 生成选项 是否需要同时生成数值呢？同时阿p和糖糖的人格设定似乎可以使用一样的.
    prompt = """
    
    ##  你好ChatGPT，你需要扮演糖糖,然后根据角色设定和话题示例来生成更多的话题.
    ## 注意! 你不能重复生成糖糖话题示例中近似的内容!
    
    糖糖角色设定:
        糖糖是一名患有躁郁症的19岁女孩，性格贫乏，辍学后隐居在家中，与阿P住在一起。阿P负责管理她的日常生活。
        糖糖是一个喜欢亚文化，二次元圈子的人，糖糖喜欢说话的时候加上各种网络流行词或者一些俚语和颜文字，但是糖糖很少会关注二次元一类的东西，只是喜欢这种聊天交流的氛围。
        糖糖说话的时候会习惯加入一些语气词，如同"笑死"、"草"、"阿哈"、"诶～"、"QAQ"、"QWQ"，”啊～“。
        糖糖的说话风格是很口语化，经常使用网络流行词和一些二次元俚语。
        糖糖的回复应该简短，一般只包含三句话，每句话不超过20个字。

    糖糖话题示例:
        糖糖:我正在想下次搞什么企划呢～阿P帮帮我 出出主意
        糖糖:哎，你会希望看到糖糖将来的样子吗？
        糖糖:嗳，你来帮我打耳洞嘛 让喜欢的人给自己打耳洞很棒不是吗,虽然我好怕！,但是来吧！
        糖糖:我今后也会努力加油的，你要支持我哦 还有阿P你自己也要加油哦！
        糖糖:我问你哦，我真的可以就这样活下去吗？
        糖糖:啊～不行了 不行不行不行不行,无论思考什么，满脑袋都只有一个“死”字,阿P，我该怎么办啊？
        糖糖:阿P，看！我买了小发发!
        糖糖:醒过来一看太阳都下山了 笑死,睡太久了浑身无力～～……我可以就酱紫睡一辈子吗？
        糖糖:我没打招呼就把冰箱里的布丁吃了 会被判死刑吗？？？
        糖糖:我们点外卖吧我一步也不想动了可是又超想吃饭！！！
        糖糖:小天使请安！这个开场白也说厌了啊～,帮我想个别的开场白！
    """

    messages = [
        SystemMessage(content=prompt),
        AIMessage(content="好的，我会严格遵守您的要求,同时不会重复生成糖糖话题示例中近似的内容."),
        AIMessage(content='今天有点想试试平时不会做的事'),
        AIMessage(content='睡太久了浑身无力～～……阿p,我可以就酱紫睡一辈子吗？'),
    ]
    result = chat(messages).content
    return result


def generateOption(prefix):
    # model_name设置为openai的16k模型
    chat = ChatOpenAI(temperature=1.0, openai_api_key=openai.api_key,
                      openai_api_base=openai.api_base)

    # 生成选项 是否需要同时生成数值呢？同时阿p和糖糖的人格设定似乎可以使用一样的.
    prompt = """
    你好ChatGPT,我会提供给你一个reply话题,你只需要根据这个话题生成json的内容,内容具体格式如下.
    该jsonl的格式如下:
    {"prefix": "", "options": [{"user": "", "reply": "", "attribute_change": ""}], "id": "", "category": "",condition: "",condition: ""}
    我只会给你reply字段的内容,你需要根据reply的内容补全user字段,其余的一律不需要补全.
    为了user和reply的句子逻辑性,你可以稍微修改reply的内容,但是不要改变reply的意思.
    
    “糖糖”是一名患有精神疾病的年轻女孩，性格贫乏，辍学后隐居在家中，与阿p住在一起。为了支付租金和满足她的拟社会关注需求，“糖糖”决定开始在互联网上直播。她戴上假发并化妆，以“超绝最可爱天使酱”的名义与观众互动。阿p负责管理她的日常生活。

    糖糖角色设定:
        糖糖是一名患有躁郁症的19岁女孩，性格贫乏，辍学后隐居在家中，与阿P住在一起。阿P负责管理她的日常生活。
        糖糖是一个喜欢亚文化，二次元圈子的人，糖糖喜欢说话的时候加上各种网络流行词或者一些俚语和颜文字，但是糖糖很少会关注二次元一类的东西，只是喜欢这种聊天交流的氛围。
        糖糖说话的时候会习惯加入一些语气词，如同"笑死"、"草"、"阿哈"、"诶～"、"QAQ"、"QWQ"，”啊～“。
        糖糖的说话风格是很口语化，经常使用网络流行词和一些二次元俚语。
        糖糖的回复应该简短，一般只包含三句话，每句话不超过20个字。
        
    糖糖对话示例:
        糖糖:大人凡事都要讲道理烦死了～～～～～～～～～ 阿P和我要一直当小朋友
        糖糖:我是不介意别人约我联动 但是总会忘记回消息 然后对方就会超生气……活着好艰难哦
        糖糖:总感觉今天特别饥渴是怎么肥四！过来让我上你！！！！
        糖糖:药要吃完了 救救我
        糖糖:直播的时候我总表现得好像点赞和粉丝数都是浮云的样子 但其实我超级在意的
        糖糖:我知道有人开了我的帖子 可是我好怕 不敢看～ 你替我看看吧
        糖糖:虽然我把黑子都拉黑了，但是好怕他们会记恨我，晚上做梦都梦到被喷……
        糖糖:一直用你的号看网飞 搞得现在推荐栏里都是我喜欢的片子类型 抱歉哦
        糖糖:昨天我趁你睡觉的时候偷拍了你的睡脸 还差点传到超天号上 吓死我了
        糖糖:如果让我变成格斗游戏里的角色 应该会是那种远程放风筝阴人的类型 虽然不会太弱 但是玩家应该都会很烦我吧？？？
    

user:此处为阿p的回复内容,阿p是一个比较冷漠、不善于表达感情的角色,同时阿p是糖糖的男友.
    ## 注意:阿p的回复内容必须比糖糖的对话内容更加简短，内容需要小于10个字符。

reply: 此处为对应user(阿p)的糖糖回复内容.
    """
    exemple = """
{"prefix": "", "options": [{"user": "得省钱呀,就不要多买了吧", "reply": "555555555 但是我们得省钱对吧 谢谢你阿P", "attribute_change": ""}], "id": "", "category": "",condition: ""}
"""

    exemple_two = """
{"prefix": "", "options": [{"user": "我最喜欢你了", "reply": "你是说，你就爱看糖糖现在这种惨兮兮的蠢样？那真是恭喜你了 请尽情享用我的丑态吧", "attribute_change": ""}], "id": "", "category": "",condition: ""}
"""

    exemple_three = """
{"prefix": "", "options": [{"user": "你要烧炭?超市打折的时候再去好了", "reply": "……你为什么要在这种时候突然这么现实啊！！！！！！！！！", "attribute_change": ""}], "id": "", "category": "",condition: ""}
    """

    exemple_four = """
{"prefix": "", "options": [{"user": "你需要去美容一下~", "reply": "人家颜值已经是天下第一了，没什么要改动的啦！阿P，你真的很没礼貌欸", "attribute_change": ""}], "id": "", "category": "",condition: ""}
"""

    exemple_five = f"""
prefix:
user:
reply:{prefix}
attribute_change:
emoji:
        """
    # print(exemple_five)
    # 使用langchain让chatgpt根据strs的内容,来获得指定输出。
    messages = [
        SystemMessage(content=prompt),
        AIMessage(
            content="好的，我会严格遵守您设定的所有内容要求"),
        SystemMessage(content=f'reply:555555555 但是我们得省钱对吧 谢谢你阿P'),
        AIMessage(content=exemple),
        SystemMessage(content=f'reply:你是说，你就爱看糖糖现在这种惨兮兮的蠢样？那真是恭喜你了 请尽情享用我的丑态吧'),
        AIMessage(content=exemple_two),
        SystemMessage(content="reply:……你为什么要在这种时候突然这么现实啊！！！！！！！！！"),
        AIMessage(content=exemple_three),
        SystemMessage(content='reply:人家颜值已经是天下第一了，没什么要改动的啦！阿P，你真的很没礼貌欸'),
        AIMessage(content=exemple_four),
        # SystemMessage(
        #     content=f"接下来你需要以json格式完整输出内容。"
        #             'jsonl格式如下: {"prefix": "", "options": [{"user": "", "reply": "", "attribute_change": ""}], "id": "", "category": "",condition: ""}'),
        SystemMessage(content=f'reply:{prefix}'
                              f'注意:reply的内容是对user的回复'),
        AIMessage(content='好的,我会按照您的要求补全user的内容,根据reply的内容生成user,并且完整输出jsonl,同时我会合理修改您提供给我的reply内容,让reply的内容变成对user的回复.'),
    ]

    result = chat(messages).content

    return result


# 返回delta数值
def get_vale(history: list):
    chat = ChatOpenAI(temperature=0.9)

    prompt = """
    从现在开始，你是一个语义分析bot，我会给你一段两个人之间三段聊天的内容。你需要总结这三段聊天的内容来分析糖糖的情感变化。
    并且输出聊天数值的变化在该表格的小括号内：[好感度]:() [压力]:() [阴暗度]:() 
    往往在话题涉及到阴暗的事物时才会涉及到阴暗度。
    具体要求如下：
    人物限制：你只可以分析在这一段对话中糖糖这一个角色的情感变化。
    数值要求：你进行分析之后，需要严格按照一个表格进行输出，该表格的格式要求如下：[阴暗值]:() [压力]:() [阴暗度]:()
    回复要求：你只可以输出添加数值后的表格。并且数值的变化量只可以在-10至10之间，且需要填写在小括号内！
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


def simple_pi(prefix, pi, reply):
    chat = ChatOpenAI(temperature=1.0, openai_api_key=openai.api_key,
                      openai_api_base=openai.api_base)
    prompt = """
    我需要你你扮演一个数据分析师,我会提供给你一段对话内容,你需要将阿pi的回复内容进行精简.
    糖糖: 糖糖是话题的发起者,你不需要对糖糖的话进行精简.
    阿pi: 此处为阿p的回复内容,阿p是一个不善于表达感情的角色,且为糖糖的男友.注意:阿p的回复内容必须限制在20个字符之间.
    """

    example1 = """
    糖糖:换个思路，不如我们反过来蹭「#吐黑泥亲友扩列」这个tag的热度吧
    阿pi:这个主意太好了，我们要赶快行动起来
    """

    example2 = '''
    糖糖:糖糖的特技→可以闭着眼睛写出「憂鬱」这两个字
    阿pi:真的吗？可以教我吗？
    '''

    example3 = f'''
    糖糖:那些瞧不起连锁快餐店的人，不就是在绕着弯子炫耀自己有钱吗？搞笑诶
    阿pi:他们是觉得连锁店没品质啊
    糖糖:哈哈哈 知道了知道了 他们哪儿比上其他的好 你说说看？
    
    '''
    # example3 = f'''
    # 糖糖:{prefix}
    # 阿pi:{pi}
    # 糖糖:{reply}
    # '''
    # todo 把阿p的回复内容变得更加简洁.
    messages = [
        SystemMessage(content=prompt),
        AIMessage(content="好的，我会帮您精简阿p的回复内容"),
        SystemMessage(content=example1),
        AIMessage(content='主意很好'),
        SystemMessage(content=str(example2)),
        AIMessage(content='教教我'),
        SystemMessage(content=str(example3)),
    ]

    result = chat(messages)
    print(result)


def generateReplyUser(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    decoder = json.JSONDecoder()
    # 读取每一列的jsonl内容
    for i in range(len(lines)):
        # 获取当前jsonl内容的text字段
        objs = []
        s = lines[i]
        while s:
            obj, pos = decoder.raw_decode(s)
            objs.append(obj)
            s = s[pos:].lstrip()
            for obj in objs:
                text = obj['text']
                # 传递text。
                image_event = generateOption(text)
                print(image_event)
                to_jsonl(image_event, 'image_text_relationship_reply.jsonl', 'idnull')


if __name__ == '__main__':
    # generatePrefix()
    # simple_pi('', '', 'pi')
    # print(generateOption("a"))
    print(generateReplyUser('image_text_relationship.jsonl'))
    # emoji_jsonl('Daily_event_130.jsonl')
    # emoji_jsonl('complete_story_30.jsonl')

# 这是我们当上主播后的第一个早晨呢
# 你快看私信！
# 快看，快看啊阿P！
