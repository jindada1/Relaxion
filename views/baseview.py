'''
    on: 2019-10-03
    by: kris Huang
'''

from aiohttp import web
import time

class logger(object):
    
    infofile = './logs/records.txt'

    @classmethod
    def log_info(cls, info):

        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        
        mid = info.split('//')[1]

        # get the query string. e.g., /app/blog?id=10
        cls.__writeline("%s -ROUTE: %s" % (t, mid[mid.find('/'):]))

    def __writeline(line):

        with open(logger.infofile, 'a') as f:
            
            f.write(line + '\n')


class router_recorder(object):

    def __init__(self):

        pass

    def __call__(self, handler):
        async def wrapper(caller, request):
            
            req = request.url.human_repr()
            logger.log_info(req)

            return await handler(caller, request)

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

    async def errorHandler(self, errmsg):
        return web.Response(text=errmsg)


class check_args_post(args_check):

    def __init__(self, argSchema):

        args_check.__init__(self, argSchema)

    def __call__(self, handler):
        async def wrapper(caller, request):
            # print("%s is running" % handler.__name__)
            req = request.url.human_repr()
            logger.log_info(req)

            # get form data
            data = await request.json()

            # validate arguments in request according to self.argSchema
            validation = self._validate(data)

            if validation['err']:
                return await self.errorHandler(validation['err'])
            else:
                return await handler(caller, validation)

        return wrapper


class check_args_get(args_check):

    def __init__(self, argSchema):

        args_check.__init__(self, argSchema)

    def __call__(self, handler):
        def wrapper(caller, request):
            # print("%s is running" % handler.__name__)
            req = request.url.human_repr()
            logger.log_info(req)

            # validate arguments in request according to self.argSchema
            validation = self._validate(request.rel_url.query)

            if validation['err']:
                return self.errorHandler(validation['err'])
            else:
                return handler(caller, validation)

        return wrapper


class pltf_get(args_check):
    '''
    Get from platforms 
    '''
    def __init__(self, argSchema):

        args_check.__init__(self, argSchema)

    def __call__(self, handler):

        async def wrapper(caller, request):
            # print("%s is running" % handler.__name__)
            platform = request.match_info['platform']
            req = request.url.human_repr()
            logger.log_info(req)

            # filter invalid platforms
            if caller.parser[platform]:
                validation = self._validate(request.rel_url.query)

                if validation['err']:
                    return await self.errorHandler(validation['err'])

                else:
                    return await handler(caller, caller.parser[platform], validation)

            # handle error platforms
            return await self.errorHandler("platform: %s is not supported" % platform)

        return wrapper


class BaseView(object):
    '''
    this class is a basic View, which contains some basic functions
    '''

    def __init__(self, parameter_list):
        pass

    def _json_response(self, dict_resp):
        return web.json_response(dict_resp)

    def _textmsg(self, msg):
        return web.Response(text=msg)

    def _send_file(self, file_path):
        return web.FileResponse(file_path)

    def _redrict_to(self, url):
        return web.HTTPFound(url)