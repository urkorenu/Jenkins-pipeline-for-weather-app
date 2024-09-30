"""
Main module that serve as web interface
"""

from datetime import datetime
import os
from flask import Flask, render_template, request, redirect, url_for
from weather import WeatherApp
from files import get_files

app = Flask(__name__)
bg_color = os.environ.get("BG_COLOR")


@app.route("/", methods=["GET", "POST"])
def home_page():
    """
    Main page
    """
    if request.method == "GET":
        err = False
        if "error" in request.args:
            err = True
        return render_template("home.html", error=err, bg_color=bg_color)
    if request.method == "POST":
        location = request.form.get("location")
        if not location:
            return redirect(url_for("history"))
        return redirect(url_for("post_location", type="location", location=location))


@app.route("/history", methods=["GET", "POST"])
def history():

    files = get_files()
    if request.method == "GET":
        return render_template("history.html", files=files, bg_color=bg_color)
    if request.method == "POST":
        location = request.form.get("choice")
        return redirect(url_for("post_location", type="file", location=location))


@app.get("/result")
def post_location():
    """
    Results page
    """
    type = request.args["type"]
    location = request.args.get("location")
    if not type or not location:
        return redirect(url_for("home_page", error=True))
    payload = ""
    today_date = datetime.today().date()
    print(location, type)

    if type == "file":
        payload = WeatherApp.format_file(location)

    else:
        payload = WeatherApp.get_weather_data(location.lower(), today_date)

    if not payload:
        return redirect(url_for("home_page", error=True))

    return render_template(
        "weather_page.html",
        payload=payload,
        len=len(payload),
        title=f"Weather of: {location}",
        bg_color=bg_color
    )


if __name__ == "__main__":
    app.run()
