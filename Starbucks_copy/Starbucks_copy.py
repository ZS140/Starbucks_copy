import random
import os
import datetime
import numpy
from PIL import Image, ImageDraw, ImageFont
from flask import render_template, request, redirect, url_for, Flask
from flask_login import login_user, LoginManager
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:1402929679zs@localhost/practical?charset=utf8"#登录数据库
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY'] = 'my-key'#密钥
db = SQLAlchemy(app)
class MyAnonymousUser():
    def __init__(self):
        self.username = "请登录"

    def is_active(self):
        return False

    def is_authenticated(self):  # 如果用户被认证，这个属性应该返回TRUE，即他们提供了有效的凭证。
        return False

    def get_id(self):
        return self.id
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))

    def __repr__(self):
        return '<User %r>' % self.username

    def is_active(self):
        return True

    def is_authenticated(self):  # 如果用户被认证，这个属性应该返回TRUE，即他们提供了有效的凭证。
        return True

    def get_id(self):
        return self.id
    @classmethod
    def checked(cls,username,password):
        user = cls.query.filter(db.and_(User.username == username,User.password == password)).first()
        return user
try:
    db.create_all()
except Exception as e:
    print(e)

login_Manager = LoginManager()
login_Manager.init_app(app)
login_Manager.login_view = "index"
login_Manager.anonymous_user = MyAnonymousUser


def create_identify():
    # 生成验证码
    array = numpy.zeros((100, 300, 3), dtype=numpy.uint8)
    Shape = array.shape
    for i in range(Shape[0]):
        for j in range(Shape[1]):
            for k in range(Shape[2]):
                array[i][j][k] = random.randint(0, 255)
    im = Image.fromarray(array)  # 生成图片
    draw = ImageDraw.Draw(im)  # 在生成的图片上添加文字
    L = [chr(i + 65) for i in range(26)] + [chr(i + 97) for i in range(26)]
    for i in range(4):
        draw.text((i * 75 + random.randint(0, 20), random.randint(0, 40)),
                  text=random.choice(L),
                  fill=(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)),
                  font=ImageFont.truetype(font="C:\Windows\Fonts\RosewoodStd-Regular.otf", size=80, index=0,
                                          encoding="", layout_engine=None))
    time = datetime.datetime.now().second
    im.save(r'D:\PyCharm 2017.3.2\Starbucks_copy\static\img\identify.jpg')
    return time


@login_Manager.user_loader#通过id回调返回用户对象，用于重新加载用户对象
def load_user(user_id):
    return User.query.get(user_id)
#首页
@app.route('/')
def index():
    return render_template('index.html')
#菜单
@app.route('/select')
def select():
    return render_template('select.html')
@app.route('/drink')
def drink():
    return render_template('drink.html')
@app.route('/coffee')
def coffee():
    return render_template('coffee.html')
@app.route('/choose')
def choose():
    return render_template('choose.html')
@app.route('/apps_intro1')
def apps_intro1():
    return render_template('apps-intro1.html')
@app.route('/apps_intro')
def apps_intro():
    return render_template('apps-intro.html')

@app.route('/enterprise_news')
def enterprise_news():
    return render_template('enterprise_news.html')
@app.route('/starbucks_in_china')
def starbucks_in_china():
    return render_template('starbucks_in_china.html')
@app.route('/job_offer')
def job_offer():
    return render_template('job_offer.html')
#登录界面
@app.route('/login',methods=['POST','GET'])
def login():
    time = create_identify()
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        remember = request.form.get('rem')
        result = User.checked(username,password)
        if result:
            print(remember)
            user = result
            if remember:
                login_user(user,remember=False)
            else:
                login_user(user, remember=True)
            try:
                return redirect(url_for("index"))
            except Exception as e:
                print(e)
        else:
            print('未登录')

    return render_template("login.html", vall = time)
#注册界面
@app.route("/register",methods=['POST','GET'])
def register():
    if request.method == 'POST':
        username = request.form['username_r']
        pw1 = request.form['password_r']
        pw2 = request.form['password_r2']
        if pw1 == pw2:
            register = User.query.filter_by(username = username).first()
            if register:
                print('该用户存在')
                return redirect(url_for('register'))
            user = User(username=username,password=pw1)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for("login"))
        else:
            print("两次密码不同")
            return redirect(url_for('register'))
    return render_template("register.html")
if __name__ == '__main__':

    app.run(host="127.0.0.1", port=8090, debug=True)
