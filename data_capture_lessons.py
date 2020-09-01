
import os
import sqlite3
import traceback


file_root = os.path.abspath(os.path.join(os.getcwd(),".."))
db = file_root+os.path.sep+"MagicRoom.db"

def get_Lessons():
    print (db)
    connection = sqlite3.connect(db)
    cur = connection.cursor()
    sql = "select Lesson_ID, Lesson_Title, Factual_Term1, Factual_Term2,Factual_Term3, Application_Step_Description_1,Application_Steps_Number from Magic_Science_Lessons"
    cur.execute(sql)
    rows = cur.fetchall()
    list_lessons = []
    for element in rows:
        list_lessons.append(element)
    connection.commit()
    connection.close()
    return list_lessons

def delete_lesson(lesson_id):
    try:
        connection = sqlite3.connect(db)
        cur = connection.cursor()
        sql = ("delete from Magic_Science_Lessons where Lesson_ID = ?")
        cur.execute(sql, (lesson_id,))
        connection.commit()
        cur = connection.cursor()
        sql = ("select seq from sqlite_sequence where name = 'Magic_Science_Lessons'")
        cur.execute(sql)
        row = cur.fetchone()
        sql1 = ("update sqlite_sequence set seq=? where name='Magic_Science_Lessons'")
        sequence = row[0] -1
        cur.execute(sql1,(sequence,))
        connection.commit()
        connection.close()

        return 0
    except sqlite3.OperationalError:
        traceback.print_exc()
        return 1

def get_lessons_for_share(lesson_id):
    connection = sqlite3.connect(db)
    cur = connection.cursor()
    sql = "select Lesson_ID, Lesson_Title, Title_Image,Title_Video,Title_Running_Notes,Factual_Term1,Factual_Term1_Description,Factual_Image1,Factual_Term2,Factual_Term2_Description,Factual_Image2,Factual_Term3,Factual_Term3_Description,Factual_Image3," \
          "Application_Steps_Number,Application_Step_Description_1,Application_Step_Description_2,Application_Step_Description_3,Application_Step_Description_4,Application_Step_Description_5,Application_Step_Description_6,Application_Step_Description_7," \
          "Application_Step_Description_8,Application_Steps_Widget_1,Application_Steps_Widget_2,Application_Steps_Widget_3,Application_Steps_Widget_4,Application_Steps_Widget_5,Application_Steps_Widget_6,Application_Steps_Widget_7," \
          "Application_Steps_Widget_8,IP_Questions,Apply_External_Link from Magic_Science_Lessons where Lesson_ID=?"
    cur.execute(sql,(lesson_id,))
    rows = cur.fetchall()
    connection.commit()
    connection.close()
    return rows[0]

def get_user_classid():
    connection = sqlite3.connect(db)
    cur = connection.cursor()
    sql = "select class_id, User from Magic_Teacher_Data where Class_No=?"
    cur.execute(sql,(1,))
    rows = cur.fetchall()[0]
    connection.commit()
    connection.close()
    return rows[0],rows[1]


def update_shared(lesson_id):
    connection = sqlite3.connect(db)
    cur = connection.cursor()
    sql = "update Magic_Science_Lessons set Shared_Flag=1 where Lesson_ID=?"
    cur.execute(sql, (lesson_id,))
    connection.commit()
    connection.close()

def is_shared(lesson_id):
    connection = sqlite3.connect(db)
    cur = connection.cursor()
    sql = "select Shared_Flag from Magic_Science_Lessons where Lesson_ID=?"
    cur.execute(sql, (lesson_id,))
    rows = cur.fetchone()
    connection.commit()
    connection.close()
    return rows[0]


def insert_imported_record(query_parameters):
    try:
        connection = sqlite3.connect(db)
        cur = connection.cursor()
        sql = ('insert into Magic_Science_Lessons (Lesson_Title,Title_Image,Title_Video,Title_Running_Notes,Factual_Term1,Factual_Term1_Description,Factual_Image1,Factual_Term2,Factual_Term2_Description,Factual_Image2,Factual_Term3,Factual_Term3_Description,'
                       'Factual_Image3,Application_Steps_Number,Application_Step_Description_1,Application_Steps_Widget_1,Application_Step_Description_2,Application_Steps_Widget_2,Application_Step_Description_3,Application_Steps_Widget_3,Application_Step_Description_4,Application_Steps_Widget_4,'
                       'Application_Step_Description_5,Application_Steps_Widget_5, Application_Step_Description_6,Application_Steps_Widget_6, Application_Step_Description_7, Application_Steps_Widget_7,Application_Step_Description_8,Application_Steps_Widget_8,'
                       'IP_Questions) values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)')
        cur.execute(sql, query_parameters)
        connection.commit()
        connection.close()
    except (Exception):
        traceback.print_exc()
def get_new_id():
    try:
        connection = sqlite3.connect(db)
        cur = connection.cursor()
        sql = "SELECT seq FROM sqlite_sequence where name = 'Magic_Science_Lessons'"
        cur.execute(sql)
        rows = cur.fetchone()
        new_id = rows[0]
        return new_id
    except sqlite3.OperationalError:
        traceback.print_exc()

