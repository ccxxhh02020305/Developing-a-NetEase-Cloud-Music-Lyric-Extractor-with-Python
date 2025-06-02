# 需要安装pycryptodome解密AES
from Crypto.Cipher import AES
from base64 import b64encode
import requests
import json
import random
from bs4 import BeautifulSoup
import os
import keyboard

song_name = input("请输入你想查询的歌名：")

# 使用正确的搜索 API 端点
search_url = f"https://music.163.com/api/search/get/web?csrf_token="


# 构建请求参数
params = {
    "s": song_name,
    "type": 1,  # 1 表示搜索歌曲
    "offset": 0,
    "limit": 10
}

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



try:
    # 使用 GET 方法并传递参数
    response = requests.get(search_url, params=params, headers=header)
    response.raise_for_status()  # 检查请求是否成功

    data = response.json()

    # 提取搜索结果
    if data.get("code") == 200 and "result" in data and "songs" in data["result"]:
        songs = data["result"]["songs"]
        if songs:
            print(f"找到 {len(songs)} 首相关歌曲：")
            for i, song in enumerate(songs, 1):
                song_id = song.get("id")
                song_name = song.get("name")
                artists = ", ".join([artist.get("name") for artist in song.get("artists", [])])
                album = song.get("album", {}).get("name")
                print(f"{i}. ID: {song_id}, 歌曲: {song_name}, 歌手: {artists}, 专辑: {album}")
        else:
            print("未找到相关歌曲")
        # song = songs[0]
        # song_id = song.get("id")
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


# 开始解密
url = "https://music.163.com/weapi/song/lyric?csrf_token="

data = {
    "csrf_token": "",
    "id": song_id,
    "lv": "-1",
    "tv": "-1"
}

song_id = data["id"]

e = "010001"
f = "00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7"
g = "0CoJUm6Qyw8W8jud"
i = "KYWx6w2CgEfW4QB8"




def get_encSecKey():
    return "d79c9344cfcd6cf951345a79c697436935f7c3a11e6a8a8222983a80a5b51feb9a55161a17531e12207b841c2f02b108e56ef57c1dbf2cc00c76dd4e726669cec3b6d854b6812499f3ff37a687d688ef14bbc15076f7ce1dd00ad0ae058b3eb3e577a28a3af4e043807e35021c8608ad24a4ab74cd0fb3f56bd2b2cc0cf7a703"

# 把参数进行加密
def get_params(data):       # 如下d函数，默认这里收到的data是字符串
    first = enc_params(data,g)
    second = enc_params(first,i)
    return second           # 返回的就是params

# 转化成16的倍数，为下方的加密算法服务
def to_16(data):
    pad = 16 - len(data) % 16
    data += chr(pad) * pad
    return data

def enc_params(data,key):   #加密过程，默认这里收到的data是字符串
    iv = "0102030405060708"
    data = to_16(data)
    aes = AES.new(key=key.encode("utf-8"),IV=iv.encode("utf-8"),mode=AES.MODE_CBC)         # 创建加密器
    bs = aes.encrypt(data.encode("utf-8"))           # 加密，加密的内容的长度必须是16的倍数
    return str(b64encode(bs),"utf-8")       # 转化成字符串返回



# 发送请求，得到歌词
resp = requests.post(url,data={
    "params": get_params(json.dumps(data)),
    "encSecKey": get_encSecKey()
})

print(resp.json())

resp.close()

# json转txt
# 提取歌词文本（字符串）
lyric_text = resp.json()["lrc"]["lyric"]

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

"""    
    function a(a) {
        var d, e, b = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", c = "";
        for (d = 0; a > d; d += 1)
            e = Math.random() * b.length,
            e = Math.floor(e),
            c += b.charAt(e);
        return c
    }
    function b(a, b) {
        var c = CryptoJS.enc.Utf8.parse(b)
          , d = CryptoJS.enc.Utf8.parse("0102030405060708")
          , e = CryptoJS.enc.Utf8.parse(a)
          , f = CryptoJS.AES.encrypt(e, c, {
            iv: d,
            mode: CryptoJS.mode.CBC
        });
        return f.toString()
    }
    function c(a, b, c) {
        var d, e;
        return setMaxDigits(131),
        d = new RSAKeyPair(b,"",c),
        e = encryptedString(d, a)
    }
    function d(d, e, f, g) {
        var h = {}
          , i = a(16);
        return h.encText = b(d, g),
        h.encText = b(h.encText, i),
        h.encSecKey = c(i, e, f),
        h
    }
"""
