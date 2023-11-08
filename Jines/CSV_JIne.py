import json
import os
import re
import pandas as pd

from Jines.Option import generateOption, generatePrefix, emoji_jsonl

'''
Affection：nan Stress：nan Darkness：nan
None

Affection：nan
Stress：nan
Darkness：nan

Darkness：?

糖糖：nan

1. 多组对话只需要传递一个变量参数
2. 去除不改变数值的选项与对话。
3. 单选项的不需要

--
追加写入 Category 和 ID

---
把同一个event的多段First Part合成一个。
写入jsonl

1. 接入python客户端
2. 添加填充更多的事件

'''
# Jine.xlsx: https://docs.google.com/spreadsheets/d/1jIOVqJEjtNY53uitiz-9Segw-0nGTjgy5b5VvzjWKw4/edit?usp=sharing
Jines_file = r"Jines.xlsx"

# # 读取与查询
Jines = pd.read_excel(Jines_file)

# 查询有选项的内容
pattern = r'(?<=\().*?(?=\))'

# 匹配事件
Title = Jines.loc[(Jines['ParentId (more info)'].str.contains(pattern, regex=True, na=False))]

Attribute_temp = {"Affection": 0, "Stress": 0, "Darkness": 0}
Title.to_pickle("Title.pkl")


def sanitize_filename(filename):
    invalid_chars = '<>:"/\\|?*\n'
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    return filename


def format_output(row):
    # ID
    ParentId = f'{row["ParentId (more info)"]}'
    Category_temp = f'{row["Category"]}'
    Category = sanitize_filename(Category_temp)
    ID = f'{row["Id"]}'

    # 匹配标题
    regex1 = r"\w+(?= \()"
    title = re.search(regex1, ParentId)
    title_str = title.group()

    # 事件
    event_list = []

    # 匹配提问
    match = re.search(r"\(First Part\)", ParentId)
    match2 = re.search(r"\(First Part; end\)", ParentId)
    match3 = re.search(r"\(Third Part\)", ParentId)
    match4 = re.search(r"\(Second Part\)", ParentId)
    match5 = re.search(r"\(Fourth Part\)", ParentId)

    # 数值
    aff = f"Affection: {row['Affection']}"
    str = f"Stress: {row['Stress']}"
    dar = f"Darkness: {row['Darkness']}"

    # 匹配选项以及回复
    choose_time = re.search(r"\d+", ParentId)
    reply_ = re.search(r'(\(.*Option[0-9]+;end\))', ParentId)
    reply_2 = re.search(r'(\(.*Option[0-9]\))', ParentId)

    # 处理提问
    # if match or match2 or match4 or match5 or match3:
    if match or match2 or match3 or match4 or match5:

        Prefix = f'\n## 对话\n### Prefix Category_temp:{Category} ID:{ID}'
        Ame = f"糖糖: {row['BodyCn']}"
        with open(f'events/{title_str}.txt', 'a+', encoding='utf-8') as f:
            # 使用 join 方法将 Ame, Title_ame, Category 连接成一个字符串，并在每个字段之间添加一个制表符
            line = '\n'.join([Prefix, Ame])

            line_bytes = line.encode('utf-8')
            # 将字节对象写入到文件中
            line_str = line_bytes.decode('utf-8')
            # 将字符串对象写入到文件中
            f.write(line_str)

        return "\n".join([Prefix, Ame])

    # 处理选项
    elif row['Speaker/Action (in blue)'] == 'pi':
        # 跳过数值为空的回复
        try:
            key = f'\n### Option-{choose_time.group()}'
            user = f"User:　{row['BodyCn']}"

            if aff == 'Affection: nan':
                aff = ''
            if str == 'Stress: nan':
                str = ''
            if dar == 'Darkness: nan':
                dar = ''
            value = f"Attribute Change: {aff} {str} {dar}"

            if value == 'Attribute Change:   ':
                value = ''

            with open(f'events/{title_str}.txt', 'a+', encoding='utf-8') as f:
                # 使用 join 方法将 Ame, Title_ame, Category 连接成一个字符串，并在每个字段之间添加一个制表符
                line = '\n'.join([key, user, value])

                line_bytes = line.encode('utf-8')
                # 将字节对象写入到文件中
                line_str = line_bytes.decode('utf-8')
                # 将字符串对象写入到文件中
                f.write(line_str)
            return "\n".join([key, user, value])
        except:
            pass

    # 处理选项回复
    elif reply_ or (reply_2 and row['Speaker/Action (in blue)'] == 'ame'):
        try:
            key = f'\nReply：\n糖糖：{row["BodyCn"]}'

            if aff == 'Affection: nan':
                aff = ''
            if str == 'Stress: nan':
                str = ''
            if dar == 'Darkness: nan':
                dar = ''
            value = f"Attribute Change: {aff} {str} {dar}"

            if value == 'Attribute Change:   ':
                value = 'Attribute Change: None'

            if key == '\nReply：\n糖糖：nan':
                with open(f'events/{title_str}.txt', 'a+', encoding='utf-8') as f:
                    # 使用 join 方法将 Ame, Title_ame, Category 连接成一个字符串，并在每个字段之间添加一个制表符
                    line = '\n'.join([value])
                    line_bytes = line.encode('utf-8')
                    # 将字节对象写入到文件中
                    line_str = line_bytes.decode('utf-8')
                    # 将字符串对象写入到文件中
                    f.write(line_str)

                return "\n".join([value])

            with open(f'events/{title_str}.txt', 'a+', encoding='utf-8') as f:
                # 使用 join 方法将 Ame, Title_ame, Category 连接成一个字符串，并在每个字段之间添加一个制表符
                line = '\n'.join([key, value])

                line_bytes = line.encode('utf-8')
                # 将字节对象写入到文件中
                line_str = line_bytes.decode('utf-8')
                # 将字符串对象写入到文件中
                f.write(line_str)

            return "\n".join([key, value])
        except:
            pass


import json


def copy_img_name(file_path_a, file_path_b, output_path):
    # 打开文件A和B
    with open(file_path_a, 'r', encoding='utf-8') as file_a:
        for line in file_a:
            line = json.loads(line)
            print(line['img_name'])
            img_name = []
            img_name += [line['img_name']]

    with open(file_path_b, 'r', encoding='utf-8') as file_b:
        for line_b in file_b:
            json_line_b = json.loads(line_b)
            # print(json_line_b)
            # 为json_line_b添加img_name字段:
            # json_line_b['img_name'] = line['img_name']
            # print(json_line_b)
            # json_line_b['img_name'] = line['img_name']
            print(img_name)



    # 创建一个新的列表来存储输出的行
    output_lines = []
    #
    #
    # # 将输出列表写入新的JSONL文件
    # with open(output_path, 'w') as output_file:
    #     output_file.write('\n'.join(output_lines))


copy_img_name('image_text_relationship.jsonl', 'image_text_relationship_reply.jsonl',
              'image_text_relationship_reply_idk.jsonl')


def get_option():
    times = 0
    text = ''
    try:
        # 查询Jines 的Speaker/Action (in blue)列内容为ame,且ParentId (more info)列内容为weekday的那行,然后以字符串的形式输出该行的BodyCn列的内容.

        prefix_temp = (Jines.loc[(Jines['Speaker/Action (in blue)'] == 'ame') & (
                Jines['ParentId (more info)'] == 'weekday'), 'BodyCn'].to_list())

        for i in prefix_temp:
            if 7 < len(i) < 20:
                times += 1
                print(f'文本内容: {i}\n句子长度: {len(i)} \n事件序号: {times}\n------')
                # 处理所有事件
                if times >= 0:
                    daily_event = generateOption(i)
                    # 算了,能用就行.
                    # 处理一下jsonl的格式.
                    to_jsonl(daily_event, 'Daily_event_len_20.jsonl', times)
                    # 生成emoji
                    emoji_jsonl('Daily_event_len_20.jsonl')
                    text = i
    except:
        print(f'出错了,请检查代码{times} \n 文本内容: {text}')


def to_jsonl(text, filename, id):
    # 分割文本为列表
    lines = text.split("\n")
    dialogs = []
    dialog = {}
    option = {}
    for line in lines:
        line = line.strip()
        if line.startswith("prefix") or line.startswith("a"):
            if dialog and option:
                dialog["options"].append(option)
                option = {}
            if dialog:
                dialogs.append(dialog)
            dialog = {"prefix": line[7:].strip(), "options": [], "id": f'event{id}', "category": 'weekday'}

            # print(ids, categories)

        elif line.startswith("options"):
            if option:
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

# get_option()
# to_jsonl(text, 'Daily_event_130.jsonl')
# format_output()
# # 并输出结果
# re_Title = Title.apply(format_output, axis=1)
# output_str = re_Title.str.cat(sep="\n \n")  # 用空格分隔每个元素
# # 输出结果
# print(output_str)
