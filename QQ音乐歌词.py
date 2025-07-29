# 需要安装pycryptodome解密AES
from Crypto.Cipher import AES
from base64 import b64encode
import requests
import json
import random
from bs4 import BeautifulSoup
import os
import keyboard
import html


song_name = input("请输入你想查询的歌名：")

headers = [
    {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36 Edg/136.0.0.0"},
    {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"},
    {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/114.0"},
    {
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Safari/605.1.15"}
]
header = random.choice(headers)


search_url = f"https://c6.y.qq.com/splcloud/fcgi-bin/smartbox_new.fcg?key={song_name}"

try:
    # 使用 GET 方法并传递参数
    response = requests.get(search_url, headers=header)
    response.raise_for_status()  # 检查请求是否成功

    data = response.json()

    # 提取搜索结果
    if data.get("code") == 0  and "data" in data:
        songs = data["data"]["song"]["itemlist"]
        if songs:
            print(f"找到 {len(songs)} 首相关歌曲：")
            for i, song in enumerate(songs, 1):
                song_id = song.get("id")
                song_name = song.get("name")
                song_mid = song.get("mid")
                song_singer = song.get("singer")
                print(f"{i}. ID: {song_id}, 歌曲: {song_name}, 歌手: {song_singer}, mid: {song_mid}")
        else:
            print("未找到相关歌曲")

    else:
        print("搜索请求失败")
        print(f"返回代码: {data.get('code')}")
        print(f"返回信息: {data.get('message')}")

except requests.exceptions.RequestException as e:
    print(f"请求发生错误: {e}")
except ValueError as e:
    print(f"解析 JSON 数据失败: {e}")
finally:
    if 'response' in locals():
        response.close()


number = int(input("请选择你要的歌曲序号："))
for i,song in enumerate(songs,1):
    if number == i:
        song_id = song.get("id")
        song_mid = song.get("mid")
# song_mid
# song_url = f"https://y.qq.com/n/ryqq/songDetail/{song_mid}"

headers1 = [
    {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36 Edg/136.0.0.0",
        "referer": f"https://y.qq.com/n/yqq/song/{song_mid}.html"
    },
    {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
        "referer": f"https://y.qq.com/n/yqq/song/{song_mid}.html"
    },
    {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/114.0",
        "referer": f"https://y.qq.com/n/yqq/song/{song_mid}.html"
    },
    {
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Safari/605.1.15",
        "referer": f"https://y.qq.com/n/yqq/song/{song_mid}.html"
    }
]
header1 = random.choice(headers1)

lyric_url = f"https://c.y.qq.com/lyric/fcgi-bin/fcg_query_lyric_yqq.fcg?nobase64=1&musicid={song_id}&format=json"


resp = requests.get(lyric_url,headers= header1)
response.raise_for_status()  # 检查请求是否成功
resp.close()

# 转HTML码
decoded_lyric = html.unescape(resp.json()['lyric'])
print(decoded_lyric)

# json转txt
# 提取歌词文本（字符串）
lyric_text = decoded_lyric

# 询问储存地址
location = input("请输入你想存入哪个盘（D或E）：")

# 定义 TXT 保存路径（字符串）
txt_file_path = f"{location}:\\lyrics-{song_id}.txt"
# 写入 TXT 文件（正确使用文件路径）
with open(txt_file_path, "w", encoding="utf-8") as f:
    f.write(lyric_text)




# txt转lrc
# lrc_file_path是储存文件地址
lrc_file_path = f"{location}:\\lyrics-{song_id}.lrc"
def txt_to_lrc(txt_path, lrc_path):
    with open(txt_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    lrc_content = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        # 格式为[时间]歌词，用]分割
        parts = line.split(']', 1)
        if len(parts) == 2:
            time_str, lyric = parts
            # 转换时间格式为[mm:ss.xx]
            lrc_time = f"{time_str}]"
            lrc_content.append(f"{lrc_time}{lyric}")


    with open(lrc_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lrc_content))

# 执行
txt_to_lrc(txt_file_path,lrc_file_path)


# 删除txt文件
directory = f"{location}:\\"

for file in os.listdir(directory):
    if file.endswith('.txt'):
        os.remove(os.path.join(directory,file))


print("")
print("")
print("")
print("")
print("")
print(f"你所需的文件在{lrc_file_path}")
print("按Esc退出......")

# 监听 Esc 键按下事件
keyboard.wait('esc')  # 阻塞程序，直到按下 Esc 键
keyboard.unhook_all()  # 释放键盘监听资源