__author__ = 'Mave'

import web
from sqlalchemy.orm import scoped_session, sessionmaker
import urls
from views import *
from models import engine


reload(__import__('sys')).setdefaultencoding('utf-8')


def load_sqla(handler):
    web.ctx.orm = scoped_session(sessionmaker(bind=engine))
    try:
        return handler()
    except web.HTTPError:
       web.ctx.orm.commit()
       raise
    except:
        web.ctx.orm.rollback()
        raise
    finally:
        web.ctx.orm.commit()


app = web.application(urls.urls, globals())
app.add_processor(load_sqla)
application = app.wsgifunc()

if __name__ == "__main__":
    app.run()
