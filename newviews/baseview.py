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

    async def errorHandler(errmsg):
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


class BaseView(object):
    '''
    this class is a basic View, which contains some basic functions
    '''

    def __init__(self, parameter_list):
        pass

    def _json_response(self, dict_resp):
        return web.json_response(dict_resp)
