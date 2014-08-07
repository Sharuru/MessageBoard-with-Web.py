__author__ = 'Mave'

import web
import urls
from views import *

application = web.application(urls.urls, globals()).wsgifunc()

if __name__ == "__main__":
    app = web.application(urls.urls, globals())
    app.run()
