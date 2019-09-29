import os
import aiofiles
from aiohttp import ClientSession

class downloader(object):

    '''
    this class can download file from url and set file name
    '''

    def __init__(self, folder):

        self.__version = "1.0"

        self.__MaxTasks = 10

        self.__tasksCount = 0

        self.__headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
        }

        self.rootFolder = folder

        self.__subfolders = ["audios", "videos", "pics"]

        if not os.path.exists(folder):
            os.makedirs(folder)

        for sub in self.__subfolders:
            p = os.path.join(folder, sub)
            if not os.path.exists(p):
                os.makedirs(p)

        print('[ok] init downloader, local folder is %s' % folder)


    def __realfolder(self, fname, ftype):

        ftypes = {
            "mp3" : 0,
            "mp4" : 1,
            "jpg" : 2
        }

        # 这里下载好的文件会成为 ffmpeg 命令行的输入，去掉空格
        fname = fname.replace(" ","")

        p = os.path.join(self.rootFolder, self.__subfolders[ftypes[ftype]], "%s.%s" % (fname, ftype))

        return  p
        
    def __err(self, s):

        return {
            'err': s,
            'content': ''
        }

    def __succ(self, s):

        return {
            'err': '',
            'content': s
        }

    async def download(self, url, name, ftype = None):

        if self.__tasksCount > self.__MaxTasks:

            return self.__err('too many tasks')
        
        ftype = ftype.replace(".","")

        path = self.__realfolder(name, ftype)

        if os.path.exists(path):
            
            return self.__succ(path)

        self.__tasksCount += 1

        async with ClientSession(headers=self.__headers) as session:

            async with session.get(url) as resp:

                if resp.status == 200:

                    f = await aiofiles.open(path, mode='wb')

                    await f.write(await resp.read())
                    await f.close()
                
                    self.__tasksCount -= 1
                    return self.__succ(path)
    
        self.__tasksCount -= 1
        return self.__err('download error')


async def __test():
    
    D = downloader("F:\\Project\\Relaxion\\files")

    url = "http://183.216.186.152/vcloud1049.tc.qq.com/1049_M0120400000XRaMW2cOTWo1001678050.f9844.mp4?vkey=518588DE46DF988A3B70825853C8017AE2F980B51DEB46A14F4A6B915EB0DD2C7C56640C93BF281F4E8DC3C9FBE6174B046EE4A7B98D254563A810F36366D04713EFFC4EF98FBE03B351439F25103FE9634AF157AD451173"
    name = "说好不哭（with 五月天阿信）"
    
    video = await D.download(url, name, 'mp4')

    print(video)

if __name__ == '__main__':
    import asyncio
    loop = asyncio.get_event_loop()
    loop.run_until_complete(__test())
    loop.close()