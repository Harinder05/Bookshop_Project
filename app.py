import sqlite3 
import os
from flask import Flask, render_template, redirect, request, session, abort, url_for 

app = Flask(__name__)
app.secret_key = "secret key"
user_is_admin=False;



@app.route('/')                                                 
def homepage():
     try:
        con = sqlite3.connect('bookshop.db')                    #Connect to the database
        cur = con.cursor();                                     #Create cursor object
        cur.execute("SELECT * FROM books WHERE quantity!= 0 ")  #Select all data from the row if the value in column quantity is not 0#
        rows = cur.fetchall()                                   #Store data as variable rows
        return render_template('index.html', books=rows)        #Render the page and pass the data to template
     except Exception as e:                                     #If there is exception error print it
        print(e)
     finally:
        cur.close()                                             #Close the cursor object
        con.close()                                             #Close the conenction with database


# Some of code is adapted from this https://stackoverflow.com/questions/16469366/flask-login-not-sure-how-to-make-it-work-using-sqlite3         
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":                                                                        #If the request method is POST
        u=request.form['name']                                                                          #Store value from the form as u
        p=request.form['pass']                                                                          #Store value from the form as p
        con = sqlite3.connect('bookshop.db')                                                            #Connect to database
        cur = con.cursor();                                                                             #Create cursor object
        cur.execute("SELECT username FROM customer_login WHERE username = ? AND Password=?;", (u, p))   #Select the username row from table cusutomer_login if the value in column username is same as varaible u and value p in column password
        x = cur.fetchone()                                                                              #The data from query is stored in varaible x
        if x is not None:                                                                               #If the value of x is not None meaning there is this username in the database
            name= request.form.get("name")                                                              #Get the name from the for and store it inside varaible name
            session["name"] = name                                                                      #Set session name to name
                        
            if name == 'admin':                                                                         #If the name is admin
                global user_is_admin                                                                    
                user_is_admin = True;                                                                   #Set global variable to True
            return redirect(url_for('homepage'))                                                        #Redirect to homepage
        else:
            msg="Username not registered. Please sign up."                                              #Set msg to message inside string
            return render_template('login.html',msg=msg)                                                #Render the login page and pass the variable msg
    else:
        return render_template('login.html')                                                            #Render the login page
    

@app.route('/logout')                                           
def logout():
    session["name"]=None                                        #Set session name to None
    global user_is_admin                                        
    if user_is_admin == True:                                   #If the global vaiarble is True
        user_is_admin= False;                                   #Set it to False
    return redirect('/')                                        #Redirect the user to homepage


@app.route('/register', methods=['GET','POST'])
def register():
    if  request.method == "POST":                                                                       #If the request method is POST
        user=request.form['user']                                                                       #Store value from the form as user
        passw=request.form['passw']                                                                     #Store value from the form as passw
        con = sqlite3.connect('bookshop.db')                                                            #Connect to database
        cur = con.cursor();                                                                             #Create cursor object
        cur.execute("SELECT * FROM customer_login WHERE username=?",(user,))                            #Select all rows from table cusutomer_login where the value in column username is same as varaible user
        data= cur.fetchone()                                                                            #The data from query is stored in varaible data
        if data is not None:                                                                            #If the value of data is not None meaning there is this username in the database
            msg="Username already used"                                                                 #Set msg to string username already used
            cur.close()                                                                                 #Close the cursor
            con.close()                                                                                 #Close the connection
            return render_template('register.html', msg=msg)                                            #Render the template for register and pass the varaible msg
        else:                                                                                           #Else if data is none meaning there is no username as variable user
            cur.execute("INSERT INTO customer_login(username,password) VALUES (?,?);",(user,passw))     #Insert the data in variable user and passw into column username and password
            con.commit()                                                                                #Commit the change to database 
            cur.close()                                                                                 #Close cursor object
            con.close()                                                                                 #Close connection
            msg="User registration successful.Please use log in."                                       #Set variable msg to successful registration
            return render_template('register.html', msg=msg)                                            #Render the template for register.html and pass the variable msg
    else:
        return render_template ('register.html')                                                        #Render the template for register.html 


@app.route('/stock_level', methods=["GET","POST"])
def stock_level():
    global user_is_admin
    if user_is_admin == False:                                                          #If varaible is false
        return render_template('unauthorized.html')                                     #Render the unauthorized template
    else:        
        con = sqlite3.connect('bookshop.db')                                            #Connect to the database
        cur = con.cursor();                                                             #Create cursor object
        cur.execute("SELECT book_name,isbn,front_cover,quantity FROM books ")           #Select the data from column book_name,isbn,front_cover, quantity from table books
        rows = cur.fetchall()                                                           #Store data from database in varaible rows
        return render_template('stock_level.html',rows=rows)                            #Render the stock_level template and pass rows variable
      


        
# Code reference for image upload: "https://www.youtube.com/watch?v=6WruncSoCdI&list=PLF2JzgCW6-YY_TZCmBrbOpgx5pSNBD0_L&index=15&ab_channel=JulianNash" and "https://blog.miguelgrinberg.com/post/handling-file-uploads-with-flask"

app.config['IMAGE_UPLOADS'] = "/home/codio/workspace/bookshop/static/book-images"       #Set image_upload in app configuration to the absolute path of book-images folder


@app.route('/add_book', methods=['GET', 'POST'])                                        
def add_book():
    global user_is_admin                                                                
    if user_is_admin == False:                                                          
        return render_template('unauthorized.html')                                     
    elif    request.method == "POST":                                                   #If request method is POST
            book=request.form['bookname']                                               #Get input from the form and store inside a variable book
            author=request.form['author']                                               #Get input from the form and store inside a variable author
            isbn=request.form['isbn']                                                   #Get input from the form and store inside a variable isbn
            desc=request.form['desc']                                                   #Get input from the form and store inside a variable desc
            tp=request.form['tp']                                                       #Get input from the form and store inside a variable tp
            rp=request.form['rp']                                                       #Get input from the form and store inside a variable rp
            quantity=request.form['quantity']                                           #Get input from the form and store inside a variable quantity
            date=request.form['date']                                                   #Get input from the form and store inside a variable date

            image=request.files['pic']                                                  #Get input from the form and store inside a variable pic
            image.save(os.path.join(app.config['IMAGE_UPLOADS'],image.filename))        #Save the image in the book-images folder
            image_name=image.filename                                                   #Set variable to name of the image from the form

            con = sqlite3.connect('bookshop.db')                                        #Connect to database
            cur = con.cursor();                                                         #Create cursor object
            cur.execute("INSERT INTO books(book_name,author_name,isbn,book_description,front_cover,trade_price,retail_price,publication_date,quantity) VALUES (?,?,?,?,?,?,?,?,?);",(book,author,isbn,desc,image_name,tp,rp,date,quantity))  #Insert the data in variables into the correct column in database
            con.commit()                                                                #Commit changes to database

            return redirect(url_for('stock_level'))
    else:
        return render_template('/add_book_form.html')


#REFERENCES:
#Flask application - https://www.youtube.com/watch?v=x_c8pTW8ZUc&ab_channel=CS50
# Form data/HTTP requests - https://www.youtube.com/watch?v=9MHYHgh4jYc&list=PLzMcBGfZo4-n4vJJybUVV3Un_NFS5EOgX&index=4&ab_channel=TechWithTim
