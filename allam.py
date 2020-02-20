from tkinter import *
from PIL import ImageTk, Image
import pymysql as MySQLdb
from tkinter import messagebox
from tkinter import filedialog as fd
from tkinter import ttk
import csv
import pyautogui
import pyttsx3
import smtplib
from email.message import EmailMessage
def forgetpassword(email):
    c=get_password(email)
    contacts = ['YourAddress@gmail.com', 'test@example.com']
    msg = EmailMessage()
    msg['Subject'] = 'Check out Bronx as a puppy!'
    msg['From'] = 'allamco4@gmail.com'
    msg['To'] = email
    msg.set_content('confirm your pass')
    msg.add_alternative("your password for university account  is {}".format(c))
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login('allamco4@gmail.com', '00000000001')
        smtp.send_message(msg)

def get_password(emaill):

        db = MySQLdb.connect("localhost", "root", "", "bio")
        # prepare a cursor object using cursor() method
        cursor = db.cursor()
        sql = "select password from users where email='%s'"%(emaill)
        try:
            # Execute the SQL command
            cursor.execute(sql)
            # Fetch all the rows in a list of lists.
            cc = []
            results = list(cursor.fetchall())
            for i in results:
                for j in i:
                    cc.append(j)
        except:
            print("error")
        db.close()
        return cc[0]

def Academic_grade(s1,s2,s3,s4,s5,s6):
    s=int(s1)+int(s2)+int(s3)+int(s4)+int(s5)+int(s6)
    x=(s/600)*100
    if x >=90 :
        return 'Excellent high'
    elif  x>=85 :
        return 'Excellent'
    elif  x>=80 :
        return 'very good high'
    elif  x>=75 :
        return 'very good'
    elif  x>=70 :
        return 'good high'
    elif  x>=65 :
        return 'good'
    elif  x>=60 :
        return 'weak'
    elif  x>=50 :
        return 'very weak'
    else :
        return 'failed'

def say_sound(name,grade):
    engine = pyttsx3.init()
    engine.setProperty('rate', 110)  # Speed percent (can go over 100)
    engine.setProperty('volume', 0.9)  # Volume 0-1
    engine.say("Academic grade ya {} in this term is {}".format(name,grade))
    engine.runAndWait()
def error_say(v):
    engine = pyttsx3.init()
    engine.setProperty('rate', 110)  # Speed percent (can go over 100)
    engine.setProperty('volume', 0.9)  # Volume 0-1
    engine.say(v)
    engine.runAndWait()

class FullScreenApp(object):
    def __init__(self, master, **kwargs):
        self.master=master
        pad=3
        self._geom='200x200+0+0'
        master.geometry("{0}x{1}+0+0".format(
            master.winfo_screenwidth()-pad, master.winfo_screenheight()-pad))
        master.bind('<Escape>',self.toggle_geom)
    def toggle_geom(self,event):
        geom=self.master.winfo_geometry()
        print(geom,self._geom)
        self.master.geometry(self._geom)
        self._geom=geom
def insert_sucess_hours(hours,name):
    db = MySQLdb.connect("localhost", "root", "", "bio")
    cursor = db.cursor()
    sql = "update term set  hours = %d where name='%s'" % (hours,name)
    try:
        cursor.execute(sql)
        db.commit()
        print("update")
    except:
        messagebox.showerror("error", "error")
        db.rollback()
    db.close()
def UP(sub,degree,name):
    db = MySQLdb.connect("localhost", "root", "", "bio")
    cursor = db.cursor()
    if sub=='sub1':sql = "update term set sub1 = %d where name='%s'" % (int(degree),name)
    if sub=='sub2':sql = "update term set sub2 = %d where name='%s'" % (int(degree),name)
    if sub=='sub3':sql = "update term set sub3 = %d where name='%s'" % (int(degree),name)
    if sub=='sub4':sql = "update term set sub4 = %d where name='%s'" % (int(degree),name)
    if sub=='sub5':sql = "update term set sub5 = %d where name='%s'" % (int(degree),name)
    if sub=='sub6':sql = "update term set sub6 = %d where name='%s'" % (int(degree),name)
    try:
        cursor.execute(sql)
        db.commit()
        print("update")
    except:
        print("error", "error")
        db.rollback()
    db.close()
def u_sucess(name,subject , degree):
    if int(degree) >= 50 :
       a=find_old_hours(name)+3
       update_show(name, find_old_hours(name), subject , degree)
       insert_sucess_hours(a, name)
       db = MySQLdb.connect("localhost", "root", "", "bio")
       # prepare a cursor object using cursor() method
       cursor = db.cursor()
       sql = "DELETE  FROM failed  WHERE name='%s'AND subject = '%s' "%(name,subject)
       try:
           # Execute the SQL command
           cursor.execute(sql)
           # Commit your changes in the database
           db.commit()
       except:
           messagebox.showerror('error', 'you have error')
           # Rollback in case there is any error
           db.rollback()
       db.close()
def failed_students_name():
    db = MySQLdb.connect("localhost", "root", "", "bio")
    # prepare a cursor object using cursor() method
    cursor = db.cursor()
    sql = "SELECT DISTINCT name FROM failed  "
    try:
        # Execute the SQL command
        cursor.execute(sql)
        # Fetch all the rows in a list of lists.
        cc = []
        results = list(cursor.fetchall())
        for i in results:
            for j in i:
                cc.append(j)
    except:
        print("error")
    db.close()
    return cc
def failed_students_subject(name):
    db = MySQLdb.connect("localhost", "root", "", "bio")
    # prepare a cursor object using cursor() method
    cursor = db.cursor()
    sql = "SELECT  subject FROM failed where name = '%s' "%(name)
    try:
        # Execute the SQL command
        cursor.execute(sql)
        # Fetch all the rows in a list of lists.
        cc = []
        results = list(cursor.fetchall())
        for i in results:
            for j in i:
                cc.append(j)
    except:
        print("error")
    db.close()
    return cc
def insert_new_records(name):
        db = MySQLdb.connect("localhost", "root", "", "bio")
        cursor = db.cursor()
        sql = "insert into term (name , hours) values ('%s',0)" % (name)
        try:
            cursor.execute(sql)
            db.commit()
            print("insert")
        except:
            messagebox.showerror("error", "error")
            db.rollback()
        db.close()
def check_failed(name ,title,sub):
    if int(sub)<50:
        db = MySQLdb.connect("localhost", "root", "", "bio")
        cursor = db.cursor()
        sql = "insert into failed values ('%s','%s',%d)" % (name , title,sub)
        try:
            cursor.execute(sql)
            db.commit()
            print("insert")
        except:
            messagebox.showerror("error", "error")
            db.rollback()
        db.close()
def hour_after_update(a,b):
    z=0
    for i in a :
        if int(i) <50 :
         c=a.index(i)
         if int(b[c])>=50 :
             z+=3
    return z
def update_show(name,hours , subgect , degree):
    if hours >=0 and hours <=15 :
        terms = "first"
    elif hours >=16 and hours <=30 :
        terms = "second"
    elif hours >=31 and hours <=48 :
        terms = "third"
    elif hours >=49 and hours <=66 :
        terms = "fourth"
    elif hours >=67 and hours <=85 :
        terms = "fifth"
    if terms == "first":
        l = ["math0", "electric circuit", "scientific report", "introduction", "chemistry1", "requirements"]
    if terms == "second":
        l = ["chemistry2", "biology1", "IS", "programming", "math1", "creative thing"]
    if terms == "third":
        l = ["logic", "statics1", "programming 2", "math2", "desctete", "biology2"]
    if terms == "fourth":
        l = ["biochemistry", "biology", "os", "math3", "data structure", "statics2"]
    if terms == "fifth":
        l = ["genetics", "graphics", "databases", "algorithms", "Bio computing", "machine learning"]
    if subgect in l:
        a = l.index(subgect)
        if a == 0:
            ssub = "sub1"
        if a == 1:
            ssub = "sub2"
        if a == 2:
            ssub = "sub3"
        if a == 3:
            ssub = "sub4"
        if a == 4:
            ssub = "sub5"
        if a == 5:
            ssub = "sub6"
        UP(ssub,degree,name )
def find_names(terms):
    db = MySQLdb.connect("localhost", "root", "", "bio")
    # prepare a cursor object using cursor() method
    cursor = db.cursor()
    if terms=="first":
        sql = "SELECT name FROM term WHERE hours BETWEEN 0 AND 15 "
    elif terms=="second":
        sql = "SELECT name FROM term WHERE hours BETWEEN 16 AND 30 "
    elif terms=="third":
        sql = "SELECT name FROM term WHERE hours BETWEEN 31 AND 48 "
    elif terms=="fourth":
        sql = "SELECT name FROM term WHERE hours BETWEEN 49 AND 66 "
    elif terms=="fifth":
        sql = "SELECT name FROM term WHERE hours BETWEEN 67 AND 85 "
    else:
        sql = "SELECT name FROM term WHERE hours BETWEEN 0 AND 85 "
    try:
        # Execute the SQL command
        cursor.execute(sql)
        # Fetch all the rows in a list of lists.
        cc=[]
        results = list(cursor.fetchall())
        for i in results :
            for j in i :
               cc.append(j)
    except :
        print("error")
    db.close()
    return cc
def find_old_degree(name):
    db = MySQLdb.connect("localhost", "root", "", "bio")
    # prepare a cursor object using cursor() method
    cursor = db.cursor()
    sql = "SELECT sub1,sub2,sub3,sub4,sub5,sub6 FROM term WHERE name='%s' "%(name)
    try:
        # Execute the SQL command
        cursor.execute(sql)
        # Fetch all the rows in a list of lists.
        cc=[]
        results = list(cursor.fetchall())
        for i in results :
            for j in i :
               cc.append(j)
    except :
        print("error")
    db.close()
    return cc
def find_old_hours(name):
    db = MySQLdb.connect("localhost", "root", "", "bio")
    # prepare a cursor object using cursor() method
    cursor = db.cursor()
    sql = "SELECT hours FROM term WHERE name='%s' "%(name)
    try:
        # Execute the SQL command
        cursor.execute(sql)
        # Fetch all the rows in a list of lists.
        cc=[]
        results = list(cursor.fetchall())
        for i in results :
            for j in i :
               cc.append(j)
    except :
        print("error")
    db.close()
    return cc[0]
def load_data(filename):
  with open(filename, 'r') as file:
      reader = list(csv.reader(file))
      del reader[0]
  return reader
def calc_hours(sub1, sub2, sub3, sub4, sub5, sub6):
    c=0
    l=[sub1, sub2, sub3, sub4, sub5, sub6]
    for i in l :
        if int(i) >=50:
            c +=3
    return c
def insert (name , sub1, sub2, sub3, sub4, sub5, sub6) :

   db = MySQLdb.connect("localhost","root","","bio")
   cursor = db.cursor()
   sql = "UPDATE term SET sub1='%s',sub2='%s',sub3='%s',sub4='%s',sub5='%s',sub6='%s',hours=%d WHERE name = '%s'" % (sub1, sub2, sub3, sub4, sub5, sub6,find_old_hours(name)+calc_hours(sub1, sub2, sub3, sub4, sub5, sub6),name )
   try:
      cursor.execute(sql)
      db.commit()
      messagebox.showinfo("dr ahmed : ","you insert {}  degrees".format(name))
   except:
      messagebox.showerror("error","error")
      db.rollback()
   db.close()
def update (name , sub1, sub2, sub3, sub4, sub5, sub6) :
   db = MySQLdb.connect("localhost","root","","bio")
   cursor = db.cursor()
   a = find_old_degree(name)
   b = [sub1, sub2, sub3, sub4, sub5, sub6]
   c = hour_after_update(a, b)
   d=find_old_hours(name)+c
   sql = "UPDATE term SET sub1='%s',sub2='%s',sub3='%s',sub4='%s',sub5='%s',sub6='%s',hours=%d WHERE name = '%s'" % (sub1, sub2, sub3, sub4, sub5, sub6,d,name )
   try:
      cursor.execute(sql)
      db.commit()
      error_say("update sucess")
      print("update")
   except:
      error_say("error")
      db.rollback()
   db.close()
def wel_name(email,password):
    db = MySQLdb.connect("localhost", "root", "", "bio")
    # prepare a cursor object using cursor() method
    cursor = db.cursor()
    sql = "SELECT name FROM users WHERE email='%s' AND password='%s' "%(email,password)
    try:
        # Execute the SQL command
        cursor.execute(sql)
        # Fetch all the rows in a list of lists.
        cc=[]
        results = list(cursor.fetchall())
        for i in results :
            for j in i :
               cc.append(j)
    except :
        print("error")
    db.close()
    return cc[0]
def users_insert(email,password,name):
    db = MySQLdb.connect("localhost", "root", "", "bio")
    cursor = db.cursor()
    sql = "insert into users (email,password,name ) values ('%s','%s','%s')" % (email,password,name)
    try:
        cursor.execute(sql)
        db.commit()
        print("insert")
    except:
        messagebox.showerror("error", "error")
        db.rollback()
    db.close()
def myapp():
    form = Tk()
    app = FullScreenApp(form)
    form.iconbitmap("BIO.ico")
    form.title("login page")
    form.config(bg="light blue")
    frame1 = Frame(form)
    frame1.config(bg="light blue")
    Label(frame1, text="email", font=(24), fg="dark blue", bg="gray").grid(row=1, column=0, padx=20, pady=20)
    Label(frame1, text="password", font=(24), fg="dark blue", bg="gray").grid(row=2, column=0, padx=20, pady=20)
    email = Entry(frame1, font=24, bd=5, bg="light blue", width=20)
    password = Entry(frame1, font=24, bd=5, bg="light blue", width=20, show="*")
    email.grid(row=1, column=1, padx=20, pady=20)
    password.grid(row=2, column=1, padx=20, pady=20)
    v=IntVar()
    Checkbutton(frame1,text='forget password ??',variable=v,bg="light blue").grid(row=3, column=1,padx=5)
    frame1.grid(row=0, column=0)

    def login():
        n = email.get()
        p = password.get()

        def w():
            form.destroy()

        def welcome_page():
            welcome = Tk()
            app = FullScreenApp(welcome)
            welcome.title(wel_name(n, p))
            welcome.iconbitmap('BIO.ico')
            welcome.config(bg='light blue')
            frame3 = Frame(welcome)
            frame4 = Frame(welcome)
            frame3.config(bg="light blue")
            frame4.config(bg="light blue")
            frame6 = Frame(frame3)
            frame6.config(bg="light blue")
            Label(frame6, text="choice the term", font=(12), fg="dark blue", bg="light blue").grid(row=0, column=0,
                                                                                                   padx=6,
                                                                                                   pady=6)
            long = ttk.Combobox(frame6, values=("first", "second", "third", "fourth", "fifth"), font=(12))
            long.grid(row=0, column=1)
            frame6.grid(row=0, column=0, padx=20, pady=20)

            def load_csv_file():
                x = long.get()
                if x == "":
                    error_say("my dear you forget choose the term")
                else:
                    if x == "first":
                        ssub1, ssub2, ssub3, ssub4, ssub5, ssub6 = "math0", "electric circuit", "scientific report", "introduction", "chemistry1", "requirements"
                    if x == "second":
                        ssub1, ssub2, ssub3, ssub4, ssub5, ssub6 = "chemistry2", "biology1", "IS", "programming", "math1", "creative thing"
                    if x == "third":
                        ssub1, ssub2, ssub3, ssub4, ssub5, ssub6 = "logic", "statics1", "programming 2", "math2", "desctete", "biology2"
                    if x == "fourth":
                        ssub1, ssub2, ssub3, ssub4, ssub5, ssub6 = "biochemistry", "biology", "os", "math3", "data structure", "statics2"
                    if x == "fifth":
                        ssub1, ssub2, ssub3, ssub4, ssub5, ssub6 = "genetics", "graphics", "databases", "algorithms", "Bio computing", "machine learning"
                    filenamee = fd.askopenfilename()
                    print(filenamee)
                    c = load_data(filenamee)
                    for i in c:
                        check_failed(str(i[0], ssub1, int(i[1])))
                        check_failed(str(i[0], ssub2, int(i[2])))
                        check_failed(str(i[0], ssub3, int(i[3])))
                        check_failed(str(i[0], ssub4, int(i[4])))
                        check_failed(str(i[0], ssub5, int(i[5])))
                        check_failed(str(i[0], ssub6, int(i[6])))
                        insert(str(i[0]), str(i[1]), str(i[2]), str(i[3]), str(i[4]), str(i[5]), str(i[6]))
                    error_say("you insert {} stedents".format(len(c)))

            def insert_one_student():
                x = long.get()
                if x == "":
                    error_say("my dear you forget choose the term")
                else:
                    if x == "first":
                        ssub1, ssub2, ssub3, ssub4, ssub5, ssub6 = "math0", "electric circuit", "scientific report", "introduction", "chemistry1", "requirements"
                    if x == "second":
                        ssub1, ssub2, ssub3, ssub4, ssub5, ssub6 = "chemistry2", "biology1", "IS", "programming", "math1", "creative thing"
                    if x == "third":
                        ssub1, ssub2, ssub3, ssub4, ssub5, ssub6 = "logic", "statics1", "programming 2", "math2", "desctete", "biology2"
                    if x == "fourth":
                        ssub1, ssub2, ssub3, ssub4, ssub5, ssub6 = "biochemistry", "biology", "os", "math3", "data structure", "statics2"
                    if x == "fifth":
                        ssub1, ssub2, ssub3, ssub4, ssub5, ssub6 = "genetics", "graphics", "databases", "algorithms", "Bio computing", "machine learning"
                    frame3.destroy()
                    frame5 = Frame(welcome)
                    frame5.config(bg='light blue')
                    frame7 = Frame(frame5)
                    frame7.config(bg="light blue")
                    Label(frame7, text="select student", font=(12), fg="dark blue", bg="light blue").grid(row=0,
                                                                                                          column=0,
                                                                                                          padx=6,
                                                                                                          pady=6)
                    longg = ttk.Combobox(frame7, values=find_names(x), font=(12))
                    longg.grid(row=0, column=1)
                    frame7.grid(row=0, column=0, padx=5, pady=5)
                    Label(frame5, text=ssub1, font=(24), fg="dark blue", bg="gray").grid(row=1, column=0, padx=5,
                                                                                         pady=5)
                    Label(frame5, text=ssub2, font=(24), fg="dark blue", bg="gray").grid(row=2, column=0, padx=5,
                                                                                         pady=5)
                    Label(frame5, text=ssub3, font=(24), fg="dark blue", bg="gray").grid(row=3, column=0, padx=5,
                                                                                         pady=5)
                    Label(frame5, text=ssub4, font=(24), fg="dark blue", bg="gray").grid(row=4, column=0, padx=5,
                                                                                         pady=5)
                    Label(frame5, text=ssub5, font=(24), fg="dark blue", bg="gray").grid(row=5, column=0, padx=5,
                                                                                         pady=5)
                    Label(frame5, text=ssub6, font=(24), fg="dark blue", bg="gray").grid(row=6, column=0, padx=5,
                                                                                         pady=5)
                    sub1 = Entry(frame5, font=18, bd=5, bg="light blue", width=5)
                    sub2 = Entry(frame5, font=18, bd=5, bg="light blue", width=5)
                    sub3 = Entry(frame5, font=18, bd=5, bg="light blue", width=5)
                    sub4 = Entry(frame5, font=18, bd=5, bg="light blue", width=5)
                    sub5 = Entry(frame5, font=18, bd=5, bg="light blue", width=5)
                    sub6 = Entry(frame5, font=18, bd=5, bg="light blue", width=5)
                    sub1.grid(row=1, column=1, padx=5, pady=5)
                    sub2.grid(row=2, column=1, padx=5, pady=5)
                    sub3.grid(row=3, column=1, padx=5, pady=5)
                    sub4.grid(row=4, column=1, padx=5, pady=5)
                    sub5.grid(row=5, column=1, padx=5, pady=5)
                    sub6.grid(row=6, column=1, padx=5, pady=5)

                    def go_back():
                        welcome.destroy()
                        welcome_page()

                    def ins():
                        check_failed(longg.get(), ssub1, int(sub1.get()))
                        check_failed(longg.get(), ssub2, int(sub2.get()))
                        check_failed(longg.get(), ssub3, int(sub3.get()))
                        check_failed(longg.get(), ssub4, int(sub4.get()))
                        check_failed(longg.get(), ssub5, int(sub5.get()))
                        check_failed(longg.get(), ssub6, int(sub6.get()))
                        insert(longg.get(), sub1.get(), sub2.get(), sub3.get(), sub4.get(), sub5.get(), sub6.get())

                    Button(frame5, font=20, text="insert ", bd=8, bg="dark blue", fg="white",
                           activebackground='Gray', activeforeground='light blue', width=20, command=ins).grid(row=7,
                                                                                                               column=0,
                                                                                                               padx=20,
                                                                                                               pady=20)
                    Button(frame5, font=20, text="back", bd=8, bg="dark blue", fg="white",
                           activebackground='Gray', activeforeground='light blue', width=20, command=go_back).grid(
                        row=7,
                        column=1,
                        padx=20,
                        pady=20)

                    frame5.grid(row=0, column=0, padx=20, pady=20)

            def UPDATE():
                x = long.get()
                if x == "":
                    error_say("my dear you forget choose the term")
                else:
                    if x == "first":
                        ssub1, ssub2, ssub3, ssub4, ssub5, ssub6 = "math0", "electric circuit", "scientific report", "introduction", "chemistry1", "requirements"
                    if x == "second":
                        ssub1, ssub2, ssub3, ssub4, ssub5, ssub6 = "chemistry2", "biology1", "IS", "programming", "math1", "creative thing"
                    if x == "third":
                        ssub1, ssub2, ssub3, ssub4, ssub5, ssub6 = "logic", "statics1", "programming 2", "math2", "desctete", "biology2"
                    if x == "fourth":
                        ssub1, ssub2, ssub3, ssub4, ssub5, ssub6 = "biochemistry", "biology", "os", "math3", "data structure", "statics2"
                    if x == "fifth":
                        ssub1, ssub2, ssub3, ssub4, ssub5, ssub6 = "genetics", "graphics", "databases", "algorithms", "Bio computing", "machine learning"
                    frame3.destroy()
                    frame5 = Frame(welcome)
                    frame5.grid(row=0, column=0, padx=20, pady=20)
                    frame5.config(bg='light blue')
                    frame7 = Frame(frame5)
                    frame7.config(bg="light blue")
                    Label(frame7, text="select student", font=(12), fg="dark blue", bg="light blue").grid(row=0,
                                                                                                          column=0,
                                                                                                          padx=6,
                                                                                                          pady=6)
                    longg = ttk.Combobox(frame7, values=find_names(x), font=(12))
                    longg.grid(row=0, column=1)

                    def info():
                        Bt.destroy()
                        s1, s2, s3, s4, s5, s6 = find_old_degree(longg.get())

                        Label(frame5, text=ssub1, font=(24), fg="dark blue", bg="gray").grid(row=1, column=0, padx=5,
                                                                                             pady=5)
                        Label(frame5, text=ssub2, font=(24), fg="dark blue", bg="gray").grid(row=2, column=0, padx=5,
                                                                                             pady=5)
                        Label(frame5, text=ssub3, font=(24), fg="dark blue", bg="gray").grid(row=3, column=0, padx=5,
                                                                                             pady=5)
                        Label(frame5, text=ssub4, font=(24), fg="dark blue", bg="gray").grid(row=4, column=0, padx=5,
                                                                                             pady=5)
                        Label(frame5, text=ssub5, font=(24), fg="dark blue", bg="gray").grid(row=5, column=0, padx=5,
                                                                                             pady=5)
                        Label(frame5, text=ssub6, font=(24), fg="dark blue", bg="gray").grid(row=6, column=0, padx=5,
                                                                                             pady=5)
                        sub1 = Entry(frame5, font=18, bd=5, bg="light blue", width=5)
                        sub2 = Entry(frame5, font=18, bd=5, bg="light blue", width=5)
                        sub3 = Entry(frame5, font=18, bd=5, bg="light blue", width=5)
                        sub4 = Entry(frame5, font=18, bd=5, bg="light blue", width=5)
                        sub5 = Entry(frame5, font=18, bd=5, bg="light blue", width=5)
                        sub6 = Entry(frame5, font=18, bd=5, bg="light blue", width=5)
                        sub1.insert(0, s1)
                        sub2.insert(0, s2)
                        sub3.insert(0, s3)
                        sub4.insert(0, s4)
                        sub5.insert(0, s5)
                        sub6.insert(0, s6)
                        sub1.grid(row=1, column=1, padx=5, pady=5)
                        sub2.grid(row=2, column=1, padx=5, pady=5)
                        sub3.grid(row=3, column=1, padx=5, pady=5)
                        sub4.grid(row=4, column=1, padx=5, pady=5)
                        sub5.grid(row=5, column=1, padx=5, pady=5)
                        sub6.grid(row=6, column=1, padx=5, pady=5)

                        def go_back():
                            welcome.destroy()
                            welcome_page()

                        def up_degree():
                            ss1, ss2, ss3, ss4, ss5, ss6 = sub1.get(), sub2.get(), sub3.get(), sub4.get(), sub5.get(), sub6.get()
                            a = [ss1, ss2, ss3, ss4, ss5, ss6]
                            b = [s1, s2, s3, s4, s5, s6]
                            c = [ssub1, ssub2, ssub3, ssub4, ssub5, ssub6]
                            for i in range(6):
                                if int(b[i]) < 50 and int(a[i]) >= 50:
                                    u_sucess(longg.get(), c[i], a[i])
                            update(longg.get(), ss1, ss2, ss3, ss4, ss5, ss6)

                        Button(frame5, font=20, text="update", bd=8, bg="dark blue", fg="white",
                               activebackground='Gray',
                               activeforeground='light blue', width=20,
                               command=up_degree).grid(row=7, column=0, padx=20, pady=20)
                        Button(frame5, font=20, text="go back", bd=8, bg="dark blue", fg="white",
                               activebackground='Gray',
                               activeforeground='light blue', width=20,
                               command=go_back).grid(row=7, column=1, padx=20, pady=20)

                    Bt = Button(frame5, font=20, text="show info", bd=8, bg="dark blue", fg="white",
                                activebackground='Gray',
                                activeforeground='light blue', width=20, command=info)
                    Bt.grid(row=1, column=0, columnspan=2, padx=20, pady=20)
                    frame7.grid(row=0, column=0, padx=5, pady=5)

            def SERCH():
                x = long.get()
                if x == "":
                    error_say("my dear you forget choose the term")
                else:
                    if x == "first":
                        sub1, sub2, sub3, sub4, sub5, sub6 = "math0", "electric circuit", "scientific report", "introduction", "chemistry1", "requirements"
                    if x == "second":
                        sub1, sub2, sub3, sub4, sub5, sub6 = "chemistry2", "biology1", "IS", "programming", "math1", "creative thing"
                    if x == "third":
                        sub1, sub2, sub3, sub4, sub5, sub6 = "logic", "statics1", "programming 2", "math2", "desctete", "biology2"
                    if x == "fourth":
                        sub1, sub2, sub3, sub4, sub5, sub6 = "biochemistry", "biology", "os", "math3", "data structure", "statics2"
                    if x == "fifth":
                        sub1, sub2, sub3, sub4, sub5, sub6 = "genetics", "graphics", "databases", "algorithms", "Bio computing", "machine learning"
                    frame3.destroy()
                    frame5 = Frame(welcome)
                    frame5.config(bg='light blue')
                    frame7 = Frame(frame5)
                    frame7.config(bg="light blue")
                    Label(frame7, text="select student", font=(12), fg="dark blue", bg="light blue").grid(row=0,
                                                                                                          column=0,
                                                                                                          padx=6,
                                                                                                          pady=6)
                    longg = ttk.Combobox(frame7, values=find_names(x), font=(12))
                    longg.grid(row=0, column=1)
                    frame7.grid(row=0, column=0, padx=5, pady=5)

                    def confirm_search():
                        s1, s2, s3, s4, s5, s6 = find_old_degree(longg.get())
                        h = find_old_hours(longg.get())
                        Label(frame5, text=sub1, font=(24), fg="dark blue", bg="gray").grid(row=2, column=0, padx=5,
                                                                                            pady=5)
                        Label(frame5, text=sub2, font=(24), fg="dark blue", bg="gray").grid(row=3, column=0, padx=5,
                                                                                            pady=5)
                        Label(frame5, text=sub3, font=(24), fg="dark blue", bg="gray").grid(row=4, column=0, padx=5,
                                                                                            pady=5)
                        Label(frame5, text=sub4, font=(24), fg="dark blue", bg="gray").grid(row=5, column=0, padx=5,
                                                                                            pady=5)
                        Label(frame5, text=sub5, font=(24), fg="dark blue", bg="gray").grid(row=6, column=0, padx=5,
                                                                                            pady=5)
                        Label(frame5, text=sub6, font=(24), fg="dark blue", bg="gray").grid(row=7, column=0, padx=5,
                                                                                            pady=5)
                        Label(frame5, text="all hours", font=(24), fg="dark blue", bg="gray").grid(row=8, column=0,
                                                                                                   padx=5,
                                                                                                   pady=5)
                        Label(frame5, text=s1, font=(24), fg="dark blue", bg="gray").grid(row=2, column=1, padx=5,
                                                                                          pady=5)
                        Label(frame5, text=s2, font=(24), fg="dark blue", bg="gray").grid(row=3, column=1, padx=5,
                                                                                          pady=5)
                        Label(frame5, text=s3, font=(24), fg="dark blue", bg="gray").grid(row=4, column=1, padx=5,
                                                                                          pady=5)
                        Label(frame5, text=s4, font=(24), fg="dark blue", bg="gray").grid(row=5, column=1, padx=5,
                                                                                          pady=5)
                        Label(frame5, text=s5, font=(24), fg="dark blue", bg="gray").grid(row=6, column=1, padx=5,
                                                                                          pady=5)
                        Label(frame5, text=s6, font=(24), fg="dark blue", bg="gray").grid(row=7, column=1, padx=5,
                                                                                          pady=5)
                        Label(frame5, text=h, font=(24), fg="dark blue", bg="gray").grid(row=8, column=1, padx=5,
                                                                                         pady=5)

                    def go_back():
                        welcome.destroy()
                        welcome_page()

                    Button(frame5, font=20, text="search", bd=8, bg="dark blue", fg="white", activebackground='Gray',
                           activeforeground='light blue', width=20, command=confirm_search).grid(row=1, column=0,
                                                                                                 padx=20,
                                                                                                 pady=20)
                    Button(frame5, font=20, text="go back", bd=8, bg="dark blue", fg="white", activebackground='Gray',
                           activeforeground='light blue', width=20, command=go_back).grid(row=1, column=1,
                                                                                          padx=20, pady=20)
                    frame5.grid(row=0, column=0, padx=20, pady=20)

            def insert_file():
                filenamee = fd.askopenfilename()
                print(filenamee)
                c = load_data(filenamee)
                for i in c:
                    insert_new_records(i[0])
                    users_insert(i[1], i[2], i[0])

            def failed():
                frame3.destroy()
                frame5 = Frame(welcome)
                frame5.config(bg='light blue')
                frame7 = Frame(frame5)
                frame7.config(bg="light blue")
                Label(frame7, text="select student", font=(12), fg="dark blue", bg="light blue").grid(row=0, column=0,
                                                                                                      padx=6,
                                                                                                      pady=6)
                longgg = ttk.Combobox(frame7, values=failed_students_name(), font=(12))
                longgg.grid(row=0, column=1)
                frame7.grid(row=0, column=0, padx=5, pady=5)
                frame5.grid(row=0, column=0, padx=20, pady=20)

                def confirm_choose():
                    x = longgg.get()
                    frame8 = Frame(frame5)
                    frame8.config(bg='light blue')
                    p = failed_students_subject(x)

                    def fill_empty(a):
                        empty = Entry(frame8, font=(10), bd=5, bg="light blue", width=5)
                        l = Label(frame8, text=p[a], font=(10), bd=5, bg="light blue")
                        l.grid(row=a, column=0, padx=10, pady=10)
                        empty.grid(row=a, column=1, padx=10, pady=10)
                        return empty

                    frame8.grid(row=2, column=0, padx=5, pady=5)
                    listOfEntries = [fill_empty(idx) for idx in range(len(p))]

                    def save():
                        entries = []
                        for i in range(len(listOfEntries)):
                            entries.append(int(listOfEntries[i].get()))
                        for i in range(len(p)):
                            u_sucess(longgg.get(), p[i], entries[i])

                    Button(frame5, font=20, text="save", bd=8, bg="dark blue", fg="white", activebackground='Gray',
                           activeforeground='light blue', width=20, command=save).grid(row=3, column=0, columnspan=2,
                                                                                       padx=20,
                                                                                       pady=20)

                def go_back():
                    welcome.destroy()
                    welcome_page()

                Button(frame5, font=20, text="choose", bd=8, bg="dark blue", fg="white", activebackground='Gray',
                       activeforeground='light blue', width=20, command=confirm_choose).grid(row=1, column=0, padx=20,
                                                                                             pady=20)
                Button(frame5, font=20, text="go back", bd=8, bg="dark blue", fg="white", activebackground='Gray',
                       activeforeground='light blue', width=20, command=go_back).grid(row=1, column=1, padx=20,
                                                                                      pady=20)

            Button(frame3, font=20, text="insert one student degree ", bd=8, bg="dark blue", fg="white",
                   activebackground='Gray', activeforeground='light blue', width=20, command=insert_one_student).grid(
                row=1,
                column=0,
                padx=20,
                pady=20)
            Button(frame3, font=20, text="insert degree by csv file", bd=8, bg="dark blue", fg="white",
                   activebackground='Gray',
                   activeforeground='light blue', width=20, command=load_csv_file).grid(row=2, column=0, padx=20,
                                                                                        pady=20)
            Button(frame3, font=20, text="search student degree", bd=8, bg="dark blue", fg="white",
                   activebackground='Gray',
                   activeforeground='light blue', width=20, command=SERCH).grid(row=3, column=0, padx=20, pady=20)
            Button(frame3, font=20, text="update degree for student", bd=8, bg="dark blue", fg="white",
                   activebackground='Gray',
                   activeforeground='light blue', width=20, command=UPDATE).grid(row=4, column=0, padx=20, pady=20)
            Button(frame3, font=20, text="insert student names", bd=8, bg="dark blue", fg="white",
                   activebackground='Gray',
                   activeforeground='light blue', width=20, command=insert_file).grid(row=5, column=0, padx=20, pady=20)
            Button(frame3, font=20, text="update failed students", bd=8, bg="dark blue", fg="white",
                   activebackground='Gray',
                   activeforeground='light blue', width=20, command=failed).grid(row=6, column=0, padx=20, pady=20)

            def cv():
                welcome.destroy()
                myapp()

            Button(frame3, font=20, text="sign out", bd=8, bg="dark blue", fg="white", activebackground='Gray',
                   activeforeground='light blue', width=20, command=cv).grid(row=7, column=0, padx=20, pady=20)

            img = ImageTk.PhotoImage(Image.open("wel.jpg"))
            panel = Label(frame4, image=img)
            panel.grid(row=4, column=0)
            frame3.grid(row=0, column=0, padx=20, pady=20)
            frame4.grid(row=0, column=1, padx=20, pady=20)
            welcome.mainloop()

        def welcome_page2():
            welcome = Tk()
            app = FullScreenApp(welcome)
            my_name = wel_name(n, p)
            welcome.title('the result for ' + wel_name(n, p))
            welcome.iconbitmap('BIO.ico')
            welcome.config(bg='light blue')
            frame3 = Frame(welcome)
            frame4 = Frame(welcome)
            frame3.config(bg="light blue")
            frame4.config(bg="light blue")
            s1, s2, s3, s4, s5, s6 = find_old_degree(wel_name(n, p))
            h = find_old_hours(wel_name(n, p))
            if h >= 0 and h <= 15:
                x = "first"
            elif h >= 16 and h <= 30:
                x = "second"
            elif h >= 31 and h <= 48:
                x = "third"
            elif h >= 49 and h <= 66:
                x = "fourth"
            elif h >= 67 and h <= 85:
                x = "fifth"
            if x == "first":
                sub1, sub2, sub3, sub4, sub5, sub6 = "math0", "electric circuit", "scientific report", "introduction", "chemistry1", "requirements"
            if x == "second":
                sub1, sub2, sub3, sub4, sub5, sub6 = "chemistry2", "biology1", "IS", "programming", "math1", "creative thing"
            if x == "third":
                sub1, sub2, sub3, sub4, sub5, sub6 = "logic", "statics1", "programming 2", "math2", "desctete", "biology2"
            if x == "fourth":
                sub1, sub2, sub3, sub4, sub5, sub6 = "biochemistry", "biology", "os", "math3", "data structure", "statics2"
            if x == "fifth":
                sub1, sub2, sub3, sub4, sub5, sub6 = "genetics", "graphics", "databases", "algorithms", "Bio computing", "machine learning"
            Label(frame3, text=sub1, font=(24), fg="dark blue", bg="gray").grid(row=0, column=0, padx=15, pady=15)
            Label(frame3, text=sub2, font=(24), fg="dark blue", bg="gray").grid(row=1, column=0, padx=15, pady=15)
            Label(frame3, text=sub3, font=(24), fg="dark blue", bg="gray").grid(row=2, column=0, padx=15, pady=15)
            Label(frame3, text=sub4, font=(24), fg="dark blue", bg="gray").grid(row=3, column=0, padx=15, pady=15)
            Label(frame3, text=sub5, font=(24), fg="dark blue", bg="gray").grid(row=4, column=0, padx=15, pady=15)
            Label(frame3, text=sub6, font=(24), fg="dark blue", bg="gray").grid(row=5, column=0, padx=15, pady=15)
            Label(frame3, text="all hours", font=(24), fg="dark blue", bg="gray").grid(row=6, column=0, padx=15,
                                                                                       pady=15)
            Label(frame3, text=s1, font=(24), fg="dark blue", bg="gray").grid(row=0, column=1, padx=15, pady=15)
            Label(frame3, text=s2, font=(24), fg="dark blue", bg="gray").grid(row=1, column=1, padx=15, pady=15)
            Label(frame3, text=s3, font=(24), fg="dark blue", bg="gray").grid(row=2, column=1, padx=15, pady=15)
            Label(frame3, text=s4, font=(24), fg="dark blue", bg="gray").grid(row=3, column=1, padx=15, pady=15)
            Label(frame3, text=s5, font=(24), fg="dark blue", bg="gray").grid(row=4, column=1, padx=15, pady=15)
            Label(frame3, text=s6, font=(24), fg="dark blue", bg="gray").grid(row=5, column=1, padx=15, pady=15)
            Label(frame3, text=h, font=(24), fg="dark blue", bg="gray").grid(row=6, column=1, padx=15, pady=15)

            def take():
                Bt.destroy()
                image = pyautogui.screenshot(wel_name(n, p) + "result.png")
                say_sound(my_name, Academic_grade(s1, s2, s3, s4, s5, s6))
                messagebox.showinfo("my dear {}".format(wel_name(n, p)), "your degree save where you save your program")

                def cv():
                    welcome.destroy()
                    myapp()

                Button(frame3, font=20, text="sign out", bd=8, bg="dark blue", fg="white", activebackground='Gray',
                       activeforeground='light blue', width=20, command=cv).grid(row=7, column=0, columnspan=2, padx=15, pady=15)

            Bt = Button(frame3, text='screen shot and listen grade', font=(30), bd=8, bg="dark blue", fg="white",
                        activebackground='Gray', activeforeground='light blue', command=take)
            Bt.grid(row=7, column=0, columnspan=2, padx=15, pady=15)
            img = ImageTk.PhotoImage(Image.open("wel.jpg"))
            panel = Label(frame4, image=img)
            panel.grid(row=4, column=0)
            frame3.grid(row=0, column=0, padx=20, pady=20)
            frame4.grid(row=0, column=1, padx=20, pady=20)

            welcome.mainloop()

        if n == "":
            error_say("enter email")
        elif p == "":
            if v.get()==1 :
                forgetpassword(n)
                error_say("check your gmail account")
            else :
                error_say("enter password")
        else:

            db = MySQLdb.connect("localhost", "root", "", "bio")
            # prepare a cursor object using cursor() method
            cursor = db.cursor()
            sql = "SELECT * FROM users WHERE ( email = '%s'  )  AND password = '%s'" % (n, p)
            try:
                # Execute the SQL command
                cursor.execute(sql)
                # Fetch all the rows in a list of lists.
                results = list(cursor.fetchall())
                if len(results) > 0:
                    if n == "kafafy@gmail.com":
                        w()
                        welcome_page()
                    else:
                        w()
                        welcome_page2()
                else:
                    if v.get() ==1 :
                        forgetpassword(n)
                        error_say("check your gmail account")
                    else :
                        error_say("email or pass are wrong")
            except:
                print("you have an error")
            db.close()

    Button(frame1, font=20, text="log in", bd=8, bg="dark blue", fg="white", activebackground='Gray',
           activeforeground='light blue', command=login).grid(row=4, column=0, columnspan=2,pady=10)
    frame2 = Frame(form)
    frame2.config(bg="light blue")
    img = ImageTk.PhotoImage(Image.open("wel.jpg"))
    panel = Label(frame2, image=img)
    panel.grid(row=0, column=1, padx=20, pady=20)
    frame2.grid(row=0, column=1, padx=20, pady=20)
    form.mainloop()
myapp()