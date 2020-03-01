# Relaxion 娱乐中心 

## 内部服务（所有用户数据均属于本项目）

- [x] 登录/注册
- [x] 收藏（/取消收藏）歌曲【歌单数据存在本平台】
- [ ] 收藏（/取消收藏）视频【看单数据存在本平台】

## 外部音乐（数据来源于其它平台）

### QQ音乐

- [x] 搜索 = 【单曲 + MV + 专辑】
- [x] 听歌 = 【音频资源 + 歌词 + 专辑封面】
- [x] 看MV = 【视频资源 + 封面】
- [x] 通过输入QQ号，获取该QQ用户的公开歌单
- [x] 评论 = 【歌曲评论 + 专辑评论 + MV评论】


### 网易云音乐

- [x] 搜索 = 【单曲 + MV + 专辑】
- [x] 听歌 = 【音频资源 + 歌词 + 专辑封面】
- [x] 看MV = 【视频资源 + 封面】
- [x] 通过输入网易云音乐的用户名，获取该用户的公开歌单
- [x] 评论 = 【歌曲评论 + 专辑评论 + MV评论】

### 酷狗音乐

- [x] 搜索 = 【单曲 + MV + 专辑】
- [x] 听歌 = 【音频资源 + 歌词 + 专辑封面】
- [x] 看MV = 【视频资源 + 封面】

### 咪咕音乐

## 外部视频（来源于其它平台）

### 腾讯视频

### 爱奇艺

### 优酷

- [x] 通过输入视频 id，获取该视频资源链接

## 文档与说明

+ apigateway [api doc](https://apizza.net/pro/#/project/01eec0c96c62477ce9c7c88a7cacef22/browse)

**run**

```
pip install -r requirements.txt
python3 gateWay.py
```

**技术栈**

+ development
  + aiohttp Server api网关
  + aiohttp Client 爬虫
  + sqlite 用户数据，其它资源存储
  + ffmpeg 分离音视频流

+ deployment
  + nginx [sites-available.conf](https://github.com/jindada1/Relaxion/blob/master/nginx.conf)

+ requirements
  + python3.x
  + aiohttp_cors
  + aiohttp
  + asyncio