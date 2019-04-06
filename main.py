from flask import Flask, redirect, render_template, request

app = Flask(__name__)
app.config['DEBUG'] = True

@app.route("/")
def index():
    return render_template("sign-up.html")

def verify_field(text, text_type):
    if not text:
        error = text_type + " cannot be empty."
    elif text.find(" ") != -1 or len(text) < 3 or len(text)> 20 :
        error = "Not a valid {0}.(No spaces, length between 3-20)".format(text_type)
    else:
        error=""
    
    return error
 
def confirm_pwd(password, verify_password):
    if password != verify_password:
        error = "Passwords don't match."
    else:
        error = ""
    return error

def verify_email(text):
    error = verify_field(text, "Email")
    
    if text.find('@') == -1 or text.find('.') == -1 :
        error = "This is not valid email."
    
    return error
    

@app.route("/", methods = ['POST'])
def validate_uname():
    
    # verify user name
    user_name = request.form['uname']
    user_error = verify_field(user_name, "User name")

    # verify password
    password = request.form['pwd']
    password_error = verify_field(password, "Password")

    # confirm password
    verify_password = request.form['confirm-pwd']
    verify_pwd_error = confirm_pwd(password, verify_password)

    # verify email
    user_email = request.form['email']
    if user_email:
        user_email_error = verify_email(user_email)
    else:
        user_email_error = ""

    if user_error or password_error or verify_pwd_error:
        return render_template("sign-up.html", uname=user_name, name_error = user_error, 
        pwd_error = password_error, conf_pwd_error = verify_pwd_error,
        email = user_email, email_error = user_email_error)

    return redirect("/welcome?username={0}".format(user_name))
      

@app.route("/welcome")
def welcome_user():
    user_name= request.args.get("username")
    return render_template("welcome.html", title = "Welcome", username = user_name)

app.run()