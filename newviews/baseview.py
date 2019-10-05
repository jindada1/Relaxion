'''
    on: 2019-10-03
    by: kris Huang
'''

from aiohttp import web


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
            req = request.path_qs
            print(req)

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
            req = request.path_qs
            print(req)

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
            req = request.path_qs
            print(req)

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