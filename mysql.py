# import sqlite3
import psycopg2
import glob
import os
import io

# Connect to PostgreSQL DBMS
#DATABASE_URL = "postgres://youylcnkjyfyfy:20a5d945df5a9da524c823962294428191105ef78735d82ff42d3ba216642a5b@ec2-50-16-198-4.compute-1.amazonaws.com:5432/d8o6aq59fi4v03"

#connect = psycopg2.connect(DATABASE_URL, sslmode='require')
connect = psycopg2.connect(
       database = 'izonedb',
       user ='makotonakai',
       password = 'postgresql',
       host = '192.168.50.30',
       port = 5432
)

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
