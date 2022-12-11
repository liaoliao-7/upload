# coding:utf-8

from flask import Flask, render_template, request
import os

from datetime import timedelta

ALLOWED_EXTENSIONS = {'png', 'jpg', 'JPG', 'PNG', 'bmp'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


app = Flask(__name__)

app.send_file_max_age_default = timedelta(seconds=1)


@app.route('/upload', methods=['POST', 'GET'])
def upload():
    if request.method == 'POST':

        f = request.files['file']
        types = request.form.get("options")

        if not (f and allowed_file(f.filename)):
            return """<body><font size="50",font color="blue">请检查上传的图片类型，仅限于png、PNG、jpg、JPG、bmp</font><br/></body>"""
            # return jsonify({"error": 1001, "msg": "请检查上传的图片类型，仅限于png、PNG、jpg、JPG、bmp"})

        mtype = request.form.get("mtype")
        user_input = request.form.get("name")

        if user_input != "" and types != 0:

            basepath = os.path.dirname(__file__)
            upload_path = os.path.join(basepath, 'static/images/',
                                       mtype + user_input + "_" + types + '.jpg')

            if os.path.exists(upload_path):
                return """<body><font size="50",font color="blue">文件已存在，请勿重复上传</font><br/></body>"""
                # return jsonify({"error": 1003, "msg": "文件已存在，请勿重复上传"})
            f.save(upload_path)
            print("用户{0}提交了{1}信息。".format(user_input, types))

            return "<script>window.alert('提交成功');</script>"

        else:
            return """<body><font size="50",font color="blue">提交失败,请填写姓名,并选择对应的证件类型</font><br/></body>"""
            # return jsonify({"error": 1002, "msg": "提交失败,请填写姓名,并选择对应的证件类型"})

    return render_template('upload.html')


if __name__ == '__main__':
    # app.debug = True
    """本地ip地址，本地测试时使用"""
    app.run(host='192.168.1.3', port=8080, debug=True)

    """服务器ip地址，部署在服务器时使用"""
    # app.run(host='116.62.103.41.', port=8888, debug=True)
