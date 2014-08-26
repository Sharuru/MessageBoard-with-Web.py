__author__ = 'Mave'

import os
from time import ctime
from web import input, setcookie, cookies, ctx
from jinja2 import Environment, FileSystemLoader
from form import newPostForm, logInForm
from models import Msg, Admin


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


def link_database(page):
    try_times = 5
    for times in range(0, try_times):
        try:
            object = ctx.orm.query(Msg).order_by(Msg.msgid.desc()).limit(8).offset((page - 1) * 8).all()
            return object
        except:
            ctx.orm.rollback()
            pass


class IndexHandler:
    def GET(self):
        page = int(input(page=1).page)
        msgs = link_database(page)
        t_page = ctx.orm.query(Msg).count()/8 + 1
        message_form = newPostForm()
        return render_template('index.html', msgs=msgs, form=message_form,
                               manage=cookies().get('isAdmin') == "Shimakaze,Go!", page=page, t_page=t_page)

    def POST(self):
        setcookie('isAdmin', "", 1800)
        return render_template('logIn.html', loginFlag='Logout')


class NewPostHandler:
    def POST(self):
        page = int(input(page=1).page)
        msgs = link_database(page)
        t_page = ctx.orm.query(Msg).count()/8 + 1
        message_form = newPostForm()
        receive_time = ctime()
        if not message_form.validates():
            return render_template('index.html', msgs=msgs, form=message_form, is_input_legal=False, page=page, t_page=t_page)
        else:
            new_msg = Msg(name=message_form.d.username, mail=message_form.d.mail, time=receive_time,
                          message=message_form.d.message)
            ctx.orm.add(new_msg)
        return render_template('newPost.html')


class DeletePostHandler:
    def POST(self):
        del_msg = ctx.orm.query(Msg).filter(Msg.msgid == input().id).one()
        ctx.orm.delete(del_msg)
        return render_template('delPost.html')


class LogInHandler:
    def POST(self):
        login_form = logInForm()
        if not login_form.validates():
            return render_template('logIn.html', loginFlag=False)
        else:
            log_check = ctx.orm.query(Admin).all()
            for record in log_check:
                if login_form.d.admin_name == record.admin_name:
                    if login_form.d.admin_pass == record.admin_pass:
                        setcookie('isAdmin', "Shimakaze,Go!", 1800)
                        return render_template('logIn.html', loginFlag=True)
                    else:
                        return render_template('logIn.html', loginFlag=False)
                else:
                    return render_template('logIn.html', loginFlag=False)
