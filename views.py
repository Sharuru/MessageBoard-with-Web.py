__author__ = 'Mave'

import os
from time import ctime
from web import input, setcookie, cookies
from jinja2 import Environment, FileSystemLoader
from form import newPostForm, logInForm
from models import insert_in_msg, delete_in_msg, session, Msg, Admin


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
        msgs = session.query(Msg).all()
        message_form = newPostForm()
        return render_template('index.html', msgs=msgs, form=message_form,
                               manage=cookies().get('isAdmin') == "Shimakaze,Go!")

    def POST(self):
        setcookie('isAdmin', "", 1800)
        return render_template('logIn.html', loginFlag='Logout')


class NewPostHandler:
    def POST(self):
        msgs = session.query(Msg).all()
        message_form = newPostForm()
        receive_time = ctime()
        if not message_form.validates():
            return render_template('index.html', msgs=msgs, form=message_form, is_input_legal=False)
        else:
            insert_in_msg(message_form.d.username, message_form.d.mail, receive_time, message_form.d.message)
            return render_template('newPost.html')


class DeletePostHandler:
    def POST(self):
        msgid = input().id
        #delete_in_msg(msgid)
        msg = session.query(Msg).filter(Msg.id == msgid).one()
        session.orm.delete(msg)
        return render_template('delPost.html')


class LogInHandler:
    def GET(self):
        return render_template('logIn.html', loginFlag=False)

    def POST(self):
        login_form = logInForm()
        if not login_form.validates():
            return render_template('logIn.html', loginFlag=False)
        else:
            log_check = session.query(Admin).all()
            for record in log_check:
                if login_form.d.admin_name == record.admin_name:
                    if login_form.d.admin_pass == record.admin_pass:
                        setcookie('isAdmin', "Shimakaze,Go!", 1800)
                        return render_template('logIn.html', loginFlag=True)
                    else:
                        return render_template('logIn.html', loginFlag=False)
                else:
                    return render_template('logIn.html', loginFlag=False)