from flask import Flask, render_template, url_for
import psycopg2
import redis

app = Flask(__name__)

pg = psycopg2.connect(
    """
                      host=localhost
                      dbname=postgres
                      user=postgres
                      password=dozorov
                      port=5432"""
)

r = redis.Redis(host='localhost', port=6379, decode_responses=True)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/citi")
def read_count():
    pair = 'cities:count'
    redisCount = r.get(pair)
    if redisCount:
        result = redisCount + " (из redis КЭША)"
        return render_template("citi.html", value=result)
    
    
    cursor = pg.cursor()
    cursor.execute("SELECT COUNT(*) FROM city WHERE countrycode = 'RUS';")
    pgCount = cursor.fetchone()[0]

    result = str(pgCount) + " (из postgreSQL)"
    r.set(pair, pgCount)
    
    return render_template("citi.html", value=result)


if __name__ == "__main__":
    app.run(debug=True)
