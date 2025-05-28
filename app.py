from flask import Flask, request, redirect, url_for, render_template
from flask_sqlalchemy import SQLAlchemy


app: Flask = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///english_memo.sqlite"
db:SQLAlchemy = SQLAlchemy(app)

class MemoItem(db.Model):
    id: int = db.Column(db.Integer, primary_key=True)
    phrase: str = db.Column(db.Text, nullable=False)
    meaning: str = db.Column(db.Text, nullable=False)
    
# データベースの初期化
with app.app_context():
    db.create_all()


@app.route("/")
def index():
    items = MemoItem.query.order_by(MemoItem.phrase).all()
    items.insert(0, {"id": 0, "phrase": "New phrase/word", "meaning": "meaning"})
    return render_template("list.html", items=items)

@app.route("/memo/<int:id>", methods=["GET", "POST"])
def memo(id: int):
    #メモ取得
    it = MemoItem.query.get(id)
    if id == 0 or it is None:
        #新規メモ
        it = MemoItem(phrase="__none__", meaning="")
    #POSTの場合はデータを保存
    if request.method == "POST":
        it.phrase = request.form.get("phrase", "__none__")
        it.meaning = request.form.get("meaning", "")
        if it.phrase == "":
            return "phraseは空にできません"
        if id == 0:
            db.session.add(it)
        db.session.commit()
        return redirect(url_for("index"))

    #メモの編集画面を表示
    return render_template("memo.html", it=it)

if __name__ == "__main__":
    app.run(debug=True, port=8888)