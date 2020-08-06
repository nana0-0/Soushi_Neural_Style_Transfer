import os
# request フォームから送信した情報を扱うためのモジュール
# redirect  ページの移動
# url_for アドレス遷移
from flask import Flask, request, redirect, url_for,render_template, flash
# ファイル名をチェックする関数
from werkzeug.utils import secure_filename
# 画像のダウンロード
from flask import send_from_directory
from mystylize import neural_style_transfer, ITERATIONS
from threading import Thread
from pathlib import Path
import json
from mystylize import neural_style_transfer
import glob
import re
from natsort import natsorted

UPLOAD_FOLDER = './uploads'
# アップロードされる拡張子の制限
ALLOWED_EXTENSIONS = set(['png', 'jpg',"jpeg"])

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config["SECRET_KEY"] = "nanaaisiteru"


#json_open = open(f"output/tokage8.jpg.1000.json","r")
#sv_info = json.load(json_open)


# l = OUTPUT_PATH+f"{filename}.{iteration}.json"
#OUTPUT_PATH = "./output"
#json_open = open(OUTPUT_PATH+f"{file.filename}.{iteration}.json")
#sv_info = json.load(json_open)
#for x in range(1000):
#   with open("file{0}.json".format(x), "r") as f:
       

def allwed_file(filename):
    # .があるかどうかのチェックと、拡張子の確認
    # OKなら１、だめなら0
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    # return '.' in filename and filename.split('.')[-1].lower() in ALLOWED_EXTENSIONS

@app.route('/',methods=["GET","POST"])
def index():
    if request.method == 'POST':
        print(f"POST {request.files['file'].filename}")
        # ファイルがなかった場合の処理
        if 'file' not in request.files:
            flash('ファイルがありません')
            return redirect(request.url)
        # データの取り出し
        file = request.files['file']
        # ファイル名がなかった時の処理
        if file.filename == '':
            flash('ファイルがありません')
            return redirect(request.url)
        # ファイルのチェック
        if file and allwed_file(file.filename):
            # 危険な文字を削除（サニタイズ処理）
            filename = secure_filename(file.filename)
            # ファイルの保存
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            # アップロード後のページに転送
            return redirect(url_for('status', filename=filename))
    else:
        return render_template('form.html.jinja', title='flask test') #変更

is_traning = False

def train(filename):
    global is_traning
    if not is_traning:
        # Thread(target=neural_style_transfer,args=(filename,)).start()
        is_traning = True
        print("training start")
        neural_style_transfer(filename)
        is_traning = False
@app.route('/status/<filename>')
def status(filename):
    numbers = []

    for f in Path("./output").iterdir():
        name_list = f.name.rsplit(".",2)
        if name_list[0] == filename:
            num = int(name_list[1])
            numbers.append(num)

    if len(numbers) == 0:
        max_num = 0
    else:
        max_num = max(numbers)
              
    jsons = []
    max_json_num = ""
    min_json_num = ""
              
    for x in natsorted(glob.glob(f'output/{filename}*.json')):
        jsons.append(f'{x}')
        print(jsons)
        if len(jsons) == 0:
            max_json_num = 0
        else:
            max_json_num = max(jsons)

        print(max_json_num)
        min_json_num = jsons[0]
        print(jsons[0])

    if jsons == []:
        val_loss_cen = 0
    else:
        cen = int(len(jsons)/2)
        cen_new = jsons[cen]
        json_open_cen = open(f"{cen_new}","r")
        val_loss_cen = json.load(json_open_cen)
        print(cen)
       
    if max_json_num == "":
        val_loss_max = 0

    else:
        json_open_max = open(f"{max_json_num}","r")
        val_loss_max = json.load(json_open_max)
        #return render_template("status.html.jinja",val_loss=sv_info)
    
    if min_json_num == "":
        val_loss_min = 0

    else:
        json_open_min = open(f"{min_json_num}","r")
        val_loss_min = json.load(json_open_min)



    return render_template("status.html.jinja",filename=filename, max_iteration=max_num, val_loss_max=val_loss_max, val_loss_cen=val_loss_cen, val_loss_min=val_loss_min)

@app.route('/uploads/<filename>')
@app.route('/uploads/<filename>/<iteration>')
# ファイルを表示する
def uploaded_file(filename,iteration):
    numbers = []

    for f in Path("./output").iterdir():
        name_list = f.name.rsplit(".",2)
        if name_list[0] == filename:
            num = int(name_list[1])
            numbers.append(num)

    if len(numbers) == 0:
        Thread(target=train,args=(filename,)).start()

        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


    if iteration:
        return send_from_directory("output", f"{filename}.{iteration}.jpg")

    max_num = max(numbers)

    if max_num < ITERATIONS-1:
        Thread(target=train,args=(filename,)).start()

    output_filename = f"{filename}.{max_num}.jpg"

    return send_from_directory("output", output_filename)

@app.route('/example/<filename>')
# ファイルを表示する
def example(filename):
    return send_from_directory("neural_style/examples", filename)


## おまじない
if __name__ == "__main__":
    app.run(debug=True,port=1234,host="0.0.0.0")
