__author__ = 'Mave'

from web import application
import urls
from views import *

#application = application(urls.urls, globals()).wsgifunc()

if __name__ == "__main__":
    app = application(urls.urls, globals())
    app.run()
