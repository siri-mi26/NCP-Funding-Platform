#import os
#from flask import Flask, render_template, request, redirect, url_for
#from flask_sqlalchemy import SQLAlchemy
import sqlite3
from flask import g




#connect database in local pathway
adress = "C:/Users/1/Desktop/ncpdummarydata.db"

#connect local database
conn = sqlite3.connect(adress)

#set cursor
mycursor = conn.cursor()
###################################### SQL code example  #####################################

                                    #### searching ####
# #execute sql code
#
# #test searching 1
# #mycursor.execute("SELECT * FROM programs order by CLASS_CODE;")

# #test searching 2
# mycursor.execute("SELECT COUNT(*) AS count,min(MOBILITY_GRANT_FUNDING_RECIEVED)AS price_min, max(MOBILITY_GRANT_FUNDING_RECIEVED) AS price_max FROM programs;")
#
# #save the result by ".fetchall()" function
# myresult = mycursor.fetchall()
#
#
# #print the result
# for x in myresult:
#     print(x)


                                               #### Insert ####
## example 1
# def insert(CAMPUS_ID, UNIVERSITY_ID, CAMPUSES_NAME, CAMPUSES_STATE):
#     sql = "insert into campuses values (?, ?, ?, ?)"
#     conn = g.db
#     cursor = conn.cursor()
#     try:
#         cursor.execute(sql, (CAMPUS_ID, UNIVERSITY_ID, CAMPUSES_NAME, CAMPUSES_STATE))
#         conn.commit()
#     except Exception as e:
#         conn.rollback()
#         raise TypeError("insert error:{}".format(e))

#example 2
sql = "insert into campuses values (?, ?, ?, ?)"
mycursor.execute(sql, ("C3200", "UWA", "The University of Western Australia", "WA"))
conn.commit()
mycursor.execute("SELECT * FROM campuses;")
myresult = mycursor.fetchall()
for x in myresult:
     print(x)





                                    #### delete ####