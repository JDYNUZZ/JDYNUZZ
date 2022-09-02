import os
import re
from helper import get_file, find_c_or_cpp, find_files, find_command, find_command_star_node, get_cpp_files_path
import json

# compdb = True
# project_path = '/hci/chaoran_data/android-7.0.0_r33'
# compdb = False
# project_path = '/hci/chaoran_data/android-8.1.0_r67'
# compdb = True
# project_path = '/hci/chaoran_data/android-7.1.2_r33'
# compdb = False
# project_path = '/hci/chaoran_data/android-9.0.0_r47'
# compdb = True
# project_path = '/hci/chaoran_data/android-11.0.0_r39'
# save_path = 'jni11.0/jni.json'
# version = '11.0'
compdb = True
# project_path = '/hci/chaoran_data/android-10.0.0_r45'
# save_path = 'jni10.0/jni.json'
# version = '10.0'
project_path = '/hci/chaoran_data/android-12.0.0_r31'
save_path = 'jni12.0/jni.json'
version = '12.0'
if(compdb):
    file_json_key = 'file'
else:
    file_json_key = 'source'

def find_str_in_file(path, str):
    if not os.path.exists(path):
        return False
    file = None
    try:
        file = open(path, 'r', encoding='UTF-8')
        lines = file.readlines()
    except Exception as e:
        file = open(path, 'r', encoding='latin1')
        lines = file.readlines()
    finally:
        if(file):
            file.close()
    analyze_this_file = False
    for i, line in enumerate(lines):
        if str in line:
            analyze_this_file = True
    if not analyze_this_file:
        return False
    else:
        return True

def extract_jni_list(path, str):
    if not os.path.exists(path):
        return False
    file = None
    try:
        file = open(path, 'r', encoding='UTF-8')
        lines = file.readlines()
    except Exception as e:
        file = open(path, 'r', encoding='latin1')
        lines = file.readlines()
    finally:
        if(file):
            file.close()
    found = False
    cache = ''
    r_list = []
    for i, line in enumerate(lines):
        if str in line:
            found = True
            cache = ''

        if found:
            tem = line.strip()
            if not tem.startswith("//"):
                cache = cache + tem

        if '};' in line:
            found = False
            if cache!='':
                r_list.append(cache)
                cache = ''
    return r_list

def transform(list):
    pairs = []
    # 多个变量
    for tem in list:

        for a in re.findall('/\*.+?\*/', tem):
            tem = tem.replace(a, '')
        if '/*' in tem or '\*' in tem:
            sss=0
        groups = re.findall('\{(.+?)\}', tem)

        pair = []
        # 变量单行
        for group in groups:
            if 'NATIVE_METHOD' in group:
                continue
            s_group = group.split(',')
            s_group[0] = re.findall('"(.+?)"', s_group[0])[0]
            s_group[-1] = s_group[-1].strip()

            for a in re.findall('^\(void.+?\)', s_group[-1]):
                s_group[-1] = s_group[-1].replace(a, '')

            s_group[-1] = s_group[-1].strip()
            pair.append(s_group)
        pairs.append(pair)
    return pairs

def extract_save():
    list = get_cpp_files_path(compdb, version)

    cpp_jni_list = []
    for tem in list:
        # if 'android_media_RemoteDisplay.cpp' in tem[file_json_key]:
        #     print('*********')
        #     print(tem[file_json_key])
        #     print(tem['command'])
            # exit(2)
        if 'test' in tem[file_json_key].lower() or 'tests' in tem[file_json_key].lower() or 'armv7' in tem[file_json_key].lower():
            continue
        # [{source:'xxxx.cpp', content:{...}}]
        f = project_path + '/' + tem[file_json_key]

        found = False
        for temm in cpp_jni_list:
            if (f == temm['cpp']):
                found = True
        if found:
            continue
        str = 'static JNINativeMethod'
        if 'frameworks/' in f and find_str_in_file(f, str) and 'main.cpp' not in f:
            # print()
            print(f)
            jni_list = extract_jni_list(f, str)
            pairs = transform(jni_list)

            cpp_jni_list.append({'cpp': f, 'pairs': pairs})
        str = 'static const JNINativeMethod'
        if 'frameworks/' in f and find_str_in_file(f, str) and 'main.cpp' not in f:
            # print()
            print(f)
            jni_list = extract_jni_list(f, str)
            pairs = transform(jni_list)

            cpp_jni_list.append({'cpp': f, 'pairs': pairs})

    with open(save_path, 'w') as file_obj:
        json.dump(cpp_jni_list, file_obj)

if __name__ == '__main__':
    extract_save()