from .baseview import BaseView, check_args_post, check_args_get, router_recorder
from core import Extractor, Downloader
import os

class Cores(BaseView):
    '''
    this class contains many instrumental functions
    '''

    def __init__(self, config):

        self.__init_path()

        self.extractor = Extractor(config["ffmpeg-path"], config['mediafolder'])

        self.downloader = Downloader(config['mediafolder'])


    def __init_path(self):

        root = os.getcwd()

        self.resource_path = os.path.join(root, 'files')

    async def index(self, request):

        front = './front/deployment/index.html'
        if os.path.exists(front):
            return self._send_file(front)
        
        else:
            return self._redrict_to('/kris/index.html')

    @check_args_post({
        'mvurl': "*",
        'picurl': "",
        'metadata': {}
    })
    async def extractAudio(self, params):

        mvurl = params['mvurl']
        albumcover = params['picurl']
        metadata = params['metadata']

        audiofile = self.extractor.extract_from_url(mvurl, metadata, cover_url = albumcover)

        return self._json_response({"url": "/resource/audios/%s" % audiofile})


    @check_args_post({
        'url': "*",
        'name': "",
    })
    async def downloadRes(self, params):
        return self._textmsg('O(∩_∩)O')

    @check_args_get({
        're_path': '*'
    })
    async def dlProgress(self, params):

        re_path = params['re_path']
        
        return self._json_response({'size': self.downloader.fileSize(re_path)})
