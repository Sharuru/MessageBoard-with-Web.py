__author__ = 'Mave'

from web.form import regexp, Form, Textbox, Textarea, Password, Button

#All FORM in system should be set here

##NewPostForm
email_verify = regexp(r".*@.*", "Must be a VALID E-mail address!")

newPostForm = Form(
    Textbox('username', description='Your Name:'),
    Textbox('mail', email_verify, description='E-mail:'),
    Textarea('message', description='Message:'),
    Button('Post it!')
)

##LogInForm
admin_name_verify = regexp(r"\w{1,}", "Must Fill Your Account")
admin_pass_verify = regexp(r"\w{1,}", "Must Fill Your Password")

logInForm = Form(
    Textbox('admin_name', admin_name_verify, description='Administrator:'),
    Password('admin_pass', admin_pass_verify, description='Password:'),
    Button('login', html='Login'),
)