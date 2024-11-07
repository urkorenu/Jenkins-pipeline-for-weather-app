import os
import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv
from flask_cors import CORS
from flask import Flask, jsonify, request

load_dotenv()
app = Flask(__name__)
CORS(app)

# Email credentials
password = os.getenv("password_mail")  # Make sure this is set correctly in .env
password = "phwi jqum keoy iuxb"  # This is just an example
sender_email = os.getenv("sender_mail")  # Sender email
sender_email = "ork39502@gmail.com"  # This is just an example

# Function to send email
def send_email(receiver_email, html_content):
    port = 587  # TLS port for Gmail
    smtp_server = "smtp.gmail.com"

    # Create the email message using MIMEMultipart to handle both HTML and plain text
    msg = MIMEMultipart("alternative")
    msg["Subject"] = "Weekly Weather Forecast"
    msg["From"] = sender_email
    msg["To"] = receiver_email

    # Attach the HTML content to the email message
    part = MIMEText(html_content, "html", "utf-8")
    msg.attach(part)

    # Set up the secure SSL context
    context = ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE

    try:
        # Establish a secure connection to the Gmail SMTP server and send the email
        with smtplib.SMTP(smtp_server, port) as server:
            server.starttls(context=context)  # Upgrade to secure connection
            server.login(sender_email, password)  # Login to your Gmail account
            server.sendmail(sender_email, receiver_email, msg.as_string())  # Send email
        print(f"Email sent to {receiver_email}")
    except Exception as e:
        print(f"Error sending email: {e}")

@app.route('/send_mail', methods=['POST'])
def mail():
    try:
        # Print the form data for debugging
        print("Form data received:", request.form)

        # Retrieve email and data (HTML content) from the form
        receiver_email = request.form.get('email')
        html_content = request.form.get('data')  # This contains the HTML content from the form

        # Check for missing email or content
        if not receiver_email or not html_content:
            print("Missing email or content in form data")
            return jsonify({"error": "Missing email or content"}), 400

        # Send email with the HTML content
        send_email(receiver_email, html_content)
        return jsonify({"message": "Email sent successfully!"}), 200

    except Exception as e:
        print("Error:", e)  # Print error to console
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    print('start')
    app.run(host="0.0.0.0", port=5001)

