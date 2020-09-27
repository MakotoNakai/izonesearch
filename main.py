from selenium.webdriver.support.ui import Select
from selenium import webdriver
from flask import *
from PIL import Image
import os
import glob
import random
import psycopg2

app = Flask(__name__)

# 最初の画面
@app.route('/', methods=["GET"])
def index():

    return render_template("index.html")



@app.route('/index', methods=["POST"])
def post():

    # 選んだメンバーの名前を取得
    name = request.form.get("name")
    num_pics = int(request.form.get("num_pics"))

    id_list = [random.randint(0, 40) for i in range(num_pics)]
    file_list = []

    for id_ in id_list:

        query = "SELECT * FROM izonetable WHERE member = %s AND id = %s"
        filename = "./pics/pic_{}.jpg".format(id_)

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

    brower = webdriver.Chrome()
    brower.get('')
    return render_template("result.html", file_list=file_list, name = name.replace('_', ' '), num_pics=num_pics)



if __name__ == "__main__":
    app.run(debug=True, threaded=True)


    
