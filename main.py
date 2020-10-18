
from flask import *
from PIL import Image
import os
import glob
import random
import psycopg2

app = Flask(__name__)

# 最初の画面
@app.route('/')
def main():

    value_list = ["Kwon_Eunbi", "Sakura_Miyawaki", "Hyewon_Kang", "Yena_Choi", "Cheyeon_Lee", \
                "Chewon_Kim", "Minju_Kim", "Nako_Yabuki", "Hitomi_Honda", "Yuri_Choi", "Yujin_Ahn", "Wonyoung_Chang"]
    name_list = ["Kwon Eunbi", "Sakura Miyawaki", "Hyewon Kang", "Yena Choi", "Cheyeon Lee", \
                "Chewon Kim", "Minju Kim", "Nako Yabuki", "Hitomi Honda", "Yuri Choi", "Yujin Ahn", "Wonyoung hang"]
    
    num_pics_list = [1, 5, 10, 20]
    str_pics_list = [str(num) for num in num_pics_list]

    return render_template("index.html", lists1=zip(value_list, name_list), lists2=zip(num_pics_list, str_pics_list))
    

@app.route('/index', methods=["POST"])
def index():

    # 選んだメンバーの名前を取得
    name = request.form.get("name")
    num_pics = request.form.get("num_pics")

    for file in glob.glob('./static/pics/*.jpg'):
        os.remove(file)

    value_list = ["Kwon_Eunbi", "Sakura_Miyawaki", "Hyewon_Kang", "Yena_Choi", "Cheyeon_Lee", \
                "Chewon_Kim", "Minju_Kim", "Nako_Yabuki", "Hitomi_Honda", "Yuri_Choi", "Yujin_Ahn", "Wonyoung_Chang"]
    name_list = ["Kwon Eunbi", "Sakura Miyawaki", "Hyewon Kang", "Yena Choi", "Cheyeon Lee", \
                "Chewon Kim", "Minju Kim", "Nako Yabuki", "Hitomi Honda", "Yuri Choi", "Yujin Ahn", "Wonyoung hang"]
    selected_name_list = ["selected" if i == value_list.index(name) else None for i in range(len(value_list))]

    num_pics_list = [1, 5, 10, 20]
    str_pics_list = [str(num) for num in num_pics_list]
    selected_pics_list = ["selected" if i == str_pics_list.index(num_pics) else None for i in range(len(num_pics_list))]


    file_list = []

    id_list = [random.randint(0, 40) for i in range(int(num_pics))]
    for id_ in id_list:
    
        query = "SELECT * FROM izonetable WHERE member = %s AND id = %s"
        filename = "./static/pics/pic_{}.jpg".format(id_)

        DATABASE_URL = "postgres://youylcnkjyfyfy:20a5d945df5a9da524c823962294428191105ef78735d82ff42d3ba216642a5b@ec2-50-16-198-4.compute-1.amazonaws.com:5432/d8o6aq59fi4v03"
        connect = psycopg2.connect(DATABASE_URL, sslmode='require')
        cursor = connect.cursor() 

        try:
            cursor.execute(query, (name, id_))
            fetch = cursor.fetchone()
            
            image = fetch[2]

            with open(filename, 'wb') as f:
                f.write(bytes(image))
            file_list.append(filename)

        except Exception as e:
            print(e)

        finally:
            cursor.close()
            connect.close()

    return render_template("result.html", lists1=zip(value_list, name_list, selected_name_list), lists2=zip(str_pics_list, num_pics_list, selected_pics_list), file_list=file_list)


if __name__ == "__main__":
    app.run(debug=True, threaded=True)


    
