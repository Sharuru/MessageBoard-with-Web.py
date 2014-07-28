import web
import datetime

render = web.template.render('templates/')

#url跳转
urls = (
        '/', 'IndexHandler',
        '/viewPost', 'ViewPost',
        '/newPost', 'NewPostHandler',
        '/deletePost', 'DeletePostHandler'
)

#数据库对象
db = web.database(dbn='sqlite', db = 'MessageRecord.db')

#form表单
##新留言表单
vemail = web.form.regexp(r".*@.*", "Must be a VALID E-mail address!")

newPostForm = web.form.Form(
                            web.form.Textbox('username', description = 'Your Name:'),
                            web.form.Textbox('mail', vemail, description = 'E-mail:'),
                            web.form.Textarea('message', description = 'Message:'),
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
        recvTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if not form.validates():
            return render.index(msgs, form)
        else:
            db.insert('msg', name = form.d.username, mail = form.d.mail, time = recvTime, message = form.d.message)
            return render.newPost()

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
