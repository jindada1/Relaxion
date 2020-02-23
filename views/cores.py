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

        self.administrator = os.path.join(root, 'front/administrator')

        self.resource_path = os.path.join(root, 'files')

    async def index(self, request):

        return self._send_file('./front/deployment/index.html')

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
