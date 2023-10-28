import os
import re
import pandas as pd

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


'''
# Jine.xlsx: https://docs.google.com/spreadsheets/d/1jIOVqJEjtNY53uitiz-9Segw-0nGTjgy5b5VvzjWKw4/edit?usp=sharing
Jines_file = r"Jine.xlsx"

# # 读取与查询
Jines = pd.read_excel(Jines_file)

# 查询有选项的内容
pattern = r'(?<=\().*?(?=\))'

# 匹配事件
Title = Jines.loc[(Jines['ParentId (more info)'].str.contains(pattern, regex=True, na=False))]

Attribute_temp = {"Affection": 0, "Stress": 0, "Darkness": 0}
event_list = []


def temp_list(event, prefix):
    # 传入事件名称，和前缀，判断是否为一组提问或者回复。
    event_list.append(event)
    # 字典？


def format_output(row):
    # ID
    ParentId = f'{row["ParentId (more info)"]}'

    # 匹配标题
    regex1 = r"\w+(?= \()"
    title = re.search(regex1, ParentId)
    title_str = title.group()

    # 匹配提问
    match = re.search(r"\(First Part\)", ParentId)
    match2 = re.search(r"\(First Part; end\)", ParentId)
    # match3 = re.search(r"\(Third Part\)", ParentId)
    # match4 = re.search(r"\(Second Part\)", ParentId)
    # match5 = re.search(r"\(Fourth Part\)", ParentId)

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
    if match or match2:
        Prefix = f'\n##\n### Prefix '
        Ame = f"糖糖: {row['BodyCn']}"

        with open(f'events/{title_str}.txt', 'a+', encoding='utf-8') as f:
            # 使用 join 方法将 Ame, Title_ame, Category 连接成一个字符串，并在每个字段之间添加一个制表符
            line = '\n'.join([Prefix, Ame, ])

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
            user = f"User:：{row['BodyCn']}"

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


# 并输出结果
re_Title = Title.apply(format_output, axis=1)
output_str = re_Title.str.cat(sep="\n \n")  # 用空格分隔每个元素
# 输出结果
print(output_str)
