__author__ = 'Mave'

import models
import form
import views

#All URL JUMP in system should be set here

urls = (
    '/', 'IndexHandler',
    '/newPost', 'NewPostHandler',
    '/delPost', 'DeletePostHandler',
    '/logIn', 'LogInHandler'
)

class IndexHandler:
    def GET(self):
        msgs = models.get_all_comments()
        message_form = form.newPostForm()
        del_button = form.delPostForm()
        return views.render_template('index.html', msgs=msgs, form=message_form, delbutton=del_button)


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