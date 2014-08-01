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
        del_button = delPostForm()
        return render_template('index.html', msgs=msgs, form=form, delbutton=del_button,
                               manage=web.cookies().get('isAdmin') == "Shimakaze,Go!")  # pythonic


class NewPostHandler:
    def POST(self):
        msgs = db.select('msg')
        form = newPostForm()
        receive = time.ctime()
        del_button = delPostForm()
        login_button = gotoLoginButton()
        if not form.validates():
            return render_template(
                'index.html', msgs=msgs, form=form, delbutton=del_button, loginbutton=login_button, is_input_legal=False
            )
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
        return render_template('logIn.html', loginFlag=False)

    def POST(self):
        login_form = logInForm()
        if not login_form.validates():
            return render_template('logIn.html', loginFlag=False)
        else:
            log_check = db.select('admin')
            for record in log_check:
                if login_form.d.adusername == record.adusername:
                    if login_form.d.adpassword == record.adpassword:
                        web.setcookie('isAdmin', "Shimakaze,Go!", 1800)
                        return render_template(
                            'logIn.html', loginFlag=True)
                    else:
                        return render_template('logIn.html', loginFlag=False)
                else:
                    return render_template('logIn.html', loginFlag=False)

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
