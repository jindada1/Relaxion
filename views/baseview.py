'''
    on: 2019-10-03
    by: kris Huang
'''

from aiohttp import web
import time


class logger(object):

    infofile = './logs/records.txt'

    @classmethod
    def get_query_route(cls, req):

        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        mid = req.split('//')[1]

        return (t, mid[mid.find('/'):])

    @classmethod
    def log_get(cls, info):

        time, query = cls.get_query_route(info)

        # get the query string. e.g., /app/blog?id=10
        cls.__writeline("%s - %5s: %s" % (time, 'GET', query))

    @classmethod
    def log_post(cls, info, data):

        time, query = cls.get_query_route(info)

        # get the query string. e.g., /app/blog?id=10
        cls.__writeline("%s - %5s: %s - DATA: %s" %
                        (time, 'POST', query, data))

    @classmethod
    def __writeline(cls, line):
        try:
            with open(logger.infofile, 'a') as f:
                f.write(line + '\n')

        except:
            print(line)


class router_recorder(object):

    def __init__(self):

        pass

    def __call__(self, handler):
        async def wrapper(view, request):

            req = request.url.human_repr()
            logger.log_get(req)

            return await handler(view, request)

        return wrapper


class args_check(object):

    def __init__(self, argSchema):
        self.argSchema = argSchema

    def _validate(self, dict_args):
        params = {}

        for arg, prpty in self.argSchema.items():
            # get value
            if arg in dict_args.keys():
                params[arg] = dict_args[arg]

            else:
                # if param is required, raise error
                if prpty == "*":
                    return {"err": "%s is required" % arg}
                # set default value
                params[arg] = prpty

        params["err"] = ""
        return params


class check_args_post(args_check):

    def __init__(self, argSchema):

        args_check.__init__(self, argSchema)

    def __call__(self, handler):
        async def wrapper(view, request):
            # print("%s is running" % handler.__name__)
            req = request.url.human_repr()

            # get form data
            data = await request.json()

            logger.log_post(req, data)

            # validate arguments in request according to self.argSchema
            validation = self._validate(data)

            if validation['err']:
                return view._textmsg(validation['err'])
            else:
                return await handler(view, validation)

        return wrapper


class check_args_get(args_check):

    def __init__(self, argSchema):

        args_check.__init__(self, argSchema)

    def __call__(self, handler):
        def wrapper(view, request):
            # print("%s is running" % handler.__name__)
            req = request.url.human_repr()
            logger.log_get(req)

            # validate arguments in request according to self.argSchema
            validation = self._validate(request.rel_url.query)

            if validation['err']:
                return view._textmsg(validation['err'])
            else:
                return handler(view, validation)

        return wrapper


class check_args_upload(args_check):

    def __init__(self, argSchema):

        args_check.__init__(self, argSchema)

    def __call__(self, handler):
        async def wrapper(view, request):
            # print("%s is running" % handler.__name__)
            req = request.url.human_repr()

            # get form data
            data = await request.post()

            logger.log_post(req, data)

            # validate arguments in request according to self.argSchema
            meta = self._validate(data)

            try:
                meta['file'] = data['file'].file.read()
            except:
                meta['err'] = 'no file'

            if meta['err']:
                return view._textmsg(meta['err'])

            else:
                return await handler(view, meta)

        return wrapper


class pltf_get(args_check):
    '''
    Get from platforms 
    '''
    def __init__(self, argSchema):

        args_check.__init__(self, argSchema)

    def __call__(self, handler):

        async def wrapper(view, request):
            # print("%s is running" % handler.__name__)
            platform = request.match_info['platform']
            req = request.url.human_repr()
            logger.log_get(req)

            # filter invalid platforms
            if view.parser[platform]:
                validation = self._validate(request.rel_url.query)

                if validation['err']:
                    return view._textmsg(validation['err'])

                else:
                    return await handler(view, view.parser[platform], validation)

            # handle error platforms
            return view._textmsg("platform: %s is not supported" % platform)

        return wrapper


class redirect(object):

    def __init__(self, response_type = 'txt'):

        self.response_type = response_type

    def __call__(self, handler):

        async def wrapper(view, request):

            if self.response_type == 'url':
                return_func = view._redrict_to
            else:
                return_func = view._textmsg

            platform = request.match_info['platform']
            _id = request.match_info['id']
            req = request.url.human_repr()
            logger.log_get(req)

            # filter invalid platforms
            if view.parser[platform]:
                cache = view.get_cache(req)
                
                if not type(cache) is dict:
                    # not dict means readable, hit cache
                    return return_func(cache)

                result = await handler(view, view.parser[platform], _id)
                view.set_cache(cache, result)
                return return_func(result)

            # handle error platforms
            return view._textmsg("platform: %s is not supported" % platform)
        return wrapper
    

class BaseView(object):
    '''
    this class is a basic View, which contains some basic functions
    '''

    def __init__(self):
        self.cache = {}
        self.TIME_SPAN = 60 * 60 * 10

    def set_cache(self, cache_block, response):
        # in order to change self.cache, must use dict[key]...
        cache_block['content'] = response
        cache_block['time'] = int(time.time())

    def get_cache(self, req):
        mid = req.split('//')[1]
        route = mid.split('/')[1:]

        cache_block = self.cache
        for layer in route:
            if not layer in cache_block:
                cache_block[layer] = {}
            cache_block = cache_block[layer]

        # block is {}, writable must be dict
        if not cache_block:
            return cache_block

        # block is {'content':---,'time': <effect>}, readable can be any type
        if int(time.time()) - cache_block['time'] < self.TIME_SPAN:
            return cache_block['content']

        # block is {'content':---,'time': <outdate>}, writable must be dict
        else:
            return cache_block

    def _json_response(self, dict_resp):
        return web.json_response(dict_resp)

    def _textmsg(self, msg):
        return web.Response(text=msg)

    def _send_file(self, file_path):
        return web.FileResponse(file_path)

    def _redrict_to(self, url):
        return web.HTTPFound(url)
