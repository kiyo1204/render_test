from flask import Flask, render_template, request, redirect
from flask import flash
from flask_login import LoginManager, current_user, login_user
from flask_migrate import Migrate
from flask_login import login_required
from flask_login import logout_user
from models import Task, db, User
from datetime import datetime, timedelta, timezone

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = (
    "mysql+pymysql://db_user:db_password@localhost/app_db"
)
app.secret_key = "deadbeef"
db.init_app(app)
Migrate(app, db)

login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html", title="ユーザ登録")
    else:
        if (
            request.form["id"] == ""
            or request.form["password"] == ""
            or request.form["lastname"] == ""
            or request.form["firstname"] == ""
        ):
            flash("入力されていない項目があります")
            return render_template("register.html", title="ユーザ登録")
        if User.query.get(request.form["id"]) is not None:
            flash("ユーザを登録できません")
            return render_template("register.html", title="ユーザ登録")
        user = User(
            id=request.form["id"],
            password=request.form["password"],
            lastname=request.form["lastname"],
            firstname=request.form["firstname"],
        )
        db.session.add(user)
        db.session.commit()
        return redirect("/")


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect("/")

    if request.method == "GET":
        return render_template("login.html", title="ログイン")
    else:
        user = User.query.get(request.form["id"])
        if user is not None and user.verify_password(request.form["password"]):
            login_user(user)
            return redirect("/")
        else:
            flash("ユーザIDかパスワードが誤っています")
            return redirect("/login")


@app.route("/logout")
def logout():
    logout_user()
    return redirect("/login")


@app.route("/")
@login_required
def index():
    my_tasks = Task.query.filter_by(user=current_user).order_by(Task.deadline)
    user = User.query.get(current_user.id)
    shared_tasks = Task.query.filter(
        (Task.user != current_user) & Task.is_shared
    ).order_by(Task.deadline)
    my_favorite_tasks = Task.query.filter(
        (Task.user == current_user) & (Task.my_favorite == True)
    ).order_by(Task.deadline)

    return render_template(
        "index.html",
        title="ホーム",
        my_tasks=my_tasks,
        shared_tasks=shared_tasks,
        user=user,
        my_favorite_tasks=my_favorite_tasks,
    )


@app.route("/account_delete", methods=["GET", "POST"])
def account_delete():
    Users = User.query.all()
    if request.method == "GET":
        return render_template("account_delete.html", title="アカウント削除")
    else:
        users = User.query.get(request.form["id"])
        for user in Users:
            if user.id is not None and users.verify_password(request.form["password"]):
                tasks = Task.query.filter_by(user=users)
                if tasks is not None:
                    for task in tasks:
                        db.session.delete(task)
                        db.session.commit()
                users = User.query.get(request.form["id"])
                db.session.delete(users)
                db.session.commit()
                return redirect("/")
            else:
                flash("ユーザIDかパスワードが誤っています")
                return redirect("/account_delete")


@app.route("/create", methods=["POST"])
@login_required
def create():
    if request.form["name"] and request.form["deadline"]:
        task = Task(
            user=current_user,
            name=request.form["name"],
            deadline=request.form["deadline"],
            is_shared=request.form.get("is_shared") is not None,
            my_favorite=request.form.get("my_favorite") is not None,
            created_at=datetime.now(timezone(timedelta(hours=+9))),
        )
        db.session.add(task)
        db.session.commit()
    else:
        flash("タスクまたは締切日時が入力されていません")
    return redirect("/")


@app.route("/update", methods=["GET", "POST"])
@login_required
def update():
    my_tasks = Task.query.filter_by(user=current_user).order_by(Task.deadline)
    task_id = [task.id for task in my_tasks]
    if request.method == "GET":
        return render_template("update.html", title="更新", my_tasks=my_tasks)
    else:
        for id in task_id:
            task = Task.query.get(id)
            task.name = request.form["name_" + str(id)]
            task.deadline = request.form["deadline_" + str(id)]
            task.is_shared = request.form.get("is_shared_" + str(id)) is not None
            task.my_favorite = request.form.get("my_favorite_" + str(id)) is not None
            db.session.commit()
        return redirect("/")


@app.route("/delete", methods=["GET", "POST"])
@login_required
def delete():
    my_tasks = Task.query.filter_by(user=current_user).order_by(Task.deadline)
    tasks_id = request.form.getlist("delete")
    if request.method == "GET":
        return render_template("delete.html", title="削除", my_tasks=my_tasks)
    else:
        for id in tasks_id:
            task = Task.query.get(id)
            db.session.delete(task)
            db.session.commit()
        return redirect("/")
