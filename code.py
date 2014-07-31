__author__ = 'Mave'

import web
import time
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
    '/delPost', 'DeletePostHandler',
    '/logIn', 'LogInHandler'
)

#Database Object
db = web.database(dbn='sqlite', db='MessageRecord.db')

#form
##NewPostForm
vemail = web.form.regexp(r".*@.*", "Must be a VALID E-mail address!")

newPostForm = web.form.Form(
    web.form.Textbox('username', description='Your Name:', class_='input'),
    web.form.Textbox('mail', vemail, description='E-mail:', class_='input'),
    web.form.Textarea('message', description='Message:', class_='input'),
    web.form.Button('Post it!')
)

##DelPostForm
delPostForm = web.form.Form(
    web.form.Button('Delete This Message')
)

##LogInForm
vadname = web.form.regexp(r"\w{1,}", "Must Fill Your Account")
vadpass = web.form.regexp(r"\w{1,}", "Must Fill Your Password")

logInForm = web.form.Form(
    web.form.Textbox('adusername', vadname, description='Administrator:'),
    web.form.Password('adpassword', vadpass, description='Password:'),
    web.form.Button('login', html='Login'),
)

gotoLoginButton = web.form.Form(
    web.form.Button('gotologin', html='Goto Login')
)


class IndexHandler:
    def GET(self):
        msgs = db.select('msg')
        form = newPostForm()
        delbutton = delPostForm()
        loginbutton = gotoLoginButton()
        if web.cookies().get('isAdmin') == "Shimakaze,Go!":
            return render_template(
                'index.html', msgs=msgs, form=form, delbutton=delbutton, loginbutton=loginbutton, manage=True
            )
        else:
            return render_template(
                'index.html', msgs=msgs, form=form, delbutton=delbutton, loginbutton=loginbutton, manage=False
            )



class NewPostHandler:
    def POST(self):
        msgs = db.select('msg')
        form = newPostForm()
        receive = time.ctime()
        delbutton = delPostForm()
        loginbutton = gotoLoginButton()
        if not form.validates():
            return render_template('index.html', msgs=msgs, form=form, delbutton=delbutton, loginbutton=loginbutton)
        else:
            db.insert('msg', name=form.d.username, mail=form.d.mail, time=receive, message=form.d.message)
            return render_template('newPost.html')


class DeletePostHandler:
    def POST(self):
        delmsg = web.input().id
        db.delete('msg', where='msgid=$msgid', vars={'msgid': delmsg})
        return render_template('delPost.html')

class LogInHandler:
    def GET(self):
        loginform = logInForm()
        return render_template('logIn.html', loginform=loginform, loginFlag=False)
    def POST(self):
        loginform = logInForm()
        if not loginform.validates():
            return render_template('logIn.html', loginform=loginform)
        else:
            logcheck = db.select('admin')
            for record in logcheck:
                if loginform.d.adusername == record.adusername:
                    if loginform.d.adpassword == record.adpassword:
                        web.setcookie('isAdmin', "Shimakaze,Go!", 1800)
                        return render_template(
                            'logIn.html', loginform=loginform, loginFlag=True)
                    else:
                        return render_template('logIn.html', loginform=loginform, loginFlag=False)
                else:
                    return render_template('logIn.html', loginform=loginform, loginFlag=False)

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
