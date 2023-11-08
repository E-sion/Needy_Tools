import json
import os
import re
import shutil
import json
import pandas as pd

tangtang_pattern = re.compile(r'糖糖: (.*)')


# 定义方法
# 定义方法
def search_in_excel(search_string):
    search_string.replace(" ", "")
    # 对 search_string 进行正则表达式匹配，并提取出糖糖后面的说话内容
    if tangtang_pattern.search(search_string):
        tangtang_speech = tangtang_pattern.search(search_string).group(1)

    else:
        # 如果没有匹配成功，就返回空列表
        return [], []
    # 读取Excel文件
    df = pd.read_excel('Jine.xlsx')

    # 用 tangtang_speech 检索字符串
    result = df[df.apply(lambda row: row.astype(str).str.contains(tangtang_speech).any(), axis=1)]

    # 获取Id和Category列的内容
    ids = result['Id'].values.tolist()
    categories = result['Category'].values.tolist()
    return ids, categories


def parse_to_jsonl(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = iter(f.readlines())
    dialogs = []
    dialog = {}
    option = {}
    for line in lines:
        line = line.strip()
        if line.startswith("## 对话") or line.startswith("## 对话组"):
            if dialog and option:
                dialog["options"].append(option)
                option = {}
            if dialog:
                dialogs.append(dialog)
            dialog = {"prefix": "", "options": []}
        elif line.startswith("### Prefix") or line.startswith('**Prefix'):
            prefix = next(lines).strip()
            ids, categories = search_in_excel(prefix)
            if ids and categories:
                dialog["id"] = ids[0]
                dialog["category"] = categories[0]
            dialog["prefix"] = prefix
        elif line.startswith("### Option") or line.startswith('**Option'):
            if option:
                dialog["options"].append(option)
            option = {"user": "", "reply": "", "attribute_change": ""}

        elif line.startswith("User") or line.startswith("User:"):
            option["user"] = line[5:].strip()
        elif line.startswith("Reply") or line.startswith('**Reply:**'):
            option["reply"] = next(lines).strip()
        elif line.startswith("Attribute Change") or line.startswith('**Attribute Change:**'):
            option["attribute_change"] = line[17:].strip()

    if option:
        dialog["options"].append(option)
    if dialog:
        dialogs.append(dialog)

    with open('emoji_story_23.jsonl', 'a+', encoding="utf-8") as outfile:
        for entry in dialogs:
            json.dump(entry, outfile, ensure_ascii=False)
            outfile.write('\n')


# parse_to_jsonl('move/Event_Advice.txt', )
def no_reply_jsonl(input_file_path, output_file_path):
    with open(input_file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    decoder = json.JSONDecoder()
    new_lines = []
    seen = set()

    for i in range(len(lines)):
        objs = []
        s = lines[i]
        while s:
            obj, pos = decoder.raw_decode(s)
            objs.append(obj)
            s = s[pos:].lstrip()

        for obj in objs:
            for option in obj['options']:
                if option['reply'] == '':
                    line = json.dumps(obj, ensure_ascii=False)
                    if line not in seen:
                        new_lines.append(line)
                        seen.add(line)
                    lines[i] = ''

    with open(input_file_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(line for line in lines if line))

    with open(output_file_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(new_lines))


# no_reply_jsonl('emoji_story_23.jsonl', 'emoji_story_23_no_reply.jsonl')

for filename in os.listdir('events'):
    if filename.endswith(".txt"):
        try:
            parse_to_jsonl(f'events/{filename}')
        except:
            # shutil.move(f'move/{filename}', f'error/{filename}')
            print(filename)
