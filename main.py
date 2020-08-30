from flask import *
from PIL import Image
import glob
import boto3

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

    s3_client = boto3.client('s3')
    bucket = 'izonebucket'
    links = []

    for id in range(num_pics):

        link = s3_client.generate_presigned_url(
            'get_object',
            Params={'Bucket': bucket, 'Key': 'IZONE/{}/pic_{}.jpg'.format(name, str(id))},
            ExpiresIn=300)
            
        links.append(link)



    return render_template("result.html", links=links, name = name.replace('_', ' '), num_pics=num_pics)



if __name__ == "__main__":
    app.run(debug=True, threaded=True)


    
