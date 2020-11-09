
# ライブラリをインポートする
from flask import *
from PIL import Image
import os
import glob
import random
import psycopg2
import config_param as config # config_param.py


app = Flask(__name__)

# 最初の画面
@app.route('/')
def main():

    # 最初のページを表示
    return render_template("index.html", lists1=config.name_list, lists2=config.num_pics_list)


# インデックスディレクトリの関数
@app.route('/index', methods=["POST"])
def index():

    # 選んだメンバーの名前を取得
    name = request.form.get("name")

    # 選んだ枚数(文字列)を取得
    num_pics = int(request.form.get("num_pics"))

    # picsディレクトリ(画像を格納するディレクトリ)の中身を全部消す
    for file in glob.glob('./static/pics/*.jpg'):
        os.remove(file)

    # どの名前を選んだ/選んでないかの配列
    selected_name_list = ["selected" if i == config.name_list.index(name) else None for i in range(len(config.name_list))]
    
    # どの枚数を選んだ/選んでないかの配列
    selected_pics_list = ["selected" if i == config.num_pics_list.index(num_pics) else None for i in range(len(config.num_pics_list))]

    # 画像ファイルのパスの配列
    file_list = []

    # 表示の画像のidの配列
    id_list = [random.randint(0, 40) for i in range(num_pics)]

    
    for id_ in id_list:
    
        # 対応するメンバー名&IDの画像を取得
        query = "SELECT * FROM izonetable WHERE member = %s AND id = %s"

        # 画像のファイル名
        filename = "./static/pics/pic_{}.jpg".format(id_)

        DATABASE_URL = "postgres://youylcnkjyfyfy:20a5d945df5a9da524c823962294428191105ef78735d82ff42d3ba216642a5b@ec2-50-16-198-4.compute-1.amazonaws.com:5432/d8o6aq59fi4v03"
        connect = psycopg2.connect(DATABASE_URL, sslmode='require')
        cursor = connect.cursor() 

        try:

            # クエリを実行
            cursor.execute(query, (name, id_))

            # データをフェッチ
            fetch = cursor.fetchone()
            
            # 画像のバイナリを取り出す
            image = fetch[2]

            # ファイル名に書き込み
            with open(filename, 'wb') as f:
                f.write(bytes(image))

            # 書き込んだ画像ファイルのパスを配列file_listに追加
            file_list.append(filename)

        except Exception as e:
            print(e)

        finally:
            cursor.close()
            connect.close()

    # 変更後のファイルを表示する
    return render_template("result.html", lists1=zip(config.name_list, selected_name_list), lists2=zip(config.num_pics_list, selected_pics_list), file_list=file_list)


if __name__ == "__main__":

    # アプリを実行
    app.run(debug=True, threaded=True)


    
