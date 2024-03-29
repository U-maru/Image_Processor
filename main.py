from flask import Flask, request, render_template, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
import os, glob, json, random

from image_process import ImageProcessor

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './upload_images'
app.config['OUTPUT_FOLDER'] = './output_images'
app.config["JSON_AS_ASCII"] = False  # 日本語などのASCII以外の文字列を返したい場合は、こちらを設定しておく

# 登録可能なファイルの拡張子
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# 登録可能なファイルかどうか判定
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# 画像ファイルの登録受付
# http://127.0.0.1:5000/upload
@app.route('/upload', methods=['POST'])
def upload_image():
    # ファイルがなければ登録フォームに返す
    if 'file' not in request.files:
        return render_template("image_form.html", message_err="　画像ファイルが指定されていません！")

    # 登録する画像ファイルの取得
    fs = request.files['file']

    # 登録可能なファイルかどうかチェック
    if not allowed_file(fs.filename):
        return render_template("image_form.html", message_err="　アップロードできるファイルは、PNG, JPG, JPEG, GIF形式のみです！")

    # ファイルに名前がなければ登録フォームに返す
    if '' == fs.filename:
        return render_template("image_form.html", message_err="　画像ファイルを指定してください！")

    # ファイルを保存（upload_imagesに保存）
    fs.save('./upload_images/' + secure_filename(fs.filename))

    # 画像処理を行うクラスにてそれぞれ処理を実行
    img_path = "./upload_images/" + secure_filename(fs.filename)
    ImageProcessor().process(img_path)

    return render_template("image_form.html", message_suc="　画像のアップロードが完了しました！")

# アップロードファイル一覧
@app.route('/uploaded_list/')
def uploaded_list():
    files = glob.glob("./upload_images/*")  # ./upload_images/以下のファイルをすべて取得
    urls = []
    for file in files:
        urls.append({
            "filename": os.path.basename(file),
            "url": "/uploaded/" + os.path.basename(file)
        })
    # 画像の名前とURLを格納した'urls'を変数として渡す
    return render_template("images_list.html", title="アップロード済み画像", page_title="アップロード済み画像　一覧", target_files=urls)

# 画像処理後のファイル一覧(グレイスケール)
@app.route('/grayscale_list/')
def processed_gs_list():
    files = glob.glob("./output_images/gs/*")
    urls = []
    for file in files:
        urls.append({
            "filename": os.path.basename(file),
            "url": "/processed/gs/" + os.path.basename(file)
        })
    return render_template("images_list.html", title="グレースケール画像", page_title="グレースケール画像　一覧", target_files=urls)

# 画像処理後のファイル一覧(二値化)
@app.route('/binary_list/')
def processed_bin_list():
    files = glob.glob("./output_images/bin/*")
    urls = []
    for file in files:
        urls.append({
            "filename": os.path.basename(file),
            "url": "/processed/bin/" + os.path.basename(file)
        })
    return render_template("images_list.html", title="二値化画像", page_title="二値化画像　一覧", target_files=urls)

# 画像処理後のファイル一覧(モザイク)
@app.route('/mozaiku_list/')
def processed_mozaiku_list():
    files = glob.glob("./output_images/mozaiku/*")
    urls = []
    for file in files:
        urls.append({
            "filename": os.path.basename(file),
            "url": "/processed/mozaiku/" + os.path.basename(file)
        })
    return render_template("images_list.html", title="モザイク画像", page_title="モザイク画像　一覧", target_files=urls)

# 問題へ進むページ
@app.route('/uploadedList')
def uploadedList():
    files = glob.glob("./upload_images/*")  # ./uploadsPicture/以下のファイルをすべて取得
    urls = []
    index = 0
    for file in files:
        urls.append({
            "filename": os.path.basename(file),
            "url": "/uploaded/" + os.path.basename(file),
            "index": index
        })
        index = index + 1
    return render_template("pictureList.html", title="アップロード済み画像", page_title="アップロード済み画像　一覧", target_files=urls)

# 選択されたデータを'selectData.json'に保存
@app.route('/setData', methods = ['POST'])
def setData():
    print("setData")
    selectData = request.form.to_dict()
    jsonData = list()
    jsonData.append(selectData)

    # 元の画像のパスを追加
    jsonData[0]['originalImage'] = "/uploaded/" + jsonData[0]['image']

    # 処理後の画像のパスのlist
    answerList = [
        ['/processed/gs/', 'gs', 'グレースケール'],
        ['/processed/bin/', 'bin', '二値化'],
        ['/processed/mozaiku/', 'mozaiku', 'モザイク']
    ]
    # 答えとなるインデックスをランダムに決定(0~2)
    randomIndex = random.randint(0, 2)

    # 処理後の画像のパスを追加
    jsonData[0]['changedImage'] = answerList[randomIndex][0] + jsonData[0]['image']
    # 答えを追加
    jsonData[0]['answer'] = [answerList[randomIndex][1], answerList[randomIndex][2]]

    # 解答欄の選択肢を追加
    options = random.sample(answerList, len(answerList))    # 選択肢の順番をシャッフル
    jsonData[0]['firstOption'] =[options[0][1], options[0][2]]
    jsonData[0]['secondOption'] = [options[1][1], options[1][2]]
    jsonData[0]['thirdOption'] = [options[2][1], options[2][2]]

    with open('selectData.json', mode="w") as f:
        # 選択されたデータを'selectData.json'に上書き
        json.dump(jsonData, f, indent=4)
    return render_template("pictureList.html")

# クイズ画面
@app.route('/test')
def test():
    print("test")
    with open('selectData.json') as f:
        # 既存のデータを読み込み
        jsonData = list(json.load(f))

    selectData = jsonData[0]
    return render_template("test.html", data = selectData)

# 削除ボタンが押された時の処理
@app.route('/delete_all/', methods=['POST'])
def delete_all():
    ImageProcessor().delete_all()
    return redirect(url_for('index'))   # index関数にリダイレクト  

# 削除ボタンが押された時の処理
@app.route('/delete_one', methods=['POST'])
def delete_one():
    img_data = request.form.to_dict()
    ImageProcessor().delete_one(img_data['img_name'])
    return redirect(url_for('uploaded_list'))   # index関数にリダイレクト

# Topページ
# http://127.0.0.1:5000/
@app.route('/')
def index():
    return render_template("image_form.html")

@app.route('/uploaded/<path:filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/processed/gs/<path:filename>')
def processed_gs_file(filename):
    return send_from_directory(app.config['OUTPUT_FOLDER'] + '/gs', filename)

@app.route('/processed/bin/<path:filename>')
def processed_bin_file(filename):
    return send_from_directory(app.config['OUTPUT_FOLDER'] + '/bin', filename)

@app.route('/processed/mozaiku/<path:filename>')
def processed_mozaiku_file(filename):
    return send_from_directory(app.config['OUTPUT_FOLDER'] + '/mozaiku', filename)


if __name__ == "__main__":
    # debugモードが不要の場合は、debug=Trueを消してください
    app.run(debug=True)