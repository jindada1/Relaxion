# Relaxion 

A RESTful API server based on aiohttp framework in python3. using web crawlers to get data from several major music platforms and aggregate them into a unified set of APIs.

*DISCLAIMER: This is an experimental software. **Please do not use it for commercial purposes**!!!*



## 音乐服务

| 平台                                   | 搜索 | 听歌 | 看MV | 获取评论 | 平台用户信息 |
| -------------------------------------- | ---- | ---- | ---- | -------- | ------------ |
| [QQ](https://y.qq.com/)                | √    | √    | √    | √        | ×            |
| [Netease](https://music.163.com/)      | √    | √    | √    | √        | ×            |
| [KuGou](https://www.kugou.com/)        | √    | √    | √    |          |              |
| [KuWo Music](http://www.kuwo.cn/)      | √    | √    | √    |          |              |
| [MiGu Music](https://music.migu.cn/v3) |      |      |      |          |              |



### 搜索

**get**  `/{platform}/songs` 返回一组歌曲

**get**  `/{platform}/albums` 返回一组专辑

**get**  `/{platform}/mv` 返回一组 MV

**参数**

| 参数名  | 类型   | 必须 | 含义           | 默认 |
| ------- | ------ | ---- | -------------- | ---- |
| keyword | String | 是   | 搜索关键字     |      |
| num     | Number |      | 返回的结果数量 | 20   |
| page    | Number |      | 第几页结果     | 0    |

样例请求：https://krishuang.top/relaxion/qq/songs?keyword=taylor

**返回**

```json
{
    "songs": [
        {
            "platform": "qq",
            "idforres": "004GK4aP4TGbbG",
            "url": "/relaxion/qq/song/004GK4aP4TGbbG",
            "idforcomments": 639141,
            "mvid": "9zlA4bBvZAC",
            "cover": "https://y.gtimg.cn/music/photo_new/T002R300x300M000002Q1XUj3HBAzw.jpg?max_age=2592000",
            "albumname": "Fearless (Platinum Edition)",
            "lrc": "/relaxion/qq/lyric/004GK4aP4TGbbG",
            "name": "Love Story",
            "artist": "Taylor Swift",
            "interval": 235,
            "playable": false
        },
        {
            "platform": "qq",
            "idforres": "003VHaBb0wCHop",
            "url": "/relaxion/qq/song/003VHaBb0wCHop",
            "idforcomments": 9109354,
            "mvid": "m0015ha2gvj",
            "cover": "https://y.gtimg.cn/music/photo_new/T002R300x300M000002Kz5Jo1uzHjz.jpg?max_age=2592000",
            "albumname": "1989 (Deluxe)",
            "lrc": "/relaxion/qq/lyric/003VHaBb0wCHop",
            "name": "Blank Space",
            "artist": "Taylor Swift",
            "interval": 231,
            "playable": false
        }
    ]
}
```



### 获取专辑内容

获取一张专辑中包含的歌

**get**  `/{platform}/songs/album`

**参数**

| 参数名  | 类型   | 必须 | 含义    | 默认 |
| ------- | ------ | ---- | ------- | ---- |
| albumid | String | 是   | 专辑 Id |      |

样例请求：https://krishuang.top/relaxion/wangyi/songs/album?albumid=32311

**返回**

```json
{
    "songs": [
        {
            "platform": "wangyi",
            "idforres": 326696,
            "url": "/relaxion/wangyi/song/326696",
            "idforcomments": 326696,
            "mvid": 0,
            "cover": "https://p2.music.126.net/klOSGBRQhevtM6c9RXrM1A==/18808245906527670.jpg",
            "albumname": "\u795e\u7684\u6e38\u620f",
            "lrc": "/relaxion/wangyi/lyric/326696",
            "name": "\u75af\u72c2\u7684\u9633\u5149",
            "artist": "\u5f20\u60ac",
            "interval": "",
            "playable": false
        },
        ...
    ]
}
```



### 获取评论

**get**  `/{platform}/comments/song`

**get**  `/{platform}/comments/album`

**get**  `/{platform}/comments/mv`

**参数**

| 参数名        | 类型   | 必须 | 含义           | 默认 |
| ------------- | ------ | ---- | -------------- | ---- |
| idforcomments | String | 是   | 获取评论的 Id  |      |
| num           | Number |      | 返回的结果数量 | 20   |
| page          | Number |      | 第几页结果     | 0    |

样例请求：https://krishuang.top/relaxion/wangyi/comments/song?idforcomments=32507038&page=0

**返回**

```json
{
    "hot": {
        "num": 15,
        "comments": [
            {
                "avatar": "https://p2.music.126.net/l14xltOH1KTAJ37qKwOAeg==/109951166692683875.jpg",
                "username": "_\u4f60\u6709\u4e8b\u5417_",
                "content": "\u4e00\u4e2a\u4eba\u80fd\u6709\u591a\u4e0d\u6b63\u7ecf\uff0c\u5c31\u80fd\u6709\u591a\u6df1\u60c5\u3002",
                "stars": 525384,
                "time": "2015-06-08, 11:05:50"
            },
            ...
        ]
    },
    "normal": {
        "num": 294410,
        "comments": [
            {
                "avatar": "https://p2.music.126.net/5u8qPPsQAvQROiYyzWcNyg==/109951166397513774.jpg",
                "username": "\u6563\u573a_dcs",
                "content": "\u5236\u7247\u4eba\u662f\u8d75\u82f1\u4fca",
                "stars": 0,
                "time": "2021-12-07, 18:18:23"
            },
    		...
        ]
    }
}
```



### 歌词

获取一首歌的歌词

**get**  `/{platform}/lyric/{id}`

样例请求：https://krishuang.top/relaxion/wangyi/lyric/32507038

**返回**

```txt
[00:00.000] 作词 : 薛之谦
[00:00.676] 作曲 : 薛之谦
[00:01.352] 编曲 : 郑伟/张宝宇
[00:02.028] 制作人 : 赵英俊
[00:02.704] 合声 : 赵英俊
[00:03.380] 录音师 : 王晓海
[00:04.056] 混音师 : 鲍锐
[00:04.732] 母带工程师 : 鲍锐
[00:05.409]
[00:21.056]简单点
[00:24.967]说话的方式简单点
[00:30.439]递进的情绪请省略
[00:33.369]你又不是个演员
[00:36.016]别设计那些情节
[00:41.795]没意见
[00:45.905]我只想看看你怎么圆
[00:51.415]你难过的太表面
[00:54.338]像没天赋的演员
[00:56.937]观众一眼能看见
[01:02.295]该配合你演出的我演视而不见
[01:07.395]在逼一个最爱你的人即兴表演
[01:12.584]什么时候我们开始收起了底线
[01:17.824]顺应时代的改变看那些拙劣的表演
[01:23.069]可你曾经那么爱我干嘛演出细节
[01:28.423]我该变成什么样子才能延缓厌倦
[01:33.707]原来当爱放下防备后的这些那些
[01:39.105]才是考验
[01:44.899]没意见
[01:48.762]你想怎样我都随便
[01:54.574]你演技也有限
[01:57.210]又不用说感言
[01:59.776]分开就平淡些
[02:05.003]该配合你演出的我演视而不见
[02:10.281]别逼一个最爱你的人即兴表演
[02:15.577]什么时候我们开始没有了底线
[02:20.685]顺着别人的谎言被动就不显得可怜
[02:26.002]可你曾经那么爱我干嘛演出细节
[02:31.284]我该变成什么样子才能配合出演
[02:36.548]原来当爱放下防备后的这些那些
[02:41.810]都有个期限
[02:47.806]其实台下的观众就我一个
[02:52.934]其实我也看出你有点不舍
[02:57.957]场景也习惯我们来回拉扯
[03:02.763]还计较着什么
[03:08.619]其实说分不开的也不见得
[03:13.691]其实感情最怕的就是拖着
[03:19.010]越演到重场戏越哭不出了
[03:24.025]是否还值得
[03:28.865]该配合你演出的我尽力在表演
[03:34.138]像情感节目里的嘉宾任人挑选
[03:39.404]如果还能看出我有爱你的那面
[03:44.602]请剪掉那些情节让我看上去体面
[03:49.795]可你曾经那么爱我干嘛演出细节
[03:55.033]不在意的样子是我最后的表演
[04:00.917]是因为爱你我才选择表演
[04:05.957]这种成全
[04:10.323]
```



### 音乐 url

获取音乐资源

**get**  `/{platform}/uri/song`

重定向到音乐 uri

**get**  `/{platform}/song/{id}`

样例请求：https://krishuang.top/relaxion/wangyi/song/32507038



### MV url

获取 MV 资源

**get**  `/{platform}/uri/mv`

**参数**

| 参数名 | 类型   | 必须 | 含义     | 默认 |
| ------ | ------ | ---- | -------- | ---- |
| mvid   | String | 是   | mv 的 Id |      |

样例请求：https://krishuang.top/relaxion/wangyi/uri/mv?mvid=420144

**返回**

```json
{
    "uri": "http://vodkgeyttp8.vod.126.net/cloudmusic/MTAwMDAiMCQ4ICUgOCFhZg==/mv/420144/abbd384e937b34ee7c22eebdd238dbb9.mp4?wsSecret=6f7fc72e06028658baa99e59e7492f42&wsTime=1638879991"
}
```



### 音乐平台用户的所有歌单

获取音乐平台上用户的歌单，例如网易云音乐某用户的歌单

**get**  `/{platform}/user/songlists`



### 音乐平台歌单中的歌曲

获取某个音乐平台上某个歌单内的歌曲列表

**get**  `/{platform}/songs/songlist`



### 重定向专辑封面

**get**  `/{platform}/albumcover/{id}`



## Run

```
pip install -r requirements.txt
python3 main.py
```




## Acknowledgements

+ [You-Get](https://github.com/soimort/you-get)
+ [NeteaseCloudMusicApi](https://github.com/Binaryify/NeteaseCloudMusicApi)
+ [FeelUOwn](https://github.com/feeluown/FeelUOwn)

