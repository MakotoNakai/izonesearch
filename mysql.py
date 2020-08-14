import sqlite3
import glob
import os
import io

# Build a database
PATH = os.path.join(os.getcwd(),"IZONE.db")
connect = sqlite3.connect(PATH)
cursor = connect.cursor()

# Create a table
create_tb_sql = """CREATE TABLE if not exists IZONE
                      (member text,
                       id int,
                       image blob,
                       PRIMARY KEY(member, id))
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
                     blob = f.read()

              # Insert a column (name of member, id, binary)
              cursor.execute("INSERT INTO IZONE VALUES(?, ?, ?)",(member, index, blob)) #変更の反映を行う

        # Show the message if done for each member
       print("{} done".format(member))


# Close the database
connect.commit() #データベースを閉じる
connect.close()