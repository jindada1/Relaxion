import baseparser


class WangYiparser(baseParser):
	def __init__(self, baseurl):
        self.baseurl = baseurl

    # override
    def search(self, parameter_list):
        return "search result"

    # override
    def mvuri(self, parameter_list):
        return "mvuri"
    
    # override
    def musicuri(self, parameter_list):
        return "musicuri"
