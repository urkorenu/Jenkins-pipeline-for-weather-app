"""
Main module that serve as web interface
"""
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for
from weather import WeatherApp

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home_page():
    """
	Main page
    """
    if request.method == "GET":
        err = False
        if "error" in request.args:
            err = True
        return render_template("home.html", error=err)
    if request.method == "POST":
        location = request.form["location"]
        return redirect(url_for("post_location", location=location))


@app.get("/result")
def post_location():
    """
	Results page
    """
    today_date = datetime.today().date()
    location = request.args["location"]
    payload = WeatherApp.get_weather_data(location.lower(), today_date)
    if not payload:
        return redirect(url_for("home_page", error=True))

    return render_template(
        "weather_page.html",
        payload=payload,
        len=len(payload),
        title=f"Weather of: {location}",
    )


if __name__ == "__main__":
    app.run()
