import os
import smtplib
import ssl
from email.mime.text import MIMEText
from dotenv import load_dotenv
from flask import Flask, jsonify, request

app = Flask(__name__)

# load_dotenv()
password = os.getenv("password_mail")
sender_email = os.getenv("sender_email")

def format_json_content(json_content):
    # Convert JSON data into a readable text format
    formatted_content = "Weather Forecast:\n\n"
    for day, data in json_content.items():
        formatted_content += (
            f"{day} - Date: {data['datetime']}\n"
            f"  Morning Temperature: {data['temp_morning']}°C\n"
            f"  Evening Temperature: {data['temp_evening']}°C\n"
            f"  Humidity: {data['humidity']}%\n\n"
        )
    return formatted_content

def send_email(email,json):
    
    port = 465
    smtp_server = "smtp.gmail.com"
    receiver_email = email
    
    body = format_json_content(json)
    
    # Use MIMEText to handle the message formatting
    msg = MIMEText(body, "plain", "utf-8")
    msg["Subject"] = "Weekly Weather Forecast"
    msg["From"] = sender_email
    msg["To"] = receiver_email

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())



@app.route('/send_mail', methods=['POST'])
def mail():

    data = request.get_json()
    receiver_email = data.get('email')
    json_content = data.get('data')

    send_email(receiver_email,json_content)
    return jsonify({"message": "Email sent successfully!"}), 200


if __name__ == "__main__":
    print('start')
    app.run(host="0.0.0.0", port=8001)

