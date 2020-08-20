
import psycopg2
import os

# connect = psycopg2.connect(dbname = 'izonedb',port = 5432)
connect = psycopg2.connect(
       dbname = 'd8o6aq59fi4v03',
       user = 'youylcnkjyfyfy',
       password = '20a5d945df5a9da524c823962294428191105ef78735d82ff42d3ba216642a5b',
       host = 'ec2-50-16-198-4.compute-1.amazonaws.com',
       port = 5432
    )
db = connect.cursor()

try:
    db.execute("SELECT * FROM izonetable WHERE member='Sakura_Miyawaki'")
    rows = db.fetchall()

    # 全ての画像に関して
    for index in range(len(rows)):
        row = rows[index]
        filename = './static/img'+index+'.jpg'
        # ファイル名に書き込む
        with open(filename,'wb') as f:
            f.write(row[2])
            f.close()

    # # static ディレクトリのファイルリストを取得
    # filelist = glob.glob("./static/*")

    # # static ディレクトリのファイルリストを返す
    # return filelist

# もし任意のsqlite3エラーが起こったら、エラー文を返す
except psycopg2.errors as e:
    print("次のエラーが発生しました:"+e)

db.close()
connect.close()