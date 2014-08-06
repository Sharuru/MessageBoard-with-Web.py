__author__ = 'Mave'

from web import application
import urls

if __name__ == "__main__":
    app = application(urls.urls, globals())
    app.run()