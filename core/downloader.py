import os
import threading
import asyncio
from aiohttp import ClientSession


class Downloader(object):

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
            "mp3": 0,
            "mp4": 1,
            "jpg": 2
        }

        # 这里下载好的文件会成为 ffmpeg 命令行的输入，去掉空格
        fname = fname.replace(" ", "")

        re_p = os.path.join(self.__subfolders[ftypes[ftype]], "%s.%s" % (fname, ftype))

        ab_p = os.path.join(self.rootFolder, re_p)

        return (ab_p, re_p)

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

    def __info(self, path, size = None):

        return {
            'err': '',
            'path': path,
            'size': size
        }


    def fileSize(self, re_path):

        path = os.path.join(self.rootFolder, re_path)

        return os.path.getsize(path)

    async def getFile(self, url, name, ftype=None):

        ftype = ftype.replace(".", "")

        path, re_path = self.__realfolder(name, ftype)

        if os.path.exists(path):

            return self.__info(re_path, self.fileSize(re_path))

        async with ClientSession(headers=self.__headers) as session:

            async with session.get(url) as resp:

                if resp.status == 200:

                    total = int(resp.headers.get('content-length', 0)) or None

                    t = threading.Thread(
                        target=self.startDownload, args=(url, path, ))

                    t.start()

        return self.__info(re_path, total)


    def startDownload(self, url, path):

        loop = asyncio.new_event_loop()

        loop.run_until_complete(self.new_download(url, path))

        loop.close()


    async def new_download(self, url, path):

        async with ClientSession(headers=self.__headers) as session:

            async with session.get(url) as resp:

                if resp.status == 200:

                    with open(path, mode='wb') as f:

                        async for chunk in resp.content.iter_chunked(512*1024):

                            f.write(chunk)

        print('finish download')


async def __test():

    D = Downloader("D:\\Project\\Relaxion\\files")

    url = "http://114.80.26.23/mv.music.tc.qq.com/AUkXJzGIJH6356SQ2VM3fRl0EScg2e5_l4XBYl8NKzn8/2459986F9BE0504A8E7AA7A5C9A86E2320D40CDAB352C34EFF8A252707F45948A92D27D28965C054FFDD9635B08EEC7CZZqqmusic_default/1049_M0135300000HdtXk2avwNV1001676254.f9844.mp4?fname=1049_M0135300000HdtXk2avwNV1001676254.f9844.mp4"
    name = "说好不哭（with 五月天阿信）"

    video = await D.getFile(url, name, 'mp4')

    print(video)

if __name__ == '__main__':
    import asyncio
    loop = asyncio.get_event_loop()
    loop.run_until_complete(__test())
    loop.close()