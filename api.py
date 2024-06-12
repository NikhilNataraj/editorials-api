import os
from dotenv import load_dotenv
import toi
import hindu

from datetime import datetime
from flask import Flask, jsonify, render_template
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy

load_dotenv()

app = Flask(__name__)
Bootstrap(app)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("POSTGRES_URI")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    source = db.Column(db.String(50), nullable=False)
    date = db.Column(db.String(255), nullable=False)


with app.app_context():
    db.create_all()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/articles")
def api_articles():
    articles = db.session.execute(db.select(Article).order_by(Article.id)).scalars()
    return jsonify(
        [{'title': article.title, 'content': article.content, 'source': article.source, 'date': article.date}
         for article in articles])


@app.route("/api/cron")
def fetch_articles():
    # Fetch articles from TOI
    toi_links = toi.get_toi_links()
    for link in toi_links:
        article = toi.get_article(link)
        if not db.session.execute(db.select(Article).where(Article.title == list(article.keys())[0])).scalar_one_or_none():
            store_article(article, "The Times of India")

    # Fetch articles from Hindu
    hindu_links = hindu.get_hindu_links()
    for link in hindu_links:
        article = hindu.get_article(link)
        if not db.session.execute(db.select(Article).where(Article.title == list(article.keys())[0])).scalar_one_or_none():
            store_article(article, "The Hindu")

    return jsonify({"message": "Articles fetched successfully"}), 200


def store_article(article, source):
    row = Article.query.count() + 1
    date = datetime.now().strftime("%B %d, %Y")
    for title, content in article.items():
        db_article = Article(id=row, title=title, content=content, source=source, date=date)
        db.session.add(db_article)
    db.session.commit()


@app.route("/api/article/<title>")
def get_article(title):
    # title = "%".join(list(title.split(" ")))
    # title_pattern = "%" + title + "%"
    with app.app_context():
        # required_article = db.session.execute(db.select(Article).where(Article.title.like(title_pattern))).scalar()
        articles = db.session.execute(db.select(Article).order_by(Article.id)).scalars().all()

        for article in articles:
            if article.title == title:
                article_data = {
                    'id': article.id,
                    'title': article.title,
                    'content': article.content,
                    'source': article.source,
                    'date': article.date
                }
                return jsonify(article_data)

    # if required_article:
    #     article_data = {
    #         'id': required_article.id,
    #         'title': required_article.title,
    #         'content': required_article.content,
    #         'source': required_article.source,
    #         'date': required_article.date
    #     }
    #     return jsonify(article_data)

    return {"error": "Article not found"}


if __name__ == "__main__":
    app.run()
