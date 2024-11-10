import requests

url = "http://localhost:5001/send_mail"
data = {
    "email": "ork14790@gmail.com",
    "data":
['Tel Aviv-Jaffa, Tel Aviv, Israel', ['Date:', '2024-11-03', '2024-11-04', '2024-11-05', '2024-11-06', '2024-11-07', '2024-11-08', '2024-11-09'], ['Day Temp (c) : ', 23.3, 23.4, 24.2, 26.8, 26.8, 26.8, 26.1], ['Night Temp (c) : ', 18.0, 16.0, 16.5, 15.5, 18.1, 22.2, 22.1], ['Humidity (%) : ', 77.3, 73.1, 77.9, 64.8, 59.0, 54.1, 54.2], ['Feels Like (c) : ', 20.4, 19.5, 20.0, 20.9, 21.7, 24.0, 23.8], ['Sunrise : ', '05:59:30', '06:00:21', '06:01:12', '06:02:04', '06:02:56', '06:03:48', '06:04:41'], ['Sunset : ', '16:48:56', '16:48:07', '16:47:20', '16:46:33', '16:45:48', '16:45:05', '16:44:23'], ['UV Index : ', 7.0, 7.0, 7.0, 7.0, 7.0, 6.0, 5.0], ['Wind (km/h) : ', 13.0, 14.8, 10.8, 16.2, 17.3, 29.5, 28.8]]


}
headers = {"Content-Type": "application/json"}

response = requests.post(url, json=data, headers=headers)
print(response.json())
print("Status Code:", response.status_code)
print("Response Text:", response.text)
