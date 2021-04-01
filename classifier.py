import os
import shutil
import random

file_src_url = '.'
file_dest_url = 'dataset'

wake_word_file_name = "wakeword"
not_wake_word_file_name = "no-wakeword"

#Test文件所占百分比
test_rile_ratio = 0.2  

# 获取文件下的所有指定类型文件  dir:文件路径, suffix:文件后缀
def getFiles(dir, suffix=".wav"):
    res = []
    if not os.path.exists(dir):
        return res
    for filename in os.listdir(dir):
        name, suf = os.path.splitext(filename)
        if suf == suffix:
            res.append(os.path.join(dir, filename))
    return res

if __name__ == '__main__':
    wake_word_src = os.path.join(file_src_url, "wake-word")
    not_wake_word_src = os.path.join(file_src_url, "not-wake-word")

    # 唤醒词文件和环境音文件导入
    wake_word_file = getFiles(wake_word_src)
    not_wake_word_file = getFiles(not_wake_word_src)
    wake_word_count = len(wake_word_file)
    not_wake_word_count = len(not_wake_word_file)
    # 随机选取测试集和训练集
    random.shuffle(wake_word_file)
    random.shuffle(not_wake_word_file)
    wake_word_train_num = int(wake_word_count * (1 - test_rile_ratio))
    not_wake_word_train_num = int(not_wake_word_count * (1 - test_rile_ratio))
    wake_word_train_file = wake_word_file[0:wake_word_train_num]
    wake_word_test_file = wake_word_file[wake_word_train_num:wake_word_count]
    not_wake_word_train_file = not_wake_word_file[0:not_wake_word_train_num]
    not_wake_word_test_file = not_wake_word_file[not_wake_word_train_num:not_wake_word_count]
    # 目标存储路径
    wake_word_url = os.path.join(file_dest_url, "wake-word")
    not_wake_word_url = os.path.join(file_dest_url, "not-wake-word")
    test_wake_word_url = os.path.join(file_dest_url, "test", "wake-word")
    test_not_wake_word_url = os.path.join(file_dest_url, "test", "not-wake-word")
    # 确保目标路径存在
    if not os.path.exists(wake_word_url):
        os.makedirs(wake_word_url)
    if not os.path.exists(not_wake_word_url):
        os.makedirs(not_wake_word_url)
    if not os.path.exists(test_wake_word_url):
        os.makedirs(test_wake_word_url)
    if not os.path.exists(test_not_wake_word_url):
        os.makedirs(test_not_wake_word_url)
    # 开始拷贝
    print("Start Copying...\nwake_word_train: {}, not_wake_word_train: {}, \nnot_wake_word_train: {},not_wake_word_test: {}"
    .format(wake_word_train_num, wake_word_count - wake_word_train_num, not_wake_word_train_num, not_wake_word_count - not_wake_word_train_num))
    print("Copying wake-word-train...")
    counter = 0
    sum_num = len(wake_word_train_file)
    for file in wake_word_train_file:
        url_new = os.path.join(wake_word_url, wake_word_file_name + str(counter) + ".wav")
        shutil.copyfile(file, url_new)
        counter += 1
        print("\rCopied: {}/{}".format(counter, sum_num), end="", flush=True)
    print("\n")
    print("Copying not-wake-word-train...")
    counter = 0
    sum_num = len(not_wake_word_train_file)
    for file in not_wake_word_train_file:
        url_new = os.path.join(not_wake_word_url, not_wake_word_file_name + str(counter) + ".wav")
        shutil.copyfile(file, url_new)
        counter += 1
        print("\rCopied: {}/{}".format(counter, sum_num), end="", flush=True)
    print("\n")
    print("Copying wake-word-test...")
    counter = 0
    sum_num = len(wake_word_test_file)
    for file in wake_word_test_file:
        url_new = os.path.join(test_wake_word_url, wake_word_file_name + str(counter) + ".wav")
        shutil.copyfile(file, url_new)
        counter += 1
        print("\rCopied: {}/{}".format(counter, sum_num), end="", flush=True)
    print("\n")
    print("Copying not-wake-word-test...")
    counter = 0
    sum_num = len(not_wake_word_test_file)
    for file in not_wake_word_test_file:
        url_new = os.path.join(test_not_wake_word_url, not_wake_word_file_name + str(counter) + ".wav")
        shutil.copyfile(file, url_new)
        counter += 1
        print("\rCopied: {}/{}".format(counter, sum_num), end="", flush=True)
    print("\n")
    print("Copy Finished!\nwake_word_train: {}, not_wake_word_train: {}, \nnot_wake_word_train: {},not_wake_word_test: {}"
    .format(wake_word_train_num, wake_word_count - wake_word_train_num, not_wake_word_train_num, not_wake_word_count - not_wake_word_train_num))