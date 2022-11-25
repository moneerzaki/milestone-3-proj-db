# importing 
from flask import Flask, render_template, request, redirect
import pymysql
import random
import queries

# Configure Database (connecting to online database system)
host = "db4free.net"
user = "moneerzaki"
password = "12345678"
db = "projdb1"

connection = pymysql.connect(
    host = host,
    user = user,
    password = password,
    db = db,
)

cursor = connection.cursor()

command = """

"""

cursor.execute("use projdb1")
cursor.execute("select * from agents_table limit 20")
print(cursor.fetchall())
