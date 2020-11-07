# import sqlite3
import psycopg2
import glob
import os
import io

# Connect to PostgreSQL DBMS
DATABASE_URL = os.environ.get('DATABASE_URL')

connect = psycopg2.connect(DATABASE_URL, sslmode='require')
# connect = psycopg2.connect("user=postgres dbname=izonedb")
cursor = connect.cursor()

create_tb_sql = """ CREATE TABLE IF NOT EXISTS izonetable
                      (member text,
                       id int,
                       image bytea,
                       PRIMARY KEY (member, id))
                """


# Execute the command above
cursor.execute(create_tb_sql)


# Directories below the current folder
member_list = ["Eunbi", "Sakura", "Hyewon", "Yena", "Cheyeon","Chewon","Minju", "Nako", "Hitomi", "Yuri", "Yujin", "Wonyoung"]


# For each member
for member in member_list:

    # The list of all pics
       pic_list = glob.glob("./images/{}/*.jpg".format(member))

        # For each pic
       for index in range(len(pic_list)):

              fp = open(pic_list[index], 'rb').read()
              cursor.execute("INSERT INTO izonetable (member, id, image) VALUES (%s, %s, %s)",(member, index, psycopg2.Binary(fp))) #変更の反映を行う
              connect.commit()

        # Show the message if done for each member
       print("{} done".format(member))


# # Close the database
 #データベースを閉じる
cursor.close()
connect.close()
