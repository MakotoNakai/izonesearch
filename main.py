
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

    # メンバーの名前を選ぶ
    name = request.form.get("name")

    # とりあえず最初は filelist は None
    filelist = None
    id = None

    # return render_template("index.html",name=name, filelist=filelist)
    return render_template("index.html", links = None)



@app.route('/index', methods=["POST"])
def post():

    # 選んだメンバーの名前を取得
    name = request.form["name"]
    num_pics = int(request.form["num_pics"])

    # s3_client = boto3.client('s3')
    # bucket = 'izonebucket'
    # links = []

    # for id in range(num_pics):

    #     link = s3_client.generate_presigned_url(
    #         'get_object',
    #         Params={'Bucket': bucket, 'Key': 'IZONE/{}/pic_{}.jpg'.format(name, str(id))},
    #         ExpiresIn=300)
            
    #     links.append(link)

    id_list = [random.randint(0, 40) for i in range(num_pics)]
    file_list = []

    for id_ in id_list:

        query = "SELECT * FROM izonetable WHERE member = %s AND id = %s"
        filename = "./static/pic_{}.jpg".format(id_)

        # connect = psycopg2.connect("user=postgres dbname=izonedb")
        # cursor = connect.cursor()
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


    return render_template("result.html", file_list=file_list, name = name.replace('_', ' '), num_pics=num_pics)



if __name__ == "__main__":
    app.run(debug=True, threaded=True)


    
