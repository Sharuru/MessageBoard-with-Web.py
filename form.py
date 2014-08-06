__author__ = 'Mave'

from web import form

#All FORM in system should be set here

##NewPostForm
email_verify = form.regexp(r".*@.*", "Must be a VALID E-mail address!")

newPostForm = form.Form(
    form.Textbox('username', description='Your Name:'),
    form.Textbox('mail', email_verify, description='E-mail:'),
    form.Textarea('message', description='Message:'),
    form.Button('Post it!')
)

##DelPostForm
delPostForm = form.Form(
    form.Button('Delete This Message')
)

##LogInForm
admin_name_verify = form.regexp(r"\w{1,}", "Must Fill Your Account")
admin_pass_verify = form.regexp(r"\w{1,}", "Must Fill Your Password")

logInForm = form.Form(
    form.Textbox('admin_name', admin_name_verify, description='Administrator:'),
    form.Password('admin_pass', admin_pass_verify, description='Password:'),
    form.Button('login', html='Login'),
)