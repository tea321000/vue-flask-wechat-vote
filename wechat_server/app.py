
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_cors import *


# static_folder是js css等资源的目录，template_folder是SPA网页的目录
app = Flask(__name__, static_folder="./dist/static", template_folder="./dist")
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:1314mysql5354@127.0.0.1:3306/wechat'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'MyProject'
app.config['UPLOAD_FOLDER'] = './files'
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024
from vote import vote
from vote.sql import db
db.init_app(app)


app.register_blueprint(vote, url_prefix='/vote')
CORS(app, supports_credentials=True)
manager = Manager(app)


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return render_template("index.html")


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=yourport, debug=True)
    # 新建表用
    # manager.run()
