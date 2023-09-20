import sqlite3
import hashlib
import bcrypt



def connectDB(name="app.db"):
    return sqlite3.connect(name, check_same_thread=False)



def DbInit(conn):
    cursor = conn.cursor()

    cursor.execute('''  CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,    
            Email TEXT NOT NULL UNIQUE ,
            password TEXT NOT NULL    
            )
        '''
    )
    conn.commit()


def gadgetDbInit(conn):
    cursor = conn.cursor()
    cursor.execute(
        ''' CREATE TABLE IF NOT EXISTS gadgets(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        description TEXT NOT NULL,
        price TEXT NOT NULL,
        imageurl TEXT NOT NULL,
        userid INTEGER NOT NULL,
        FOREIGN KEY (userid) REFERENCES users (id)
        )   
    '''
    )
    conn.commit()

def addGadget(conn , userid , name , description, price , imageurl):    
    cursor = conn.cursor()
    query = "INSERT INTO gadgets (userid,name,description,price,imageurl) VALUES(?,?,?,?,?) "    
    cursor.execute(query,(userid,name,description,price,imageurl))
    conn.commit()


def getUserGadgets(conn, userid):
    cursor=conn.cursor()
    query = "SELECT * FROM gadgets WHERE userid=?"
    cursor.execute(query,(userid,))
    return cursor.fetchall()

def getAllGadgets(conn):
    cursor= conn.cursor()
    query = "SELECT * FROM gadgets"
    cursor.execute(query)
    return cursor.fetchall()

def getSGadget(conn, GadgetId):
    cursor = conn.cursor()
    query = '''SELECT * FROM gadgets WHERE id =?'''
    cursor.execute(query, (GadgetId,))
    return cursor.fetchone()



def AddUser(conn , email , username , password):
    cursor = conn.cursor()
    # pas = hashlib.md5(password.encode())
    # hashedPassword= pas.hexdigest()
    hashedPassword = bcrypt.hashpw(password.encode() , bcrypt.gensalt())
    hashedPassword=hashedPassword.decode()
    query = f''' INSERT INTO users (username , Email , password)  VALUES (?,?,? ) '''
    cursor.execute(query,(username,email,hashedPassword))
    conn.commit()


def getUser_username(conn, username):
    cursor = conn.cursor()
    query = f"SELECT * FROM users WHERE username = ? "
    cursor.execute(query,(username,))
    return cursor.fetchone()


def getUser(conn , username):
    cursor= conn.cursor()
    query=f''' SELECT * FROM users WHERE username=?'''
    cursor.execute(query,(username,))
    return cursor.fetchone()



def Admin_getAllUsers(conn):
    cursor = conn.cursor()
    query = ''' SELECT * FROM users '''
    cursor.execute(query)
    return cursor.fetchall()



def deleteUser(conn , id):
    cursor = conn.cursor()
    query = "DELETE FROM users WHERE id=? "
    cursor.execute(query, (id,))
    conn.commit()



def CommentDB(conn):
    cursor=conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS comments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            gadget_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            text TEXT NOT NULL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (gadget_id) REFERENCES gadgets (id),
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    conn.commit()

def addComment(conn , userid, gadgetid , text):
    cursor = conn.cursor()
    query='''INSERT INTO comments (user_id,gadget_id,text) VALUES (?,?,?) '''
    cursor.execute(query,(userid,gadgetid,text))
    conn.commit()


def getcomment(conn , gadgetid):
    cursor=conn.cursor()
    query = '''  SELECT  users.username, comments.text, comments.timestamp
        FROM comments
        JOIN users ON comments.user_id = users.id
        WHERE comments.gadget_id = ?'''
    cursor.execute(query,(gadgetid,))
    return cursor.fetchall()

