import baseparser


class QQparser(baseParser):
	def __init__(self, baseurl):
        self.baseurl = baseurl

    # override
    def search(self, parameter_list):
        return "QQparser search result"

    # override
    def mvuri(self, parameter_list):
        return "QQparser mvuri"

    # override
    def musicuri(self, parameter_list):
        return "QQparser musicuri"
