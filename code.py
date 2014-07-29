__author__ = 'Mave'

import web
import datetime
import os
from jinja2 import Environment, FileSystemLoader


def render_template(template_name, **context):
    extensions = context.pop('extensions', [])
    globals = context.pop('globals', {})

    jinja_env = Environment(
        loader=FileSystemLoader(os.path.join(os.path.dirname(__file__), 'templates')),
        extensions=extensions,
            )
    jinja_env.globals.update(globals)

    #jinja_env.update_template_context(context)
    return jinja_env.get_template(template_name).render(context)

#urlJump
urls = (
    '/', 'IndexHandler',
    '/newPost', 'NewPostHandler',
    '/delPost-(.*)', 'DeletePostHandler',
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
        return render_template('index.html', msgs=msgs, form=form, delbutton=delbutton)


class NewPostHandler:
    def POST(self):
        msgs = db.select('msg')
        form = newPostForm()
        receive = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        delbutton = delPostForm()
        if not form.validates():
            return render_template('index.html', msgs=msgs, form=form, delbutton=delbutton)
        else:
            db.insert('msg', name=form.d.username, mail=form.d.mail, time=receive, message=form.d.message)
            return render_template('newPost.html')


class DeletePostHandler:
    def POST(self, delmsg):
        db.delete('msg', where='message=$message', vars={'message': delmsg})
        return render_template('delPost.html')

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
