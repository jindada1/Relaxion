from .baseview import BaseView, check_args_post, check_args_get, router_recorder
import os


class Cores(BaseView):
    '''
    this class contains many instrumental functions
    '''

    def __init__(self, workers):

        self.__init_path()

        self.extractor = workers[0]

        self.downloader = workers[1]

    def __init_path(self):

        root = os.getcwd()

        self.front_path = os.path.join(root, 'front')

        self.resource_path = os.path.join(root, 'files')

    @router_recorder()
    async def index(self, request):

        f = os.path.join(self.front_path, 'templates', 'index.html')

        if os.path.exists(f):
            return self._send_file('./front/templates/index.html')

        return self._json_response({'err': "no index file"})

    @router_recorder()
    async def pages(self, request):

        page = request.match_info['page']
        page = page.split('.')[0] + '.html'

        f = os.path.join(self.front_path, 'templates', page)

        if os.path.exists(f):
            return self._send_file(f)

        return self._json_response({'err': "no html file named %s" % page})

    @router_recorder()
    async def static(self, request):

        filename = request.match_info['filename']

        return self._send_file('./front/static/' + filename)

    @router_recorder()
    async def getResource(self, request):

        ftype = request.match_info['ftype']
        fname = request.match_info['fname']

        path = os.path.join('./files/', ftype, fname)

        if os.path.exists(path):
            return self._send_file(path)

        return self._textmsg("no file error")

    @check_args_post({
        'mvurl': "*",
        'picurl': "",
        'metadata': {}
    })
    async def extractAudio(self, params):

        mvurl = params['mvurl']
        albumcover = params['picurl']
        metadata = params['metadata']

        audiofile = self.extractor.getAudio(metadata['title'])

        if not audiofile:
            
            video = await self.downloader.download(mvurl, metadata['title'], 'mp4')

            if video['err']:
                return self._json_response({"err": video['err']})

            audiofile = self.extractor.extract(video['content'], metadata)

        return self._json_response({"url": "/resource/audios/%s" % audiofile})

    @check_args_post({
        'mvurl': "*",
        'picurl': "",
        'metadata': {}
    })
    async def downloadRes(self, params):

        mvurl = params['mvurl']
        albumcover = params['picurl']
        metadata = params['metadata']

        video = await self.downloader.getFile(mvurl, metadata['title'], 'mp4')

        if video['err']:
            return self._json_response({"err": video['err']})

        if albumcover:
            cover = await self.downloader.getFile(albumcover, metadata['album'], 'jpg')

        return self._json_response(video)

    @check_args_get({
        're_path': '*'
    })
    async def dlProgress(self, params):

        re_path = params['re_path']
        
        return self._json_response({'size': self.downloader.fileSize(re_path)})