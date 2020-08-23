from flask import *
from flask_sqlalchemy import SQLAlchemy
from PIL import Image

#import sqlite3
import psycopg2
import os
import shutil
import io
import random
import string
import glob
import boto3

app = Flask(__name__)
    
 # ランダムな文字列を生成する
def generate_random_string():
    randlst = [random.choice(string.ascii_letters + string.digits) for i in range(10)]
    return ''.join(randlst)

# メンバーの名前に対応する画像を全部取り出す
# def get_name(member_name):

    # connect = psycopg2.connect(
    #    dbname = 'd8o6aq59fi4v03',
    #    user = 'youylcnkjyfyfy',
    #    password = '20a5d945df5a9da524c823962294428191105ef78735d82ff42d3ba216642a5b',
    #    host = 'ec2-50-16-198-4.compute-1.amazonaws.com',
    #    port = 5432
    # )
    # db = connect.cursor()

    #  # コネクションエラーが発生しない限り以下の処理を実行する
    # try:
    #     db.execute('SELECT * FROM izonetable WHERE member=%s AND id=%s', (member_name, 0))
    #     rows = db.fetchall()
    #     # 全ての画像に関して
    #     for row in rows:
    #      filename = './static/'+generate_random_string()+'.jpg'
    #      # ファイル名に書き込む
    #      with open(filename,'wb') as f:
    #          f.write(row[2])
    #          f.close()

    #     db.close()
    #     connect.close()

    #     # static ディレクトリのファイルリストを取得
    #     filelist = glob.glob("./static/*")

    #     # static ディレクトリのファイルリストを返す
    #     return filelist

    # # もし任意のsqlite3エラーが起こったら、エラー文を返す
    # except psycopg2.errors as e:
    #     return "次のエラーが発生しました:"+e

    

# 最初の画面
@app.route('/', methods=["GET"])
def index():

    # # staticフォルダ内のjpgファイルを削除
    # all_files = glob.glob('static/*.jpg', recursive=True)

    # for file in all_files:

    #     os.remove(file)

    # メンバーの名前を選ぶ
    name = request.form.get("name")

    # とりあえず最初は filelist は None
    filelist = None
    id = None

    # return render_template("index.html",name=name, filelist=filelist)
    return render_template("index.html", link = None)

# @app.route('/static/<path:path>')
# def send_image(path):
#     return send_from_directory('./static', path)


@app.route('/index', methods=["POST"])
def post():

    # 選んだメンバーの名前を取得

    name = request.form["name"]
    id = request.form["id"]

    s3_client = boto3.client('s3')

    BUCKET = 'izonebucket'
    OBJECT = 'IZONE/{}/pic_{}.jpg'.format(name, id)

    link = s3_client.generate_presigned_url(
        'get_object',
        Params={'Bucket': BUCKET, 'Key': OBJECT},
        ExpiresIn=300)

    return render_template("index.html", link=link)

    # メンバーの画像全て取得
    # filelist = get_image(name)

    # return render_template("index.html",name=name, id=id, filelist=filelist)



if __name__ == "__main__":
    app.run(debug=True, threaded=True)
    # app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

    
