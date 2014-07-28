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
        form = newPostForm()
        recvTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if not form.validates():
            return render.newPost(form, False, recvTime)
        else:
            return render.newPost(form, True, recvTime)
            #return render.newPost(form)
            #return web.seeother('/')
            #return render.newPost(web.form.username)

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
