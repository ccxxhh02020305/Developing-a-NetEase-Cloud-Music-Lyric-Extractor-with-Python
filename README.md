﻿# 歌词提取器(支持QQ音乐和网易云音乐)
Pr，剪映等软件都支持将lrc文件直接导入从而迅速获取歌词

于是，在听完室友的介绍后，我毅然决然地建立了这个仓库（其实也有检验学习成果的意思啦）

你可以使用pyinstaller打包它

马上要期末考了，挤出点时间不容易，还望觉得有用的大佬们帮忙点点星星orz......
有什么改进也可以提，我会努力改进的(✧∇✧)

感谢大佬给出的QQ音乐歌词api，直接减少一半工作量，可惜佬是根据歌手进行查找的，要不然前半截也可以沾沾光了

佬的链接：https://github.com/yangjianxin1/QQMusicSpider


===========================================================================

添加了QQ音乐歌曲下载功能（不能开箱即用，需要做一点修改）

不过想要获取会员歌曲的话还是需要会员账号，所以需要先用一个会员账号登进QQ音乐，拿到cookie里的qm_keyst以及psrf_qqaccess_token字段再贴进脚本里

user_id可以选择每次都要输入，不过我更推荐硬编码

部分歌曲在下载时可能会跳两次地址选择，因为我默认请求flac格式的音频，在没有flac格式的情况下再请求m4a格式，所以会跳两次选择地址（说到底不过是因为懒，见笑了）

使用之前记得下载node.js，向QQ音乐服务器请求vkey时uin是自动拉取的，所以里面用一段JavaScript模拟了QQ音乐前端环境的部分对象

node.js下载链接：https://nodejs.org/zh-cn/download
