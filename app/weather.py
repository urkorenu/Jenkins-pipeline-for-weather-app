"""
Main module for weather app, api interface
"""

import datetime
from functools import lru_cache
import requests
import json
import os
import ast
from deep_translator import GoogleTranslator
from config import KEY


class WeatherApp:
    """
    Main class of the
    """

    URL = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline"
    QUERY = (
        "next7days?unitGroup=metric&elements=datetime%2CdatetimeEpoch%2CresolvedAddress%2Ctempmax%2"
        "Ctempmin%2Ctemp%2Cfeelslike%2Chumidity%2Cwindspeed%2Cvisibility%2Cuvindex%2Csunrise%2"
        "Csunset&include=days&"
    )

    @classmethod
    @lru_cache(maxsize=32)
    def get_weather_data(cls, location: str, date: datetime):
        """
        Cached function!
        Sends a request, Convert it to json and call format_data with the jsoned dict
        Args:
            location(str): The location to be searched.
            date(datetime): The date of the call, for cache usage.

        Returns:
            Returns dict represent the jsoned response is it worked, else returns False.
        """
        print("Cached")
        response = requests.get(
            f"{cls.URL}/{location}/{cls.QUERY}{KEY}&contentType=json"
        )
        if response.status_code == 200:
            data = cls.format_data(response.json())
            file1 = open(f"history/{location}-{date}.txt", "w")
            json.dump(data, file1)
            return data
        return False

    @classmethod
    def format_file(cls, filename: str):
        file_path = os.path.join("history", filename)

        with open(file_path, "r") as file:
            content = file.read()
            return ast.literal_eval(content)

    @classmethod
    def format_data(cls, response: dict) -> list:
        """
        Format the response json dict to a list to display on the website.
        Args:
            response(dict): Dict represent the response json.

        Returns:
            List: Formatted list for the web app.
        """
        payload = [
            GoogleTranslator(source="auto", target="en").translate(
                response["resolvedAddress"]
            ),
            ["Date:"],
            ["Day Temp (c) : "],
            ["Night Temp (c) : "],
            ["Humidity (%) : "],
            ["Feels Like (c) : "],
            ["Sunrise : "],
            ["Sunset : "],
            ["UV Index : "],
            ["Wind (km/h) : "],
        ]
        for j in range(7):
            day = response["days"][j]
            payload[1].append(day["datetime"])
            payload[2].append(day["tempmax"])
            payload[3].append(day["tempmin"])
            payload[4].append(day["humidity"])
            payload[5].append(day["feelslike"])
            payload[6].append(day["sunrise"])
            payload[7].append(day["sunset"])
            payload[8].append(day["uvindex"])
            payload[9].append(day["windspeed"])
        return payload
