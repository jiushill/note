import sqlite3

conn=sqlite3.connect("data.db")
print("Connect Sqlite Sucess")
c=conn.cursor()
c.execute('''CREATE TABLE WX (title TEXT NOT NULL,url NOT NULL,time NOt NULL,numbername NOT NULL)''')
print("Create Table Sucess")