import os
import smtplib
import ssl
from email.mime.text import MIMEText
from dotenv import load_dotenv
from flask_cors import CORS
from flask import Flask, jsonify, request

load_dotenv()
app = Flask(__name__)
CORS(app)

# load_dotenv()
password = os.getenv("password_mail")
password = "phwi jqum keoy iuxb"
print(password)
sender_email = os.getenv("sender_mail")
sender_email = "ork39502@gmail.com"
print(sender_email)

def format_json_content(json_content):
    # Assuming json_content is a list where each inner list represents a specific field
    formatted_content = f"Weather Forecast for {json_content[0]}:\n\n"
    for i in range(1, len(json_content)):
        label = json_content[i][0]
        values = json_content[i][1:]
        formatted_content += f"{label}\n"
        for value in values:
            formatted_content += f"  {value}\n"
        formatted_content += "\n"
    return formatted_content


def send_email(email, json):
    port = 587  # TLS port for Gmail
    smtp_server = "smtp.gmail.com"
    receiver_email = email

    body = format_json_content(json)

    msg = MIMEText(body, "plain", "utf-8")
    msg["Subject"] = "Weekly Weather Forecast"
    msg["From"] = sender_email
    msg["To"] = receiver_email

    context = ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE
    with smtplib.SMTP(smtp_server, port) as server:
        server.starttls(context=context)  # Upgrade to secure connection
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())


@app.route('/send_mail', methods=['POST'])
def mail():
    try:
        data = request.get_json()
        receiver_email = data.get('email')
        json_content = data.get('data')

        send_email(receiver_email, json_content)
        return jsonify({"message": "Email sent successfully!"}), 200
    except Exception as e:
        print("Error:", e)  # Print error to console
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    print('start')
    app.run(host="0.0.0.0", port=5001)

