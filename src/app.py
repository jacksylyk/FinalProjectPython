from flask import Flask, request, render_template
from flask.cli import load_dotenv

import utils.scraper
from utils.database import db

from models.news import News

load_dotenv()

app = Flask(__name__)

app.config['SECRET_KEY'] = 'thisismyflasksecretkey'

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:0@localhost:5432/finalPython'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)


async def scrap(query):
    scraper = utils.scraper.Scraper()
    results = await scraper.scrap(query, 100)

    for result in results:
        news = News(
            url=result['url'],
            heading=result['heading'],
            paragraph=result['paragraph']
        )

        news.sync()

    return results


@app.route('/', methods=['GET'])
async def search():
    query = request.args.get('q')

    if not query:
        return render_template('base.html')

    return render_template('base.html', query=query, data=await scrap(query))


if __name__ == "__main__":
    app.run(debug=True)
