import os
from dotenv import load_dotenv
import toi
import hindu

from flask import Flask, jsonify, render_template
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_apscheduler import APScheduler

load_dotenv()

app = Flask(__name__)
Bootstrap(app)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("POSTGRES_URI")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Config:
    SCHEDULER_API_ENABLED = True


app.config.from_object(Config())


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    source = db.Column(db.String(50), nullable=False)


with app.app_context():
    db.create_all()

scheduler = APScheduler()
scheduler.init_app(app)

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/articles")
def api_articles():
    articles = Article.query.all()
    return jsonify(
        [{'title': article.title, 'content': article.content, 'source': article.source} for article in articles])


@scheduler.task('interval', id='fetch_articles', minutes=720)
def fetch_articles():
    # Fetch articles from Hindu
    hindu_links = hindu.get_hindu_links()
    for link in hindu_links:
        article = hindu.get_article(link)
        store_article(article, "Hindu")

    # Fetch articles from TOI
    toi_links = toi.get_toi_links()
    for link in toi_links:
        article = toi.get_article(link)
        store_article(article, "TOI")


def store_article(article, source):
    for title, content in article.items():
        db_article = Article(title=title, content=content, source=source)
        db.session.add(db_article)
    db.session.commit()


if __name__ == "__main__":
    scheduler.start()
    app.run()
