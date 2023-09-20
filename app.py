from flask import Flask, render_template, request, redirect , url_for, flash, session
import appDataBase
import re
import os
import hash
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)
connection = appDataBase.connectDB()
app.secret_key="dskjbfdbgesoglkjdsd3493hrpeffe;l"
limiter = Limiter(app=app, key_func=get_remote_address, default_limits=["50 per minute"])


@app.route("/")
def index():
    if 'username' in session :
        if session['username']== 'Admin':
            users = appDataBase.Admin_getAllUsers(connection)
            return render_template("adminscreen.html" , users = users)
    return render_template("index.html")

@app.route("/gadgetid/<string:id>" , methods=['POST',"GET"] )
def gadgetid(id):

    if 'username' in session:
        if request.method == 'POST':
            text = request.form['commentText']
            appDataBase.addComment(connection, session['userId'] , id , text)
            return redirect(url_for('gadgetid' , id=id))
        gadget = appDataBase.getSGadget(connection, id)
        comments = appDataBase.getcomment(connection,id)
        return render_template('Sgadget.html' , gadget=gadget ,comments=comments)

    return "Login to access this page"

@app.route("/delete_user/<string:id>" , methods=['POST',"GET"])
def delete_user(id):
    if 'username' in session and session['username'] == 'Admin':
       
        appDataBase.deleteUser(connection, id)
        flash("user is deleted.." , "success")
        return redirect(url_for("index"))
    else:
        return "You are not authorized to access this page."


@app.route("/register" , methods=['POST' , 'GET'])
@limiter.limit("10 per minute")
def register():
    errorMessage = ''
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        ChechUser = appDataBase.getUser_username(connection , username)

        if(ChechUser):
            errorMessage = "User Already Exists"
        else:
            lengthbool = False
            symbolBool = False
            upperBool = False
            
            # password length check
            if len(password) >= 8:
                lengthbool = True
            
            # password symbol check
            if re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
                symbolBool = True    
            
            # password uppercase check
            if any(char.isupper() for char in password):
                upperBool = True

            if lengthbool and symbolBool and upperBool:   
                appDataBase.AddUser(connection,email,username, password)
                return redirect(url_for('login'))
            else:
                errorMessage ='Password must be more than 8 characters and at least one symbol and one Uppercase letter' 

    return render_template("register.html" , exists_message=errorMessage)


@app.route("/login" , methods=['POST' , 'GET'])
@limiter.limit("10 per minute")
def login():
    errorMessage=''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = appDataBase.getUser(connection, username)
        if(user):
            if hash.is_password_match(password, user[3]):
                session['username']=user[1]
                session['userId']=user[0]
                if session['username'] == 'Admin':
                    return redirect(url_for("index"))
                return redirect(url_for("homePage"))
        else:
            return render_template("login.html", errorMessage="Please Check Your UserName and Your Password")
    return render_template("login.html", errorMessage=errorMessage )


@app.route("/logout")
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))


@app.route('/homepage')
def homePage():
    if 'username' in session:
        return render_template('homePage.html', name = session['username'])



@app.route('/gadgets', methods=['POST', 'GET'])
def gadgets():
    validExt = ["jpeg", "jpg", "png", "gif"]
    if 'username' in session:
        if request.method == 'POST':
            name = request.form['name']
            description = request.form['description']
            price = request.form['price']
            gadgetImage = request.files['image']
            imageUrl = f"static/uploads/{gadgetImage.filename}"
            filename = gadgetImage.filename

            extension = filename.rsplit('.',1)[1].lower() 
            file_size = request.content_length
            if file_size > 100 * 1024 * 1024:
                flash('Please Enter Valid Image')
                return redirect(url_for("gadgets"))
            if not extension in validExt:
                flash('Please Enter Valid Image')
                return redirect(url_for('gadgets')) 
            gadgetImage.save(imageUrl)
            userid= session['userId']
            appDataBase.addGadget(connection , userid , name , description, price , imageUrl)
            return redirect(url_for('gadgets'))
        usergadgets = appDataBase.getUserGadgets(connection, session['userId'])
        print(gadgets)
        return render_template('Gadgets.html' , Gadgets=usergadgets)
    else:
        return "Login To Access This Page"

@app.route('/allGadgets', methods=['POST', 'GET'])
def allgadgets():
    if 'username' in session:
        allgadgets = appDataBase.getAllGadgets(connection)
        return render_template('allgadgets.html' , Gadgets=allgadgets)
    return "login to enter this page."




if __name__ == "__main__":
    appDataBase.DbInit(connection)
    appDataBase.gadgetDbInit(connection)
    appDataBase.CommentDB(connection)
    app.run(debug=True)

