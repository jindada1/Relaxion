from .baseview import BaseView, check_args_post, check_args_get, router_recorder
import os

class Cores(BaseView):
    '''
    this class contains many instrumental functions
    '''
    def __init__(self, workers):

        self.extractor = workers[0]

        self.downloader = workers[1]

    @router_recorder()
    async def index(self, request):

        return self._send_file('./front/templates/index.html')

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

        video = await self.downloader.download(mvurl, metadata['title'], 'mp4')

        if video['err']:
            return self._json_response({"err": video['err']})

        if albumcover:
            cover = await self.downloader.download(albumcover, metadata['album'], 'jpg')
            albumcover = cover['content']

        path, audiofile = self.extractor.extract(video['content'], metadata, albumcover)
        
        return self._json_response({"url": "/resource/audios/%s" % audiofile})
    