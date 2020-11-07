
from flask import *
from PIL import Image
import os
import glob
import random
import psycopg2
import config_param as config
# config.py 固定パラメータを別ファイルに書き込む (value, name, num)

app = Flask(__name__)

# 最初の画面
@app.route('/')
def main():

    return render_template("index.html", lists1=config.value_list, lists2=config.num_pics_list)


@app.route('/index', methods=["POST"])
def index():

    # 選んだメンバーの名前を取得
    name = request.form.get("name")
    num_pics = int(request.form.get("num_pics"))

    for file in glob.glob('./static/pics/*.jpg'):
        os.remove(file)

    selected_name_list = ["selected" if i == config.value_list.index(name) else None for i in range(len(config.value_list))]
    selected_pics_list = ["selected" if i == config.num_pics_list.index(num_pics) else None for i in range(len(config.num_pics_list))]

    file_list = []

    id_list = [random.randint(0, 40) for i in range(num_pics)]

    for id_ in id_list:
    
        query = "SELECT * FROM izonetable WHERE member = %s AND id = %s"
        filename = "./static/pics/pic_{}.jpg".format(id_)

        DATABASE_URL = os.environ.get('DATABASE_URL')
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

    return render_template("result.html", lists1=zip(config.value_list, selected_name_list), lists2=zip(config.num_pics_list, selected_pics_list), file_list=file_list)


if __name__ == "__main__":
    app.run(debug=True, threaded=True)


    
