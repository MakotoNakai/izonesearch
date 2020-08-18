# import sqlite3
import psycopg2
import glob
import os
import io

# postgresql://{username}:{password}@{hostname}:{port}/{database}
# postgres://youylcnkjyfyfy:20a5d945df5a9da524c823962294428191105ef78735d82ff42d3ba216642a5b@ec2-50-16-198-4.compute-1.amazonaws.com:5432/d8o6aq59fi4v03

# Connect to PostgreSQL DBMS
connect = psycopg2.connect(
       dbname = 'd8o6aq59fi4v03',
       user = 'youylcnkjyfyfy',
       password = '20a5d945df5a9da524c823962294428191105ef78735d82ff42d3ba216642a5b',
       host = 'ec2-50-16-198-4.compute-1.amazonaws.com',
       port = 5432
)
# connect.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
# print(connect.get_backendpid())

# Obtain a DB Cursor
cursor = connect.cursor()

 
# Create table statement
#sqlCreateDatabase = "create database "+name_Database+";"

# Create a table in PostgreSQL database
#cursor.execute(sqlCreateDatabase)

# Build a database
# dsn = os.environ.get('DATABASE_URL')
# connect = sqlite3.connect(PATH)
# cursor = connect.cursor()
# connect = psycopg2.connect(dbname=db_name, user=username, password=password)
# cursor = connect.cursor()

# Create a table
# delete_tb_sql = "drop table izonetable"
# cursor.execute(delete_tb_sql)

create_tb_sql = """create table izonetable
                      (member text,
                       id int,
                       image bytea,
                       primary key(member, id))
                """


# Execute the command above
cursor.execute(create_tb_sql)


# Directories below the current folder
member_list = ["Kwon_Eunbi", "Sakura_Miyawaki", "Hyewon_Kang", "Yena_Choi", "Cheyeon_Lee","Chewon_Kim","Minju_Kim", "Nako_Yabuki", "Hitomi_Honda", "Yuri_Choi", "Yujin_Ahn", "Wonyoung_Chang"]


# For each member
for member in member_list:

    # The list of all pics
       pic_list = glob.glob("./IZONE/{}/*.jpg".format(member))

        # For each pic
       for index in range(len(pic_list)):

            # Change an image data into binary string
              with open(pic_list[index], 'rb') as f:
                     bytea = f.read()

                     # Insert a column (name of member, id, binary)
                     cursor.execute("insert into izonetable (member, id, image) VALUES (%s, %s, %s)",(member, index, bytea)) #変更の反映を行う

        # Show the message if done for each member
       print("{} done".format(member))


# # Close the database
connect.commit() #データベースを閉じる
connect.close()
