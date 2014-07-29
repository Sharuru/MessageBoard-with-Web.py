__author__ = 'Mave'

import web
import datetime

render = web.template.render('templates/')

#urlJump
urls = (
    '/', 'IndexHandler',
    '/viewPost', 'ViewPost',
    '/newPost', 'NewPostHandler',
    '/deletePost', 'DeletePostHandler'
)

#Database Object
db = web.database(dbn='sqlite', db='MessageRecord.db')

#form
##NewPostForm
vemail = web.form.regexp(r".*@.*", "Must be a VALID E-mail address!")

newPostForm = web.form.Form(
    web.form.Textbox('username', description='Your Name:'),
    web.form.Textbox('mail', vemail, description='E-mail:'),
    web.form.Textarea('message', description='Message:'),
    web.form.Button('Post it!')
)


class IndexHandler:
    def GET(self):
        msgs = db.select('msg')
        form = newPostForm()
        return render.index(msgs, form)


class NewPostHandler:
    def POST(self):
        msgs = db.select('msg')
        form = newPostForm()
        receive = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if not form.validates():
            return render.index(msgs, form)
        else:
            db.insert('msg', name=form.d.username, mail=form.d.mail, time=receive, message=form.d.message)
            return render.newPost()

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
