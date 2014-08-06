__author__ = 'Mave'

import os
import time
import web
from jinja2 import Environment, FileSystemLoader
import form
import models


def render_template(template_name, **context):
    extensions = context.pop('extensions', [])
    globals = context.pop('globals', {})
    jinja_env = Environment(
        loader=FileSystemLoader(os.path.join(os.path.dirname(__file__), 'templates')),
        extensions=extensions,
        autoescape=True
    )
    jinja_env.globals.update(globals)
    return jinja_env.get_template(template_name).render(context)


class IndexHandler:
    def GET(self):
        msgs = models.select_table('msg')
        message_form = form.newPostForm()
        return render_template('index.html', msgs=msgs, form=message_form,
                               manage=web.cookies().get('isAdmin') == "Shimakaze,Go!")

    def POST(self):
        web.setcookie('isAdmin', "", 1800)
        return render_template('logIn.html', loginFlag='Logout')


class NewPostHandler:
    def POST(self):
        msgs = models.select_table('msg')
        message_form = form.newPostForm()
        receive_time = time.ctime()
        if not message_form.validates():
            return render_template('index.html', msgs=msgs, form=message_form, is_input_legal=False)
        else:
            models.insert_in_msg(message_form.d.username, message_form.d.mail, receive_time, message_form.d.message)
            return render_template('newPost.html')


class DeletePostHandler:
    def POST(self):
        msgid = web.input().id
        models.delete_in_msg(msgid)
        return render_template('delPost.html')


class LogInHandler:
    def GET(self):
        return render_template('logIn.html', loginFlag=False)

    def POST(self):
        login_form = form.logInForm()
        if not login_form.validates():
            return render_template('logIn.html', loginFlag=False)
        else:
            log_check = models.select_table('admin')
            for record in log_check:
                if login_form.d.admin_name == record.adusername:
                    if login_form.d.admin_pass == record.adpassword:
                        web.setcookie('isAdmin', "Shimakaze,Go!", 1800)
                        return render_template('logIn.html', loginFlag=True)
                    else:
                        return render_template('logIn.html', loginFlag=False)
                else:
                    return render_template('logIn.html', loginFlag=False)