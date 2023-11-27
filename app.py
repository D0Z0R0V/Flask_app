import requests, sqlite3
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)


def get_db_connection():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn


def db_hisotry(city, temperature, icon):
    conn = get_db_connection()
    conn.execute(
        "INSERT INTO posts (context, tempr, icon) VALUES(?, ?, ?)",
        (city, temperature, icon),
    )
    conn.commit()
    conn.close()


def get_weather_data(city):
    appid = "f6ae488f0ab8f3b69469ef0f66452b1b"
    url = (
        "https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=".format(
            city
        )
        + appid
    )

    response = requests.get(url)
    weather_data = response.json()

    if response.status_code != 200:
        return None

    return weather_data


@app.route("/", methods=("POST", "GET"))
def index():
    if request.method == "POST":
        city = request.form["city"]
        weather_data = get_weather_data(city)

        if not weather_data:
            return redirect(url_for("error"))

        city = weather_data["name"]
        temperature = int(weather_data["main"]["temp"])
        icon = weather_data["weather"][0]["icon"]

        db_hisotry(city, temperature, icon)

        return render_template(
            "weather.html", city=city, temperature=temperature, icon=icon
        )

    return render_template("weather.html")


@app.route("/history", methods=("POST", "GET"))
def history():
    conn = get_db_connection()
    posts = conn.execute("SELECT * FROM posts").fetchall()
    conn.close()

    return render_template("history.html", posts=posts)


@app.route("/delete", methods=("POST",))
def delete():
    conn = get_db_connection()
    conn.execute("DELETE FROM posts")
    conn.commit()
    conn.close()
    return redirect(url_for("index"))


@app.route("/error")
def error():
    error_message = "Ошибка при запросе данных"
    return render_template("error.html", error_message=error_message)


@app.route("/info")
def info():
    return render_template("info.html")


@app.route("/doc")
def doc():
    return render_template("document.html")


if __name__ == "__main__":
    app.run(debug=True)
