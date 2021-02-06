
from flask import *
from PIL import Image
import os
import glob
import random
import psycopg2
import config_param as config


app = Flask(__name__)

@app.route('/')
def main():

    return render_template("index.html", lists1=config.name_list, lists2=config.num_pics_list)


@app.route('/index', methods=["POST"])
def index():

    name = request.form.get("name")

    num_pics = int(request.form.get("num_pics"))

    for file in glob.glob('./static/pics/*.jpg'):
        os.remove(file)

    selected_name_list = ["selected" if i == config.name_list.index(name) else None for i in range(len(config.name_list))]
    
    selected_pics_list = ["selected" if i == config.num_pics_list.index(num_pics) else None for i in range(len(config.num_pics_list))]

    file_list = []

    id_list = [random.randint(0, 40) for i in range(num_pics)]

    
    for id_ in id_list:
    
        query = "SELECT * FROM izonetable WHERE member = %s AND id = %s"

        filename = "./static/pics/pic_{}.jpg".format(id_)

        DATABASE_URL = "postgres://youylcnkjyfyfy:20a5d945df5a9da524c823962294428191105ef78735d82ff42d3ba216642a5b@ec2-50-16-198-4.compute-1.amazonaws.com:5432/d8o6aq59fi4v03"
        # connect = psycopg2.connect(DATABASE_URL, sslmode='require')
        connect = psycopg2.connect(
            database = 'izonedb',
            user ='makotonakai',
            password = 'postgresql',
            host = '192.168.50.30',
            port = 5432
        )
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

    return render_template("result.html", lists1=zip(config.name_list, selected_name_list), lists2=zip(config.num_pics_list, selected_pics_list), file_list=file_list)


if __name__ == "__main__":

    app.run(host="0.0.0.0", debug=True, threaded=True)


    
