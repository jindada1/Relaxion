# Relaxion 

[![Build Status](https://travis-ci.com/jindada1/Relaxion.svg?branch=master)](https://travis-ci.com/jindada1/Relaxion)

An aiohttp server, fetching musics from multiple platforms. it can serve as music app's backend, providing services below

*DISCLAIMER: This is an experimental software. **Please do not use it for commercial purposes**!!!*



## Internal User Service

- [x] sign in / up
- [x] like / unlike songs



## External Music Service

| platform                               | search | listen | watch | comments | account |
| -------------------------------------- | ------ | ------ | ----- | -------- | ------- |
| [QQ](https://y.qq.com/)                | √      | √      | √     | √        |         |
| [Netease](https://music.163.com/)      | √      | √      | √     | √        |         |
| [KuGou](https://www.kugou.com/)        | √      | √      | √     |          |         |
| [KuWo Music](http://www.kuwo.cn/)      | √      | √      | √     |          |         |
| [MiGu Music](https://music.migu.cn/v3) |        |        |       |          |         |



## Run

```
pip install -r requirements.txt
python3 main.py
```



## Acknowledgements

+ [You-Get](https://github.com/soimort/you-get)
+ [NeteaseCloudMusicApi](https://github.com/Binaryify/NeteaseCloudMusicApi)
+ [FeelUOwn](https://github.com/feeluown/FeelUOwn)

