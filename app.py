from flask import Flask
from flask import request,render_template,redirect,url_for,session,g
import utlis
import jidoong
import lagou
import maoyan
import news
import ajxc
app=Flask(__name__,static_url_path="/")
app.config['SECRET_KEY']="sjkhdwiuhdo2j"

@app.before_request
def before_request():
    users = utlis.get_data()
    g.user=None
    if 'user_id' in session:
        user=[u for u in users if u.id==int(session['user_id'])][0]
        g.user=user

@app.route("/login",methods=['GET','POST'])
def login():
    print(request.values.get("user"))
    if request.method=='POST':
        users = utlis.get_data()
        #登录操作
        session.pop('user_id',None)
        username=request.form.get("username",None)
        password = request.form.get("password", None)
        user=[user for user in users if user.username==username]
        if len(user)>0:
            user=user[0]
        if user and user.password==password:
            session['user_id']=user.id
            if request.values.get("user")=="manager":
                return redirect(url_for('page1'))
            else:
                return redirect(url_for('page2'))



    return render_template("login.html")

@app.route("/zhuce",methods=['GET','POST'])
def zhuce():
    if request.method=='POST':
        #注册操作
        username=request.form.get("username",None)
        password = request.form.get("password", None)
        utlis.insert_user(username,password)
        return redirect(url_for('login'))


    return  render_template("zhuce.html")

@app.route("/xiugai",methods=['GET','POST'])
def xiugai():
    if request.method=='POST':
        #注册操作
        username=request.form.get("username",None)
        password = request.form.get("password", None)
        utlis.user_alter(password,username)
        #print(username,password)
        return redirect(url_for('login'))
    return render_template("xiugai.html")

@app.route("/shanchu",methods=['GET','POST'])
def shanchu():
    if request.method=='POST':
        #注册操作
        username=request.form.get("username",None)
        utlis.user_delet(username)
        #print(username,password)
        return redirect(url_for('guanli'))
    return render_template("delet_user.html")

@app.route("/guanli",methods=['GET','POST'])
def guanli():
        #用户删除界面操作
        items = utlis.get_userdata()
        showtime = ajxc.get_time()
        return render_template('delet.html', items=items, showtime=showtime)


@app.route("/outcome")
def outcome():
    items = utlis.getItems()
    showtime = ajxc.get_time()
    return render_template('outcom.html', items=items,showtime=showtime)

@app.route("/outcomhuiyuan")
def outcomhuiyuan():
    items = utlis.getItems()
    showtime = ajxc.get_time()
    return render_template('outcomhuiyuan.html', items=items,showtime=showtime)

@app.route("/outcome2")
def outcome2():
    items = utlis.getItems_lagou()
    showtime = ajxc.get_time()
    return render_template('outcome2.html', items=items, showtime=showtime)

@app.route("/outcome2huiyuan")
def outcome2huiyuan():
    items = utlis.getItems_lagou()
    showtime = ajxc.get_time()
    return render_template('outcome2huiyuan.html', items=items, showtime=showtime)

@app.route("/outcome3")
def outcome3():
    items = utlis.getItems_maoyan()
    showtime = ajxc.get_time()
    return render_template('outcome3.html', items=items, showtime=showtime)

@app.route("/outcome4")
def outcome4():
    items = utlis.getItems_new()
    showtime = ajxc.get_time()
    return render_template('outcome4.html', items=items, showtime=showtime)

@app.route("/outcome4huiyuan")
def outcome4huiyuan():
    items = utlis.getItems_new()
    showtime = ajxc.get_time()
    return render_template('outcome4huiyuan.html', items=items, showtime=showtime)

@app.route("/page1",methods=['GET','POST'])
def page1():
    if not g.user:
        return redirect(url_for('login'))
    elif request.method=='POST':
        #搜索操作
        url=request.form.get("jingong_url",None)
        subject = request.form.get("subject", None)
        if url=='https://www.jd.com/':
             #jidoong.spider(url,subject)
             return redirect(url_for('outcome'))
        elif url=='https://www.lagou.com/':
             #lagou.spider(url,subject)
             return redirect(url_for('outcome2'))
        elif url=='https://maoyan.com/board/4':
             #maoyan.spider(url)
             return redirect(url_for('outcome3'))
        elif url=='https://news.sina.com.cn/china/':
             #news.spider(url)
             return redirect(url_for('outcome4'))
        else:
             return redirect(url_for('page1'))  #网址输入有误就不跳转

    return render_template("page1.html")

@app.route("/page2",methods=['GET','POST'])
def page2():
    if not g.user:
        return redirect(url_for('login'))
    elif request.method=='POST':
        #搜索操作
        url=request.form.get("jingong_url",None)
        subject = request.form.get("subject", None)
        if url=='https://www.jd.com/':
             #jidoong.spider(url,subject)
             return redirect(url_for('outcomhuiyuan'))
        elif url=='https://www.lagou.com/':
             #lagou.spider(url,subject)
             return redirect(url_for('outcome2huiyuan'))
        elif url=='https://maoyan.com/board/4':
             #maoyan.spider(url)
             return redirect(url_for('outcome3'))
        elif url=='https://news.sina.com.cn/china/':
             #news.spider(url)
             return redirect(url_for('outcome4huiyuan'))
        else:
             return redirect(url_for('page2'))  #网址输入有误就不跳转

    return render_template("page2.html")

#print(users)
@app.route("/logout")
def logout():
    session.pop("user_id", None)
    return redirect(url_for('login'))

@app.route('/time')
def gettime():
    return  gettime.get_time()



#https://www.jd.com/
#diy红绳珍珠庄梦蝶
if __name__=="__main__":
    app.run()