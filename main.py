__author__ = 'Mave'

import web
import urls
from views import *

reload(__import__('sys')).setdefaultencoding('utf-8')

application = web.application(urls.urls, globals()).wsgifunc()

if __name__ == "__main__":
    app = web.application(urls.urls, globals())
    app.run()
