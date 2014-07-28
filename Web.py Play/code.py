import web
import time

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
newPostForm = web.form.Form(
                            web.form.Textbox('Your Name'),
                            web.form.Textarea('Message'),
                            web.form.Button('Post it!')
)

class IndexHandler:
    def GET(self):
        msgs = db.select('msg')
        return render.index(msgs)

class NewPostHandler:
    def POST(self):
        form = newPostForm()
        return render.newPost(form)

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()