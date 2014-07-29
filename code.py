__author__ = 'Mave'

import web
import datetime

render = web.template.render('templates/')

#urlJump
urls = (
    '/', 'IndexHandler',
    '/newPost', 'NewPostHandler',
    '/delPost-(.*)', 'DeletePostHandler'
)

#Database Object
db = web.database(dbn='sqlite', db='MessageRecord.db')

#form
##NewPostForm
vname = web.form.regexp(r"\w{1,}", "Must Fill Your Name")
vemail = web.form.regexp(r".*@.*", "Must be a VALID E-mail address!")
vmessage = web.form.regexp(r"\w{1,}", "Must Fill Your Message")

newPostForm = web.form.Form(
    web.form.Textbox('username', vname, description='Your Name:'),
    web.form.Textbox('mail', vemail, description='E-mail:'),
    web.form.Textarea('message', vmessage, description='Message:'),
    web.form.Button('Post it!')
)

##DelPostForm
delPostForm = web.form.Form(
    web.form.Button('Delete This Message')
)


class IndexHandler:
    def GET(self):
        msgs = db.select('msg')
        form = newPostForm()
        delbutton = delPostForm()
        return render.index(msgs, form, delbutton)


class NewPostHandler:
    def POST(self):
        msgs = db.select('msg')
        form = newPostForm()
        receive = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        delbutton = delPostForm()
        if not form.validates():
            return render.index(msgs, form, delbutton)
        else:
            db.insert('msg', name=form.d.username, mail=form.d.mail, time=receive, message=form.d.message)
            return render.newPost()


class DeletePostHandler:
    def POST(self, delmsg):
        #msgs = db.select('msg')
        db.delete('msg', where='message=$message', vars={'message': delmsg})
        return render.delPost()

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
