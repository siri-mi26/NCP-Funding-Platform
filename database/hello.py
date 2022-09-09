from flask import g
import sqlite3
import os
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

PROJECT_ROOT = "C:/Users/1/Desktop"
DATABASE_INITFILE = os.path.join(PROJECT_ROOT, "newdummydata.sql")

def connect_db():
    db = getattr(g, 'db', None)
    if db is None:
        db = g.db = sqlite3.connect(DATABASE)
    return db

def init_db(): #使用数据库建模文件初始化数据库，在命令行中使用一次即可。
    print(".sql file path:{}".format(DATABASE_INITFILE))
    with app.app_context():
        db = connect_db()
        with app.open_resource(DATABASE_INITFILE, mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

def before_request():
    g.db=connect_db()

def close_db(exception):
    if hasattr(g, 'db'):
        g.db.close()


#
# ##EXAMPLE TO INSERT DATA
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
#
#
# ##
# def query_db(query, args=(), one=False):
#     cur=g.db.execute(query, args)
#     rv=[dict((cur.description[idx][0], value) for idx,value in enumerate(row)) for row in cur.fetchall()]
#     return (rv[0] if rv else None) if one else rv
#
#
# ##################################################
# @app.route('/campuses') #增加campuses信息页面
# def student():
#     return render_template('campuses.html')
#
# @app.route('/add', methods=['POST','GET'])
# def add():
#     if request.method=='POST':
#         CAMPUS_ID = request.form['CAMPUS_ID']
#         UNIVERSITY_ID = request.form['UNIVERSITY_ID']
#         CAMPUSES_NAME = request.form['CAMPUSES_NAME']
#         CAMPUSES_STATE = request.form['CAMPUSES_STATE']
#
#         try:
#             insert(CAMPUS_ID, UNIVERSITY_ID, CAMPUSES_NAME, CAMPUSES_STATE)
#             return redirect(url_for('result'))
#         except Exception as e:
#             flash("{}".format(e))
#             return redirect(url_for('campuses'))
#
# @app.route('/result') #所有campuses信息list页面
# def result():
#     rows=query_db("select * from campuses")
#     return render_template('result.html', rows=rows)
#
if __name__ == '__main__':
    app.run()